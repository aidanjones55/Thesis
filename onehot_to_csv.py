import pickle
import pandas as pd
import operator
import numpy as np
import matplotlib.pyplot as plt
from util import one_hot_translate

with open('to_1_hot.pickle', 'rb') as handle:
    to_1_hot = pickle.load(handle)

tuple_list = [k + (v,) for k, v in to_1_hot.items()]
tuple_list.sort(key=lambda x: x[4], reverse=True)


for i, x in enumerate(tuple_list):
    tuple_list[i] = (str(x[0]), str(x[1]), str(x[2]), str(int(x[3])), x[4])


#df = pd.DataFrame(tuple_list, columns =['PrimaryAction', 'SecondaryAction', 'ActionResult', 'ScoreResult', 'Size'])
#df.to_csv('onehot_master.csv')

final_encoding = {}

for ent in tuple_list:
    if not one_hot_translate[(ent[0], ent[1], ent[2], ent[3])] in final_encoding.keys():
        final_encoding[one_hot_translate[(ent[0], ent[1], ent[2], ent[3])]] = ent[4]
    else:
        final_encoding[one_hot_translate[(ent[0], ent[1], ent[2], ent[3])]] += ent[4]

with open('final_encoding.pickle', 'wb') as handle:
    pickle.dump(final_encoding, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(sum(final_encoding.values()))
print(len(final_encoding))


