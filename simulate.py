import random
import json
import pandas as pd
from utils import (
    LLM_persuade,
    handle_user_side,
    handle_user_tweet,
    LLM_update_profile_5_and_LLM_get_reason,
    handle_user_reconnect,
    initialize_tweet,
)
from multiprocessing import Pool, Manager
from pebble import ProcessPool
import os
import tqdm
import concurrent
import networkx as nx
import copy
import time

import sys


class User:
    def __init__(
        self,
        node_id,
        profile,
        message_list=[],
        friend_pool=[],
        var_dict={},
        probability=0.9,
    ):
        self.node_id = node_id
        self.previous_message = []
        self.message_list = message_list
        self.profile = profile
        self.friend_pool = friend_pool
        self.profile["reasons"] = ""
        self.prompt_hist = {}
        self.prompt_hist["LLM_update_profile_5"] = []
        self.prompt_hist["LLM_get_reason"] = []
        self.prompt_hist["LLM_action"] = []
        self.prompt_hist["LLM_willing_tweet_5"] = []
        self.prompt_hist["LLM_persuade"] = []
        self.prompt_hist["LLM_update_profile_5_and_LLM_get_reason"] = []
        self.prompt_hist["initialize_tweet"] = []
        self.var_dict = var_dict
        self.target_size = len(self.friend_pool)

        if not self.message_list and random.random() > probability:
            generate_message = initialize_tweet(self.profile, var_dict)
            self.mark_prompt(
                "initialize_tweet", generate_message, {"profile": self.profile}
            )
            self.message_list.append(
                {
                    "source": self.node_id,
                    "target": None,
                    "content": generate_message,
                }
            )
            self.profile["reasons"] = generate_message
            self.update_profile(initialize=True)

    def mark_prompt(self, prompt, result, input):
        self.prompt_hist[prompt].append(
            {
                "profile": copy.deepcopy(self.profile),
                "input": copy.deepcopy(input),
                "result": copy.deepcopy(result),
            }
        )

    def update_profile(self, initialize=False):
        string_new = ""
        difference = [
            d
            for d in self.message_list[-300:]
            if d not in self.previous_message[-300:]
        ]
        for i in range(5 if len(difference) > 5 else len(difference)):
            string_new += difference[-i]["content"]
        string_old = ""
        same = [
            d
            for d in self.message_list[-300:]
            if d in self.previous_message[-300:]
        ]
        for i in range(5 if len(same) > 5 else len(same)):
            string_old += same[-i]["content"]
        temp = LLM_update_profile_5_and_LLM_get_reason(
            self.profile, string_new[-1000:], string_old[-1000:], self.var_dict
        )
        self.mark_prompt(
            "LLM_update_profile_5_and_LLM_get_reason",
            temp,
            {
                "profile": self.profile,
                "string_old": string_old[-1000:],
                "string_new": string_new[-1000:],
            },
        )
        self.profile["side"] = temp["side"]
        self.profile["reasons"] = "".join(temp["reasons"])
        self.profile["tendency"] = temp["tendency"]
        return self

    def persuade(self, target):
        string = ""
        for i in range(
            5 if len(self.message_list) > 5 else len(self.message_list)
        ):
            string += self.message_list[-i]["content"]
            persuade = LLM_persuade(
                self.profile, string[-1000:], target.profile, self.var_dict
            )
            self.mark_prompt(
                "LLM_persuade", persuade, [string[-1000:], target.profile]
            )
            persuade = json.loads(persuade)

        return persuade


def create_node(
    id, message_user, neighbour_list, given_profile, var_dict, probability
):
    profile = copy.deepcopy(given_profile)
    profile["p_side"] = copy.deepcopy(profile["side"])
    message_list = []
    for tweet in message_user:
        message_list.append({"source": id, "target": None, "content": tweet})
    return User(
        id,
        profile,
        message_list,
        [int(temp) for temp in neighbour_list],
        var_dict,
        probability,
    )


if __name__ == "__main__":
    var_dict = {}
    var_dict["environment"] = sys.argv[1]
    var_dict["topic"] = sys.argv[2]
    var_dict["S_m2"] = sys.argv[3]
    var_dict["S_m1"] = sys.argv[4]
    var_dict["S_0"] = sys.argv[5]
    var_dict["S_p1"] = sys.argv[6]
    var_dict["S_p2"] = sys.argv[7]
    var_dict["S_m2_e"] = sys.argv[8]
    var_dict["S_m1_e"] = sys.argv[9]
    var_dict["S_0_e"] = sys.argv[10]
    var_dict["S_p1_e"] = sys.argv[11]
    var_dict["S_p2_e"] = sys.argv[12]
    var_dict["side_b_0"] = sys.argv[13]
    var_dict["side_s_0"] = sys.argv[14]
    var_dict["side_e_0"] = sys.argv[15]

    starting_time = time.time()
    datasource = sys.argv[16]

    num_epoch = int(sys.argv[17])

    side_init = sys.argv[18].split(",")
    ex_sup = float(side_init[0])
    sup = float(side_init[1])
    neu = float(side_init[2])
    opp = float(side_init[3])
    ex_opp = float(side_init[4])

    sideP_list = {2: ex_sup, 1: sup, 0: neu, -1: opp, -2: ex_opp}

    abb = sys.argv[19]
    starting_epoch = int(sys.argv[20])
    save_path = f"./output_pol/e{num_epoch}_prob{ex_sup},{sup},{neu},{opp},{ex_opp}_{datasource}_{abb}/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    datasource += "/"

    edges = pd.read_csv(
        datasource + "edges.csv",
        usecols=["source", "target"],
        dtype={"source": int, "target": int},
    )
    G = nx.from_pandas_edgelist(
        edges, source="source", target="target", create_using=nx.DiGraph()
    )
    nodes = pd.read_csv(
        datasource + "data_ID2Net_ID.csv",
        usecols=["Network_id"],
        dtype={"Network_id": int},
    )
    G.add_nodes_from(nodes["Network_id"])

    user_list = []
    num_nodes = G.number_of_nodes()
    message = json.load(
        open(datasource + "user_message_generate.json", "r", encoding="utf-8")
    )

    created_user_pool = []
    specified_numbers = {
        -2: [],
        -1: [],
        0: [],
        1: [],
        2: [],
    }
    for i in specified_numbers:
        specified_numbers[i] = [int(x) for x in specified_numbers[i]]

    initial_side_dict = {}
    node_side = {}
    node_list = list(range(num_nodes))
    for i in specified_numbers:
        node_list = list(set(node_list) - set(specified_numbers[i]))
        for j in specified_numbers[i]:
            initial_side_dict[j] = i

    for i in range(-2, 3):
        temp = random.sample(
            node_list,
            int(num_nodes * sideP_list[i] - len(specified_numbers[i])),
        )
        for j in temp:
            initial_side_dict[j] = i
        node_list = list(set(node_list) - set(temp))
    with ProcessPool(max_workers=50) as pool:
        for id in range(num_nodes):
            created_user_pool.append(
                pool.schedule(
                    create_node,
                    [
                        id,
                        message[str(id)],
                        G.successors(id),
                        {"side": initial_side_dict[id]},
                        var_dict,
                        1 if starting_epoch else 0.9,
                    ],
                    timeout=40,
                )
            )

        updated_user = list(range(num_nodes))

        retry_index = [i for i in range(num_nodes)]
        while retry_index:
            new_retry_index = []
            for i in tqdm.tqdm(retry_index):
                try:
                    updated_user[i] = created_user_pool[i].result()
                except concurrent.futures._base.TimeoutError:
                    new_retry_index.append(i)
                    created_user_pool[i] = pool.schedule(
                        create_node,
                        [
                            i,
                            message[str(i)],
                            G.successors(i),
                            {"side": initial_side_dict[i]},
                            var_dict,
                            1 if starting_epoch else 0.9,
                        ],
                        timeout=40,
                    )
            retry_index = new_retry_index

    user_list = list(range(num_nodes))
    for user in updated_user:
        user_list[user.node_id] = user

    def load_data(epoch):
        with open(save_path + f"p_edges_{epoch}.txt", "r") as file:
            edges = [line.strip().split() for line in file.readlines()]
            for user in user_list:
                user.friend_pool = []
            for edge in edges:
                user_list[int(edge[0])].friend_pool.append(int(edge[1]))
        loaded_message_pool = json.load(
            open(
                save_path + f"message_pool_{epoch}.json", "r", encoding="utf-8"
            )
        )
        loaded_previous_message = json.load(
            open(
                save_path + f"previous_message_{epoch}.json",
                "r",
                encoding="utf-8",
            )
        )
        loaded_profile = json.load(
            open(save_path + f"profile_{epoch}.json", "r", encoding="utf-8")
        )
        for user in user_list:
            user.previous_message = loaded_previous_message[str(user.node_id)]
            user.message_list = loaded_message_pool[str(user.node_id)]
            user.profile = loaded_profile[str(user.node_id)]

    if starting_epoch:
        load_data(starting_epoch)

    def spread():
        return_index = []
        for user in user_list:
            difference = [
                d
                for d in user.message_list[-300:]
                if d not in user.previous_message[-300:]
            ]
            for message in difference:
                if message["source"] == user.node_id:
                    if message["target"]:
                        user_list[message["target"]].message_list.append(
                            message
                        )
                        return_index.append(message["target"])
                    else:
                        for target_id in user.friend_pool:
                            if target_id != user.node_id:
                                temp = {
                                    "source": message["source"],
                                    "target": target_id,
                                    "content": message["content"],
                                }
                                user_list[target_id].message_list.append(temp)
                                return_index.append(target_id)
            user.previous_message = copy.deepcopy(user.message_list)
        return return_index

    def save_data(epoch):
        message_pool = {}
        for user in user_list:
            message_pool[user.node_id] = user.message_list
        json.dump(
            message_pool,
            open(
                save_path + "message_pool_" + str(epoch) + ".json",
                "w",
                encoding="utf-8",
            ),
            ensure_ascii=False,
        )
        message_pool = {}
        for user in user_list:
            message_pool[user.node_id] = user.previous_message
        json.dump(
            message_pool,
            open(
                save_path + "previous_message_" + str(epoch) + ".json",
                "w",
                encoding="utf-8",
            ),
            ensure_ascii=False,
            indent=4,
        )
        with open(save_path + "p_edges_" + str(epoch) + ".txt", "w") as file:
            for user in user_list:
                for friend in user.friend_pool:
                    file.write(f"{user.node_id} {friend}\n")
        profile_list = {}
        for user in user_list:
            profile_list[user.node_id] = copy.deepcopy(user.profile)
            user.profile["p_side"] = copy.deepcopy(user.profile["side"])
        json.dump(
            profile_list,
            open(
                save_path + "profile_" + str(epoch) + ".json",
                "w",
                encoding="utf-8",
            ),
            ensure_ascii=False,
            indent=4,
        )
        hist_list = {}
        for user in user_list:
            hist_list[user.node_id] = copy.deepcopy(user.prompt_hist)
            user.prompt_hist = {}
            user.prompt_hist["LLM_update_profile_5"] = []
            user.prompt_hist["LLM_get_reason"] = []
            user.prompt_hist["LLM_action"] = []
            user.prompt_hist["LLM_willing_tweet_5"] = []
            user.prompt_hist["LLM_persuade"] = []
            user.prompt_hist["LLM_update_profile_5_and_LLM_get_reason"] = []
        json.dump(
            hist_list,
            open(
                save_path + "history_" + str(epoch) + ".json",
                "w",
                encoding="utf-8",
            ),
            ensure_ascii=False,
            indent=4,
        )
        updated_user_friend_pair_store = []
        for i in updated_user_friend_pair:
            updated_user_friend_pair_store.append(
                [i[0], i[1].node_id, i[2].node_id]
            )
        json.dump(
            updated_user_friend_pair_store,
            open(
                save_path + "updated_user_friend_pair_" + str(epoch) + ".txt",
                "w",
            ),
        )
        json.dump(
            reconnecting_remark,
            open(
                save_path + "reconnecting_remark_" + str(epoch) + ".txt",
                "w",
                encoding="utf-8",
            ),
            ensure_ascii=False,
            indent=4,
        )

    if not starting_epoch:
        updated_user_friend_pair = []
        reconnecting_remark = []
        save_data(0)

    pool = Pool(processes=50)
    manager = Manager()
    lock = manager.Lock()
    print(starting_epoch)
    for epoch in range(starting_epoch + 1, num_epoch + 1):
        print(epoch)

        updating_user_index = spread()

        print("handle_user_side")
        updated_user_pool = []
        updating_user = list(set([user_list[i] for i in updating_user_index]))

        with ProcessPool(max_workers=50) as pool:
            for i in range(len(updating_user)):
                updated_user_pool.append(
                    pool.schedule(
                        handle_user_side,
                        [
                            updating_user[i],
                        ],
                        timeout=40,
                    )
                )

            updated_user = updating_user

            retry_index = [i for i in range(len(updating_user))]
            while retry_index:
                new_retry_index = []
                for i in tqdm.tqdm(retry_index):
                    try:
                        updated_user[i] = updated_user_pool[i].result()
                    except concurrent.futures._base.TimeoutError:
                        new_retry_index.append(i)
                        updated_user_pool[i] = pool.schedule(
                            handle_user_side,
                            [
                                updating_user[i],
                            ],
                            timeout=80,
                        )
                retry_index = new_retry_index
        changed_side = 0
        for user in updated_user:
            if user.profile["side"] != user_list[user.node_id].profile["side"]:
                changed_side += 1
            user_list[user.node_id] = user
        print(f"side changed:{changed_side}")

        updating_friend_pair = []

        for user in updated_user:
            for friend in user.friend_pool:
                updating_friend_pair.append([user, user_list[friend]])
        updated_user_friend_pair_pool = []
        with ProcessPool(max_workers=50) as pool:
            for i in range(len(updating_friend_pair)):
                updated_user_friend_pair_pool.append(
                    pool.schedule(
                        handle_user_reconnect,
                        updating_friend_pair[i],
                        timeout=60,
                    )
                )

            updated_user_friend_pair = updating_friend_pair
            print("handle_user_reconnect")
            retry_index = [i for i in range(len(updating_friend_pair))]
            while retry_index:
                new_retry_index = []
                for i in tqdm.tqdm(retry_index):
                    try:
                        updated_user_friend_pair[i] = (
                            updated_user_friend_pair_pool[i].result()
                        )
                    except concurrent.futures._base.TimeoutError:
                        new_retry_index.append(i)
                        updated_user_friend_pair_pool[i] = pool.schedule(
                            handle_user_reconnect,
                            updating_friend_pair[i],
                            timeout=160,
                        )
                retry_index = new_retry_index

        reconnected_edge = 0
        reconnecting_remark = []
        for temp in updated_user_friend_pair:
            if not temp[0]:
                reconnecting_remark.append(
                    {
                        "result": "no",
                        "user": temp[1].node_id,
                        "target": temp[2].node_id,
                        "user_profile": temp[1].profile,
                        "target_profile": temp[2].profile,
                        "explain": temp[3],
                    }
                )
                reconnected_edge += 1
                user_list[temp[1].node_id].friend_pool.remove(temp[2].node_id)
                not_self = True
                while not_self:
                    new_friend = random.randint(0, num_nodes - 1)
                    if new_friend != temp[1].node_id:
                        not_self = False

                user_list[temp[1].node_id].friend_pool.append(new_friend)
            else:
                reconnecting_remark.append(
                    {
                        "result": "yes",
                        "user": temp[1].node_id,
                        "target": temp[2].node_id,
                        "user_profile": temp[1].profile,
                        "target_profile": temp[2].profile,
                        "explain": temp[3],
                    }
                )

        print(f"reconnected edges:{reconnected_edge}")

        updated_user_target_pool = []
        updating_user = list(set([user_list[i] for i in updating_user_index]))
        updating_user_target = []
        for i in updating_user:
            for j in i.friend_pool:
                updating_user_target.append([i, user_list[j]])

        updating_user_target = [
            list(x) for x in set(tuple(x) for x in updating_user_target)
        ]

        with ProcessPool(max_workers=50) as pool:
            for i in range(len(updating_user_target)):
                updated_user_target_pool.append(
                    pool.schedule(
                        handle_user_tweet,
                        updating_user_target[i],
                        timeout=40,
                    )
                )

            updated_user_target = updating_user_target
            print("handle_user_tweet")
            retry_index = [i for i in range(len(updating_user_target))]
            while retry_index:
                print(retry_index)
                new_retry_index = []
                for i in tqdm.tqdm(retry_index):
                    try:
                        updated_user_target[i] = updated_user_target_pool[
                            i
                        ].result()
                    except concurrent.futures._base.TimeoutError:
                        new_retry_index.append(i)
                        updated_user_target_pool[i] = pool.schedule(
                            handle_user_tweet,
                            updating_user_target[i],
                            timeout=80,
                        )
                retry_index = new_retry_index
        willing_to_speak = 0
        for i in updated_user_target:
            if i[0] != "no" and i[0] != "No":
                willing_to_speak += 1
                user_list[i[1].node_id].message_list.append(
                    {
                        "source": i[1].node_id,
                        "target": i[2].node_id,
                        "content": i[0],
                    }
                )
        print(f"spoken line:{willing_to_speak}")
        save_data(epoch)
        print(f"end of epoch {epoch}")
        epoch_time = time.time()
        print("time_spent" + str(epoch_time - starting_time))
