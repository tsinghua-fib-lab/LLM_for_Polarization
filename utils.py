import json
import openai
import time
import requests

openai.api_key = ""
llama_port = ""


def get_completion_0(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=5,
    )
    return response.choices[0].message["content"]


def get_completion_0_llama(prompt):
    messages = [{"role": "user", "content": prompt}]
    res = requests.post(
        "http://localhost:" + llama_port + "/chat", json={"messages": messages}
    )
    res = json.loads(res.text)
    return res["choices"][0]["message"]["content"]


def get_completion_1(prompt, model="gpt-3.5-turbo", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=5,
    )
    return response.choices[0].message["content"]


def get_completion_1_llama(prompt):
    messages = [{"role": "user", "content": prompt, "temperature": 1}]
    res = requests.post(
        "http://localhost:" + llama_port + "/chat", json={"messages": messages}
    )
    res = json.loads(res.text)
    return res["choices"][0]["message"]["content"]


def LLM_persuade(
    profile: dict, message_list: str, target_profile: dict, var_dict: dict
):
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    max_retries = 1000000
    for i in range(max_retries):
        try:
            string = f"Assume you are someone who cares about {environment}."
            string += (
                f"Your thought about {topic} are: <<<"
                + profile["reasons"]
                + ">>>\n"
            )
            string += (
                "You have recieved some tweets from your friends:<<<"
                + message_list
                + ">>>\n"
            )
            string += "Do you want to interact with or persuade a friend of yours to support your thought, that has the following thought:\n"
            string += "<<<" + target_profile["reasons"] + ">>>\n"
            string += "If yes, please generate a message to persuade your friend into supporting your perspective with around 50 words.\n"
            string += "Please return in json format with 2 keys: 'will' and 'message'. Please keep the message as short as possible.\n"
            string += "'will' should be either 'yes' or 'no'\n"
            string += "If no, leave 'message' blank.\n"
            string += "check if the response is in json format."
            message = get_completion_1(string)
            json.loads(message)

            if "yes" in message or "no" in message:
                return message
            else:
                raise
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2)
                print(e)
            else:
                raise


def LLM_persuade_debias_sim(
    profile: dict, message_list: str, target_profile: dict, var_dict: dict
):
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    max_retries = 1000000
    retry = 0
    for i in range(max_retries):
        try:

            string = f"Assume you are someone who cares about {environment}."
            string += (
                f"Your thought about {topic} are: <<<"
                + profile["reasons"]
                + ">>>\n"
            )
            string += (
                "You have recieved some tweets from your friends:<<<"
                + message_list
                + ">>>\n"
            )
            string += "Do you want to interact with or persuade a friend of yours to support your thought, that has the following thought:\n"
            string += "<<<" + target_profile["reasons"] + ">>>\n"
            string += "If yes, please generate a message to persuade your friend into supporting your perspective with around 50 words.\n"
            string += "Please return in json format with 2 keys: 'will' and 'message'. Please keep the message as short as possible.\n"
            string += "'will' should be either 'yes' or 'no'\n"
            string += "If no, leave 'message' blank.\n"
            string += "check if the response is in json format."
            message = get_completion_1(string)
            test = json.loads(message)
            test1 = test["will"]
            test2 = test["message"]
            if "no" in test1 or "No":
                return message
            elif "yes" in test1 or "Yes":
                string = (
                    "You tried to persuade your friend with the following message: <<<"
                    + test2
                    + ">>>\n"
                )
                string += "Do you find the message persuasive enough to persuade your friend to:"
                if profile["side"] == -2:
                    string += f"<<<{var_dict['S_m2']}>>>"
                if profile["side"] == -1:
                    string += f"<<<{var_dict['S_m1']}>>>"
                if profile["side"] == 0:
                    string += f"<<<{var_dict['S_0']}>>>"
                if profile["side"] == 1:
                    string += f"<<<{var_dict['S_p1']}>>>"
                if profile["side"] == 2:
                    string += f"<<<{var_dict['S_p2']}>>>"
                string += "? Please respond yes or no only.\n"
                persuasive = get_completion_1(string)
                if "yes" in persuasive or "Yes" in persuasive:
                    return message
            if retry > 2:
                return json.dumps({"will": "no", "message": ""})
            retry += 1
        except Exception as e:
            if i < max_retries - 1:
                print(e)
                time.sleep(2)
            else:
                raise


def LLM_persuade_debias_sim_kol(
    profile: dict, message_list: str, target_profile: dict, var_dict: dict
):
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    max_retries = 1000000
    retry = 0
    for i in range(max_retries):
        try:

            string = f"Assume you are someone who cares about {environment}."
            if profile["kol"]:
                string += f"You are a key opinion leader in {environment}, skilled at persuading others to adopt your opinions.\n"
            string += (
                f"Your thought about {topic} are: <<<"
                + profile["reasons"]
                + ">>>\n"
            )
            string += (
                "You have recieved some tweets from your friends:<<<"
                + message_list
                + ">>>\n"
            )
            string += "Do you want to interact with or persuade a friend of yours to support your thought, that has the following thought:\n"
            string += "<<<" + target_profile["reasons"] + ">>>\n"
            string += "If yes, please generate a message to persuade your friend into supporting your perspective with around 50 words.\n"
            string += "Please return in json format with 2 keys: 'will' and 'message'. Please keep the message as short as possible.\n"
            string += "'will' should be either 'yes' or 'no'\n"
            string += "If no, leave 'message' blank.\n"
            string += "check if the response is in json format."
            message = get_completion_1(string)
            test = json.loads(message)
            test1 = test["will"]
            test2 = test["message"]
            if "no" in test1 or "No" in test1 and retry <= 1:
                return message
            elif "yes" in test1 or "Yes" in test1 and retry <= 1:
                string = (
                    "You tried to persuade your friend with the following message: <<<"
                    + test2
                    + ">>>\n"
                )
                string += "Do you find the message persuasive enough to persuade your friend to:"
                if profile["side"] == -2:
                    string += f"<<<{var_dict['S_m2']}>>>"
                if profile["side"] == -1:
                    string += f"<<<{var_dict['S_m1']}>>>"
                if profile["side"] == 0:
                    string += f"<<<{var_dict['S_0']}>>>"
                if profile["side"] == 1:
                    string += f"<<<{var_dict['S_p1']}>>>"
                if profile["side"] == 2:
                    string += f"<<<{var_dict['S_p2']}>>>"
                string += "? Please respond yes or no only.\n"
                persuasive = get_completion_1(string)
                if "yes" in persuasive or "Yes" in persuasive:
                    if profile["kol"]:
                        test["message"] = (
                            "The following message is from a key opinion leader in "
                            + environment
                            + ", skilled at persuading you to adopt his/her opinions:"
                            + test["message"]
                            + "\n\n"
                        )
                    else:
                        test["message"] = (
                            "The following message is from a person who cares about "
                            + environment
                            + ":"
                            + test["message"]
                            + "\n\n"
                        )
                    message = json.dumps(test)
                    return message
            if retry > 2:
                return json.dumps({"will": "no", "message": ""})
            retry += 1

        except Exception as e:
            retry += 1
            if i < max_retries - 1:
                print(e)
                time.sleep(2)
            else:
                raise


def LLM_get_reason(profile: dict, message_list: str, var_dict: dict):

    environment = var_dict["environment"]
    topic = var_dict["topic"]
    side_s_0 = var_dict["side_s_0"]
    side_b_0 = var_dict["side_b_0"]
    side_e_0 = var_dict["side_e_0"]

    max_retries = 1000000
    for i in range(max_retries):
        string = f"Assume you are someone who cares about {environment}."
        string += f"Towards {topic}: \n"
        string += "You have received the following tweets:"
        string += "<<<\n" + message_list + ">>>\n"
        if profile["side"] < 0:
            string += f"You have been persuaded to {side_s_0}.\n"
        if profile["side"] > 0:
            string += f"You have been persuaded to {side_b_0}.\n"
        if profile["side"] == 0:
            string += f"You {side_e_0}.\n"

        string += "Try generate 1-3 reasons on why you are persuaded soley base on the above tweets with around 50 words."
        try:
            reasons = get_completion_1(string)
            return reasons
        except Exception:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise


def initialize_tweet(profile: dict, var_dict: dict):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]

        string = f"Assume you are someone who cares about {environment}.\n"
        if profile["side"] == -2:
            string += f"You <<<{S_m2}>>>.\n"
        if profile["side"] == -1:
            string += f"You <<<{S_m1}>>>.\n"
        if profile["side"] == 0:
            string += f"You feel <<<{S_0}>>>. \n"
        if profile["side"] == 1:
            string += f"You <<<{S_p1}>>>.\n"
        if profile["side"] == 2:
            string += f"You <<<{S_p2}>>>.\n"
        string += (
            f"Please express your opinion on {topic} with around 50 words.\n"
        )

        max_retries = 1000000
        for i in range(max_retries):
            try:

                message = get_completion_1(string)

                return message

            except Exception:
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def initialize_tweet_debias(profile: dict, var_dict: dict):
    try:
        max_retries = 1000000
        message = ""
        retry = 0
        for i in range(max_retries):
            environment = var_dict["environment"]
            topic = var_dict["topic"]
            S_m2 = var_dict["S_m2"]
            S_m1 = var_dict["S_m1"]
            S_0 = var_dict["S_0"]
            S_p1 = var_dict["S_p1"]
            S_p2 = var_dict["S_p2"]
            S_m2_e = var_dict["S_m2_e"]
            S_m1_e = var_dict["S_m1_e"]
            S_0_e = var_dict["S_0_e"]
            S_p1_e = var_dict["S_p1_e"]
            S_p2_e = var_dict["S_p2_e"]

            string = f"Assume you are someone who cares about {environment}.\n"
            string += (
                f"People are divided into 5 standpoints on {environment}:\n"
            )
            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]

            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
            if profile["side"] == -2:
                string1 = S_m2
            if profile["side"] == -1:
                string1 = S_m1
            if profile["side"] == 0:
                string1 = S_0
            if profile["side"] == 1:
                string1 = S_p1
            if profile["side"] == 2:
                string1 = S_p2
            string += f"Please generate a tweet to persuade yourself to {string1} with around 50 words.\n"

            try:

                message = get_completion_1(string)

                string = (
                    f"Assume you are someone who cares about {environment}.\n"
                )
                string += f"People are divided into 5 standpoints on {topic}:\n"
                temp_list = [
                    [S_m2, S_m2_e],
                    [S_m1, S_m1_e],
                    [S_0, S_0_e],
                    [S_p1, S_p1_e],
                    [S_p2, S_p2_e],
                ]
                for item in temp_list:
                    string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
                string += f"You have written the following message to express your opinion on {topic}:\n"
                string += "<<<" + message + ">>>\n"
                string += "Can you determine that you "
                if profile["side"] == -2:
                    string += f"<<<{S_m2}>>>\n"
                if profile["side"] == -1:
                    string += f"<<<{S_m1}>>>\n"
                if profile["side"] == 0:
                    string += f"<<<{S_0}>>>\n"
                if profile["side"] == 1:
                    string += f"<<<{S_p1}>>>\n"
                if profile["side"] == 2:
                    string += f"<<<{S_p2}>>>\n"
                string += "from the message you wrote? Please respond 'yes' or 'no' only.\n"

                yes_no = get_completion_1(string)

                if "yes" in yes_no or "Yes" in yes_no or retry >= 1000000:
                    return message
                else:
                    retry += 1

            except Exception:
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_update_profile_5_and_LLM_get_reason(
    profile: dict,
    message_list_new: str,
    message_list_old: str,
    var_dict: dict,
    style=0,
    remind=False,
):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]
        S_m2_e = var_dict["S_m2_e"]
        S_m1_e = var_dict["S_m1_e"]
        S_0_e = var_dict["S_0_e"]
        S_p1_e = var_dict["S_p1_e"]
        S_p2_e = var_dict["S_p2_e"]

        max_retries = 1000000
        for i in range(max_retries):

            string = f"Assume you are someone who cares about {environment}."
            string += f"Towards {topic}: \n"
            if profile["side"] == -2:
                string += f"You <<<{S_m2}>>>.\n"
            if profile["side"] == -1:
                string += f"You <<<{S_m1}>>>.\n"
            if profile["side"] == 0:
                string += f"You feel <<<{S_0}>>>. \n"
            if profile["side"] == 1:
                string += f"You <<<{S_p1}>>>.\n"
            if profile["side"] == 2:
                string += f"You <<<{S_p2}>>>.\n"
            string += "Your reasons were:\n"
            string += "<<<" + profile["reasons"] + ">>>\n"
            string += "You now have received the following tweets from your friends, and you have recieved some tweets:\n"
            string += "<<<" + message_list_new + ">>>\n"
            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]
            if style == 0:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to choose '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' , and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to choose '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"
            if style == 1:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}', and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"
            if style == 2:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic} become? You need to select a tendency from '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}', '{temp_list[4][0]}', and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to select a tendency from '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}', '{temp_list[4][0]}' in the first line, and explain.\n"

            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"

            if remind:
                string += "Your current tendency is: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"

            string += "Please return in json, with two keys: tendency and reasons. Please keep the reasons as short as possible."
            try:

                new_side = get_completion_1(string)

                new_side = json.loads(new_side)
                stand = ""
                if S_p2 in new_side["tendency"]:
                    stand = 2
                elif S_m2 in new_side["tendency"]:
                    stand = -2
                elif S_p1 in new_side["tendency"]:
                    stand = 1
                elif S_m1 in new_side["tendency"]:
                    stand = -1
                elif S_0 in new_side["tendency"]:
                    stand = 0
                else:
                    raise

                return {
                    "side": stand,
                    "reasons": new_side["reasons"],
                    "tendency": new_side["tendency"],
                    "new_side": string,
                }
            except Exception:
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_update_profile_5_and_LLM_get_reason_debias(
    profile: dict,
    message_list_new: str,
    message_list_old: str,
    var_dict: dict,
    style=0,
    remind=False,
):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]
        S_m2_e = var_dict["S_m2_e"]
        S_m1_e = var_dict["S_m1_e"]
        S_0_e = var_dict["S_0_e"]
        S_p1_e = var_dict["S_p1_e"]
        S_p2_e = var_dict["S_p2_e"]

        max_retries = 1000000

        retry = 0
        for i in range(max_retries):

            string = f"Assume you are someone who cares about {environment}."
            string += f"Towards {topic}: \n"
            if profile["side"] == -2:
                string += f"You <<<{S_m2}>>>.\n"
            if profile["side"] == -1:
                string += f"You <<<{S_m1}>>>.\n"
            if profile["side"] == 0:
                string += f"You feel <<<{S_0}>>>. \n"
            if profile["side"] == 1:
                string += f"You <<<{S_p1}>>>.\n"
            if profile["side"] == 2:
                string += f"You <<<{S_p2}>>>.\n"
            string += "Your reasons were:\n"
            string += "<<<" + profile["reasons"] + ">>>\n"

            string += "You now have received the following tweets from your friends, and you have recieved some tweets:\n"
            string += "<<<" + message_list_new + ">>>\n"

            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]
            if style == 0:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to choose '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' , and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to choose '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"
            if style == 1:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}', and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"
            if style == 2:
                string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic} become? You need to select a tendency from '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}', '{temp_list[4][0]}', and explain the reasons of it in around 50 words. \n"
                string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to select a tendency from '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}', '{temp_list[4][0]}' in the first line, and explain.\n"

            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"

            if remind:
                string += "Your current tendency is: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"

            stand = ""
            new_side = {
                "tendency": "",
                "reasons": "",
            }

            string += "Please return in json, with two keys: tendency and reasons. Please keep the reasons as short as possible."

            try:

                new_side = get_completion_1(string)

                new_side = json.loads(new_side)
                stand = ""
                if S_p2 in new_side["tendency"]:
                    stand = 2
                elif S_m2 in new_side["tendency"]:
                    stand = -2
                elif S_p1 in new_side["tendency"]:
                    stand = 1
                elif S_m1 in new_side["tendency"]:
                    stand = -1
                elif S_0 in new_side["tendency"]:
                    stand = 0
                else:
                    raise

                string = (
                    f"Assume you are someone who cares about {environment}."
                )
                string += f"Towards {topic}: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"
                string += "Your reasons were:\n"
                string += "<<<" + profile["reasons"] + ">>>\n"

                string += "You have received the following tweets from your friends, and you have recieved some tweets:\n"
                string += "<<<" + message_list_new + ">>>\n"
                string += (
                    "You have been persuaded to change your standpoint from "
                )
                if profile["side"] == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "to "
                if stand == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if stand == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if stand == 0:
                    string += f"<<<{S_0}>>>. \n"
                if stand == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if stand == 2:
                    string += f"<<<{S_p2}>>>.\n"

                string += "Please reconsider whether your decision is plausible and valid. Please  respond 'yes' or 'no' only."
                temp_list = [
                    [S_m2, S_m2_e],
                    [S_m1, S_m1_e],
                    [S_0, S_0_e],
                    [S_p1, S_p1_e],
                    [S_p2, S_p2_e],
                ]
                for item in temp_list:
                    string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
                confirm = get_completion_1(string)
                if "yes" in confirm or "Yes" in confirm or retry >= 2:
                    return {
                        "side": stand,
                        "reasons": new_side["reasons"],
                        "tendency": new_side["tendency"],
                        "new_side": string,
                    }
                else:
                    retry += 1
            except Exception as e:
                if i < max_retries - 1:
                    print(e)
                    time.sleep(2)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_update_profile_5_and_LLM_get_reason_debias_no_con(
    profile: dict, message_list_new: str, message_list_old: str, var_dict: dict
):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]
        S_m2_e = var_dict["S_m2_e"]
        S_m1_e = var_dict["S_m1_e"]
        S_0_e = var_dict["S_0_e"]
        S_p1_e = var_dict["S_p1_e"]
        S_p2_e = var_dict["S_p2_e"]

        max_retries = 1000000

        retry = 0
        for i in range(max_retries):

            string = f"Assume you are someone who cares about {environment}."
            string += f"Towards {topic}: \n"
            if profile["side"] == -2:
                string += f"You <<<{S_m2}>>>.\n"
            if profile["side"] == -1:
                string += f"You <<<{S_m1}>>>.\n"
            if profile["side"] == 0:
                string += f"You feel <<<{S_0}>>>. \n"
            if profile["side"] == 1:
                string += f"You <<<{S_p1}>>>.\n"
            if profile["side"] == 2:
                string += f"You <<<{S_p2}>>>.\n"
            string += "Your reasons were:\n"
            string += "<<<" + profile["reasons"] + ">>>\n"

            string += "You now have received the following tweets from your friends, and you have recieved some tweets:\n"
            string += "<<<" + message_list_new + ">>>\n"

            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]
            string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' , and explain the reasons of it in around 50 words. \n"
            string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"
            string += "You DO NOT have confirmation bias, that means you are open-minded to persuasion of diverse opinions.\n"
            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"

            stand = ""
            new_side = {
                "tendency": "",
                "reasons": "",
            }

            string += "Please return in json, with two keys: tendency and reasons. Please keep the reasons as short as possible."
            try:
                new_side = get_completion_1(string)
                new_side = json.loads(new_side)
                stand = ""
                if S_p2 in new_side["tendency"]:
                    stand = 2
                elif S_m2 in new_side["tendency"]:
                    stand = -2
                elif S_p1 in new_side["tendency"]:
                    stand = 1
                elif S_m1 in new_side["tendency"]:
                    stand = -1
                elif S_0 in new_side["tendency"]:
                    stand = 0
                else:
                    raise

                string = (
                    f"Assume you are someone who cares about {environment}."
                )
                string += f"Towards {topic}: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"
                string += "Your reasons were:\n"
                string += "<<<" + profile["reasons"] + ">>>\n"

                string += "You have received the following tweets from your friends, and you have recieved some tweets:\n"
                string += "<<<" + message_list_new + ">>>\n"
                string += (
                    "You have been persuaded to change your standpoint from "
                )
                if profile["side"] == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "to "
                if stand == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if stand == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if stand == 0:
                    string += f"<<<{S_0}>>>. \n"
                if stand == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if stand == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "Please reconsider whether your decision is plausible and valid. Please  respond 'yes' or 'no' only."
                temp_list = [
                    [S_m2, S_m2_e],
                    [S_m1, S_m1_e],
                    [S_0, S_0_e],
                    [S_p1, S_p1_e],
                    [S_p2, S_p2_e],
                ]
                for item in temp_list:
                    string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
                confirm = get_completion_1(string)
                if "yes" in confirm or "Yes" in confirm or retry >= 2:
                    return {
                        "side": stand,
                        "reasons": new_side["reasons"],
                        "tendency": new_side["tendency"],
                        "new_side": string,
                    }
                else:
                    retry += 1
            except Exception as e:
                if i < max_retries - 1:
                    print(e)
                    time.sleep(2)

                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_update_profile_5_and_LLM_get_reason_debias_con(
    profile: dict, message_list_new: str, message_list_old: str, var_dict: dict
):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]
        S_m2_e = var_dict["S_m2_e"]
        S_m1_e = var_dict["S_m1_e"]
        S_0_e = var_dict["S_0_e"]
        S_p1_e = var_dict["S_p1_e"]
        S_p2_e = var_dict["S_p2_e"]

        max_retries = 1000000

        retry = 0
        for i in range(max_retries):

            string = f"Assume you are someone who cares about {environment}."
            string += f"Towards {topic}: \n"
            if profile["side"] == -2:
                string += f"You <<<{S_m2}>>>.\n"
            if profile["side"] == -1:
                string += f"You <<<{S_m1}>>>.\n"
            if profile["side"] == 0:
                string += f"You feel <<<{S_0}>>>. \n"
            if profile["side"] == 1:
                string += f"You <<<{S_p1}>>>.\n"
            if profile["side"] == 2:
                string += f"You <<<{S_p2}>>>.\n"
            string += "Your reasons were:\n"
            string += "<<<" + profile["reasons"] + ">>>\n"

            string += "You now have received the following tweets from your friends, and you have recieved some tweets:\n"
            if profile["det"]:
                string += "You have confirmation bias, showing a tendency to favor information that confirms your existing beliefs and to interpret new evidence in a way that aligns with those beliefs."
            string += "<<<" + message_list_new + ">>>\n"
            string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to answer '{S_m2}', '{S_m1}', '{S_0}', '{S_p1}', or '{S_p2}', and explain the reasons of it in around 50 words. \n"
            string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to answer '{S_m2}', '{S_m1}', '{S_0}', '{S_p1}', or '{S_p2}' in the first line, and explain.\n"
            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]
            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
            stand = ""
            new_side = {
                "tendency": "",
                "reasons": "",
            }

            string += "Please return in json, with two keys: tendency and reasons. Please keep the reasons as short as possible."
            try:
                new_side = get_completion_1(string)
                new_side = json.loads(new_side)
                stand = ""
                if S_p2 in new_side["tendency"]:
                    stand = 2
                elif S_m2 in new_side["tendency"]:
                    stand = -2
                elif S_p1 in new_side["tendency"]:
                    stand = 1
                elif S_m1 in new_side["tendency"]:
                    stand = -1
                elif S_0 in new_side["tendency"]:
                    stand = 0
                else:
                    raise

                string = (
                    f"Assume you are someone who cares about {environment}."
                )
                string += f"Towards {topic}: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"
                string += "Your reasons were:\n"
                string += "<<<" + profile["reasons"] + ">>>\n"

                string += "You have received the following tweets from your friends, and you have recieved some tweets:\n"
                string += "<<<" + message_list_new + ">>>\n"
                string += (
                    "You have been persuaded to change your standpoint from "
                )
                if profile["side"] == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"<<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "to "
                if stand == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if stand == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if stand == 0:
                    string += f"<<<{S_0}>>>. \n"
                if stand == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if stand == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "Please reconsider whether your decision is plausible and valid. Please  respond 'yes' or 'no' only."
                temp_list = [
                    [S_m2, S_m2_e],
                    [S_m1, S_m1_e],
                    [S_0, S_0_e],
                    [S_p1, S_p1_e],
                    [S_p2, S_p2_e],
                ]
                for item in temp_list:
                    string += f"<<<{item[0]}>>> means you think {item[1]}.\n"
                confirm = get_completion_1(string)
                if "yes" in confirm or "Yes" in confirm or retry >= 2:
                    return {
                        "side": stand,
                        "reasons": new_side["reasons"],
                        "tendency": new_side["tendency"],
                        "new_side": string,
                    }
                else:
                    retry += 1
            except Exception as e:
                if i < max_retries - 1:
                    time.sleep(2)
                    print(e)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_update_profile_5_and_LLM_get_reason_debias_initialize(
    profile: dict, message_list_new: str, message_list_old: str, var_dict: dict
):
    try:
        environment = var_dict["environment"]
        topic = var_dict["topic"]
        S_m2 = var_dict["S_m2"]
        S_m1 = var_dict["S_m1"]
        S_0 = var_dict["S_0"]
        S_p1 = var_dict["S_p1"]
        S_p2 = var_dict["S_p2"]
        S_m2_e = var_dict["S_m2_e"]
        S_m1_e = var_dict["S_m1_e"]
        S_0_e = var_dict["S_0_e"]
        S_p1_e = var_dict["S_p1_e"]
        S_p2_e = var_dict["S_p2_e"]

        max_retries = 1000000

        retry = 0
        for i in range(max_retries):

            string = f"Assume you are someone who cares about {environment}."
            string += f"Towards {topic}: \n"
            if profile["side"] == -2:
                string += f"You <<<{S_m2}>>>.\n"
            if profile["side"] == -1:
                string += f"You <<<{S_m1}>>>.\n"
            if profile["side"] == 0:
                string += f"You feel <<<{S_0}>>>. \n"
            if profile["side"] == 1:
                string += f"You <<<{S_p1}>>>.\n"
            if profile["side"] == 2:
                string += f"You <<<{S_p2}>>>.\n"
            string += "Your reasons were:\n"
            string += "<<<" + profile["reasons"] + ">>>\n"

            string += "You now have received the following tweets from your friends, and you have recieved some tweets:\n"
            string += "<<<" + message_list_new + ">>>\n"
            temp_list = [
                [S_m2, S_m2_e],
                [S_m1, S_m1_e],
                [S_0, S_0_e],
                [S_p1, S_p1_e],
                [S_p2, S_p2_e],
            ]
            string += f"Have you been persuaded to decide your tendency, what would your feeling about {topic}? You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}', and explain the reasons of it in around 50 words. \n"
            string += f"Please choose your standpoint on {topic} base on the INFORMATION PROVIDED ABOVE. You need to answer '{temp_list[0][0]}', '{temp_list[1][0]}', '{temp_list[2][0]}', '{temp_list[3][0]}' or '{temp_list[4][0]}' in the first line, and explain.\n"

            for item in temp_list:
                string += f"<<<{item[0]}>>> means you think {item[1]}.\n"

            stand = ""
            new_side = {
                "tendency": "",
                "reasons": "",
            }

            string += "Please return in json, with two keys: tendency and reasons. Please keep the reasons as short as possible."
            try:
                new_side = get_completion_1(string)
                new_side = json.loads(new_side)
                stand = ""
                if S_p2 in new_side["tendency"]:
                    stand = 2
                elif S_m2 in new_side["tendency"]:
                    stand = -2
                elif S_p1 in new_side["tendency"]:
                    stand = 1
                elif S_m1 in new_side["tendency"]:
                    stand = -1
                elif S_0 in new_side["tendency"]:
                    stand = 0
                else:
                    raise

                string = (
                    f"Assume you are someone who cares about {environment}."
                )
                string += f"Towards {topic}: \n"
                if profile["side"] == -2:
                    string += f"You <<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"You <<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"You feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"You <<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"You <<<{S_p2}>>>.\n"
                string += "Your reasons were:\n"
                string += "<<<" + profile["reasons"] + ">>>\n"

                string += "You have received the following tweets from your friends, and you have recieved some tweets:\n"
                string += "<<<" + message_list_new + ">>>\n"
                string += (
                    "You have been persuaded to change your standpoint from "
                )
                if profile["side"] == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if profile["side"] == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if profile["side"] == 0:
                    string += f"feel <<<{S_0}>>>. \n"
                if profile["side"] == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if profile["side"] == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "to "
                if stand == -2:
                    string += f"<<<{S_m2}>>>.\n"
                if stand == -1:
                    string += f"<<<{S_m1}>>>.\n"
                if stand == 0:
                    string += f"<<<{S_0}>>>. \n"
                if stand == 1:
                    string += f"<<<{S_p1}>>>.\n"
                if stand == 2:
                    string += f"<<<{S_p2}>>>.\n"
                string += "Please reconsider whether your decision is plausible and valid. Please respond 'yes' or 'no' only."
                temp_list = [
                    [S_m2, S_m2_e],
                    [S_m1, S_m1_e],
                    [S_0, S_0_e],
                    [S_p1, S_p1_e],
                    [S_p2, S_p2_e],
                ]
                for item in temp_list:
                    string += f"<<<{item[0]}>>> means you think {item[1]}.\n"

                confirm = get_completion_1(string)
                if "yes" in confirm or "Yes" in confirm or retry >= 100000:
                    return {
                        "side": stand,
                        "reasons": new_side["reasons"],
                        "tendency": new_side["tendency"],
                        "new_side": string,
                    }
                else:
                    retry += 1
            except Exception as e:
                if i < max_retries - 1:
                    time.sleep(2)
                    print(e)
                else:
                    raise
    except Exception as e:
        print(e)
        pass


def LLM_reconnect(user: dict, target: dict, var_dict: dict):
    max_retries = 1000000
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    S_m2 = var_dict["S_m2"]
    S_m1 = var_dict["S_m1"]
    S_0 = var_dict["S_0"]
    S_p1 = var_dict["S_p1"]
    S_p2 = var_dict["S_p2"]

    for i in range(max_retries):
        string = f"Assume you are someone who cares about {environment}."
        string += f"You are now discussing {topic} with a person you know.\n"
        if user["side"] == -2:
            string += f"You {S_m2}.\n"
        if user["side"] == -1:
            string += f"You {S_m1}.\n"
        if user["side"] == 0:
            string += f"You {S_0}.\n"
        if user["side"] == 1:
            string += f"You {S_p1}.\n"
        if user["side"] == 2:
            string += f"You {S_p2}.\n"
        string += "Your thought is: <<<" + user["reasons"] + ">>> \n"
        if target["side"] == -2:
            string += f"The person {S_m2}.\n"
        if target["side"] == -1:
            string += f"The person {S_m1}.\n"
        if target["side"] == 0:
            string += f"The person {S_0}.\n"
        if target["side"] == 1:
            string += f"The person {S_p1}.\n"
        if target["side"] == 2:
            string += f"The person {S_p2}.\n"
        if target["reasons"]:
            string += (
                "The thought of that person you are discussing with is: <<<"
                + target["reasons"]
                + ">>>\n"
            )
        else:
            string += f"The person knows nothing about {environment}.\n"
        if user["patience"] == 1:
            string += "You enjoy discussing with anyone.\n"
        if user["patience"] == 0:
            string += f"You enjoy sharing with people that have reasonable thoughts about {environment}.\n"
        if user["patience"] == -1:
            string += "You do not enjoy talking with people with.\n"

        string += (
            "Would you enjoy continue sharing your thought with that person?\n"
        )
        string += "Please return 'yes' or 'no', and explain.\n"
        string += "Please return in json with 2 keys: decision and explain.\n"

        try:
            stand = get_completion_1(string)
            stand = json.loads(stand)
            if "yes" in stand["decision"] or "Yes" in stand["decision"]:
                return True, stand["explain"]
            elif "no" in stand["decision"] or "No" in stand["decision"]:
                return False, stand["explain"]
            else:
                raise

        except Exception:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise


def LLM_reconnect_noex(user: dict, target: dict, var_dict: dict):
    max_retries = 1000000
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    S_m2 = var_dict["S_m2"]
    S_m1 = var_dict["S_m1"]
    S_0 = var_dict["S_0"]
    S_p1 = var_dict["S_p1"]
    S_p2 = var_dict["S_p2"]

    for i in range(max_retries):
        string = f"Assume you are someone who cares about {environment}."
        string += f"You are now discussing {topic} with a person you know.\n"
        if user["side"] == -2:
            string += f"You {S_m2}.\n"
        if user["side"] == -1:
            string += f"You {S_m1}.\n"
        if user["side"] == 0:
            string += f"You {S_0}.\n"
        if user["side"] == 1:
            string += f"You {S_p1}.\n"
        if user["side"] == 2:
            string += f"You {S_p2}.\n"
        string += "Your thought is: <<<" + user["reasons"] + ">>> \n"
        if target["side"] == -2:
            string += f"The person {S_m2}.\n"
        if target["side"] == -1:
            string += f"The person {S_m1}.\n"
        if target["side"] == 0:
            string += f"The person {S_0}.\n"
        if target["side"] == 1:
            string += f"The person {S_p1}.\n"
        if target["side"] == 2:
            string += f"The person {S_p2}.\n"
        if target["reasons"]:
            string += (
                "The thought of that person you are discussing with is: <<<"
                + target["reasons"]
                + ">>>\n"
            )
        else:
            string += f"The person knows nothing about {environment}.\n"
        if user["patience"] == 1:
            string += "You enjoy discussing with anyone.\n"
        if user["patience"] == 0:
            string += f"You enjoy sharing with people that have reasonable thoughts about {environment}.\n"
        if user["patience"] == -1:
            string += "You do not enjoy talking with people with.\n"

        string += (
            "Would you enjoy continue sharing your thought with that person?\n"
        )
        string += "Please return 'yes' or 'no', and explain.\n"
        string += "Please return in json with 2 keys: decision and explain.\n"
        string += "You DO NOT have selective exposure, which means you like to communicate with people holding diverse opinions.\n"

        try:
            stand = get_completion_1(string)
            stand = json.loads(stand)
            if "yes" in stand["decision"] or "Yes" in stand["decision"]:
                return True, stand["explain"]
            elif "no" in stand["decision"] or "No" in stand["decision"]:
                return False, stand["explain"]
            else:
                raise
        except Exception:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise


def LLM_persuade_100(profile: dict, target_profile: dict, var_dict: dict):
    max_retries = 1000000
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    S_m2 = var_dict["S_m2"]
    S_m1 = var_dict["S_m1"]
    S_0 = var_dict["S_0"]
    S_p1 = var_dict["S_p1"]
    S_p2 = var_dict["S_p2"]
    max_retries = 1000000
    for i in range(max_retries):
        try:
            string = f"Assume you are someone who cares about {environment}."
            string += (
                f"You are now discussing {topic} with a person you know.\n"
            )
            if profile["side"] == -2:
                string += f"You {S_m2}.\n"
            if profile["side"] == -1:
                string += f"You {S_m1}.\n"
            if profile["side"] == 0:
                string += f"You {S_0}.\n"
            if profile["side"] == 1:
                string += f"You {S_p1}.\n"
            if profile["side"] == 2:
                string += f"You {S_p2}.\n"
            string += (
                f"Your thought about {topic} are: <<<"
                + profile["reasons"]
                + ">>>\n"
            )
            string += "You want to interact with or persuade a friend of yours to support your thought, that has the following thought:\n"
            string += "<<<" + target_profile["reasons"] + ">>>\n"
            string += "Please generate a message to persuade your friend into supporting your perspective with around 50 words.\n"
            message = get_completion_1(string)
            return message

        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2)
                print(e)
            else:
                raise


def LLM_persuade_100_debias(
    profile: dict, target_profile: dict, var_dict: dict
):
    max_retries = 1000000
    environment = var_dict["environment"]
    topic = var_dict["topic"]
    S_m2 = var_dict["S_m2"]
    S_m1 = var_dict["S_m1"]
    S_0 = var_dict["S_0"]
    S_p1 = var_dict["S_p1"]
    S_p2 = var_dict["S_p2"]
    max_retries = 1000000
    retry = 0
    message = ""
    for i in range(max_retries):
        try:
            string = f"Assume you are someone who cares about {environment}."
            string += (
                f"You are now discussing {topic} with a person you know.\n"
            )
            if profile["side"] == -2:
                string += f"You {S_m2}.\n"
            if profile["side"] == -1:
                string += f"You {S_m1}.\n"
            if profile["side"] == 0:
                string += f"You {S_0}.\n"
            if profile["side"] == 1:
                string += f"You {S_p1}.\n"
            if profile["side"] == 2:
                string += f"You {S_p2}.\n"
            string += (
                f"Your thought about {topic} are: <<<"
                + profile["reasons"]
                + ">>>\n"
            )
            string += "You want to interact with or persuade a friend of yours to support your thought, that has the following thought:\n"
            string += "<<<" + target_profile["reasons"] + ">>>\n"
            string += "Please generate a message to persuade your friend into supporting your perspective with around 50 words.\n"

            message = get_completion_1(string)
            string = (
                "You tried to persuade your friend with the following message: <<<"
                + message
                + ">>>\n"
            )

            string += "Do you find the message persuasive enough to persuade your friend to:"
            if profile["side"] == -2:
                string += f"<<<{S_m2}>>>"
            if profile["side"] == -1:
                string += f"<<<{S_m1}>>>"
            if profile["side"] == 0:
                string += f"<<<{S_0}>>>"
            if profile["side"] == 1:
                string += f"<<<{S_p1}>>>"
            if profile["side"] == 2:
                string += f"<<<{S_p2}>>>"
            string += "? Please respond yes or no only.\n"
            persuasive = get_completion_1(string)
            if "yes" in persuasive or "Yes" in persuasive or retry >= 10:
                return message
            retry += 1
        except Exception:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise


def handle_user_side(user):
    user.update_profile()
    return user


def handle_user_tweet(user, target):
    message = user.persuade(target)
    if "no" in message["will"]:
        return ["no", user, target]
    else:
        return [message["message"], user, target]


def handle_user_reconnect(user, target):

    yes_or_no, explain = LLM_reconnect(
        user.profile, target.profile, user.var_dict
    )
    return [yes_or_no, user, target, explain]


def handle_user_reconnect_noex(user, target):

    yes_or_no, explain = LLM_reconnect_noex(
        user.profile, target.profile, user.var_dict
    )
    return [yes_or_no, user, target, explain]


def handle_user_reconnect_cut(user, target):
    return [False, user, target, "yes"]


def handle_user_reconnect_retian(user, target):
    return [True, user, target, "yes"]
