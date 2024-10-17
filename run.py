import os

environment = "Sociopolitical"
topic = "Politics"
S_m2 = "strongly support the Republican party"
S_m1 = "support the Republican party"
S_0 = "don't have a tendency"
S_p1 = "support the Democratic party"
S_p2 = "Strongly support the Democratic party"
S_m2_e = "the Republic party is absolutely better than the Democratic party in every aspect."
S_m1_e = "the Republican party and the Democratic party both have ups and downs, but the Republican party have a slight edge."
S_0_e = "doesn't lean towards or favor either the Democratic or Republican party."
S_p1_e = "the Democratic party and the Republican party both have ups and downs, but the Democratic party have a slight edge."
S_p2_e = "the Democratic party is absolutely better than the Republican party in every aspect."
side_s_0 = "Support the Republican party"
side_e_0 = "Maintain neutrality"
side_b_0 = "Support the Democratic party"

datasource = "Data_WS_2000"
num_epoch = 2000
starting_epoch = 0
side_init = "0.1,0.2,0.4,0.2,0.1"

abb = "Politics"
cmd = f"""python simulate_debiased.py "{environment}" "{topic}" "{S_m2}" "{S_m1}" "{S_0}" "{S_p1}" "{S_p2}" "{S_m2_e}" "{S_m1_e}" "{S_0_e}" "{S_p1_e}" "{S_p2_e}" "{side_b_0}" "{side_s_0}" "{side_e_0}" "{datasource}" "{num_epoch}" "{side_init}" "{abb}" "{starting_epoch}" """
os.system(cmd)
