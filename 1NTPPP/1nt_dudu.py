from os import sys, path

sys.path.append("/home/eduucaldas/GitHub/AlphaBridge")
from Pickle_Data.extract_data import load_file, BridgeDeal
import auxiliary_functions.encode_and_parsing as eap
import numpy as np
import matplotlib.pyplot as plt

filename = "Search.bin"
data = load_file(filename)
# TODO Big problem, hand is not in the order of lead
leads = [data[i].lead.upper() for i in range(len(data))]
hands = [data[i].hands[0] for i in range(len(data))]

bugged_id = []
for i in range(1000, len(data)):
    if not eap.is_card_in_hand(data[i].hands[0], data[i].lead.upper()):
        bugged_id.append(i)
print(len(bugged_id))
for i in range(len(bugged_id)):
    print(data[bugged_id[i]].leader)

print(data[bugged_id[0]].hands)
print(np.roll(data[bugged_id[0]].hands, 2))

for i in range(len(bugged_id)):
    if data[bugged_id[i]].leader == 0:
        print("aha")
length = len(data)

# S = 0, H = 1, D = 2, C = 3
suits_lead = []
for i in range(length):
    if leads[i][0] == 'S':
        suits_lead.append(0)
    if leads[i][0] == 'H':
        suits_lead.append(1)
    if leads[i][0] == 'D':
        suits_lead.append(2)
    if leads[i][0] == 'C':
        suits_lead.append(3)

plt.hist(suits_lead, bins=[0, 1, 2, 3, 4])
plt.xticks([0.5, 1.5, 2.5, 3.5], ['Spade', 'Heart', 'Diamond', 'Club'])
plt.ylabel('Number of boards where the suit is lead')
plt.xlabel('Suits')
plt.plot()
plt.show()

number_of_cardes = np.zeros((length, 4), int)


for i in range(length):
    number_of_cardes[i][0] = sum(hands[i][0:13])
    number_of_cardes[i][1] = sum(hands[i][13:26])
    number_of_cardes[i][2] = sum(hands[i][26:39])
    number_of_cardes[i][3] = sum(hands[i][39:52])

best_suit = []
for i in range(length):
    best_suit.append(np.argmax(number_of_cardes[i]))

a = np.array(best_suit)
print(len(a))
b = np.array(suits_lead)
print(len(b))
print(1.0 * np.count_nonzero(a == b) / length)

#
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.svm import SVC
# from sklearn.model_selection import cross_val_score
#
# classifier = OneVsRestClassifier(SVC(random_state=0))
# classifier_scoring = cross_val_score(classifier, hands, suits_lead, scoring='accuracy', cv=5)
# print('OneVsRest Classifier')
# print('Accuracy scores: ', classifier_scoring)
# print('mean: {}, max: {}, min: {}, std: {}'.format(classifier_scoring.mean(), classifier_scoring.max(),
#                                                    classifier_scoring.min(), classifier_scoring.std()))
