import pickle
import operator
import numpy as np
import matplotlib.pyplot as plt

with open('to_1_hot.pickle', 'rb') as handle:
    to_1_hot = pickle.load(handle)

print(to_1_hot)

hot_1_list = [(k, v) for k, v in to_1_hot.items()]
print(hot_1_list)

hot_1_list.sort(key=lambda x: x[1], reverse=True)

# save the names and their respective scores separately
# reverse the tuples to go from most frequent to least frequent
name = list(zip(*hot_1_list))[0]
score = list(zip(*hot_1_list))[1]
x_pos = np.arange(len(name))

# calculate slope and intercept for the linear trend line

plt.figure(figsize=(30, 30))

plt.bar(x_pos, score, align='center')
plt.xticks(x_pos, name)
plt.xticks(rotation=90)

plt.ylabel('Frequency')
plt.savefig('figures/freq.jpeg')

plt.show()


