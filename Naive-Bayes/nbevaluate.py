import sys
import os
import math

def main():
    file = str(sys.argv[1])
    f = open(file, "r")
    ccah = 0
    ccas = 0
    cas = 0
    cah = 0
    bts = 0
    bth = 0
    for line in f:
        line.strip('\n')
        word_list = line.split('\t')
        label = word_list[0]
        if "spam" in word_list[1]:
            actual = "spam"
        elif "ham" in word_list[1]:
            actual = "ham"
        else:
            continue
        if label == "spam" and actual == "spam":
            ccas += 1
            cas += 1
            bts += 1
        elif label == "ham" and actual == "spam":
            cah += 1
            bts += 1
        elif label == "ham" and actual == "ham":
            ccah += 1
            cah += 1
            bth += 1
        elif label == "spam" and actual == "ham":
            cas += 1
            bth += 1
    f.close()
    p_spam = ccas/cas
    p_ham = ccah/cah
    r_spam = ccas/bts
    r_ham = ccah/bth
    f1_spam = (2 * p_spam * r_spam)/(p_spam + r_spam)
    f1_ham = (2 * p_ham * r_ham)/(p_ham + r_ham)
    print(f"Precision of spam is {p_spam}")
    print(f"Recall of spam is {r_spam}")
    print(f"F1 score of spam is {f1_spam}")
    print(f"Precision of ham is {p_ham}")
    print(f"Recall of ham is {r_ham}")
    print(f"F1 score of ham is {f1_ham}")



if __name__ == "__main__":
    main()