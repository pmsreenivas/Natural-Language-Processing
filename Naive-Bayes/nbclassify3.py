import sys
import os
import math

def main():
    directory = str(sys.argv[1])
    dev_files = set()
    for dirpath, dirnames, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(dirpath, file)
            if file.endswith('.txt'):
                dev_files.add(file_path)
    f = open("nbmodel.txt", "r", encoding="latin1")
    p_spam = 0
    p_ham = 0
    token_probs = dict()
    for line in f:
        line.strip('\n')
        word_list = line.split()
        if len(word_list) == 0:
            break
        elif word_list[0] == "PROBABILITIES":
            p_ham = float(word_list[1])
            p_spam = float(word_list[2])
        else:
            token_probs[word_list[0]] = [float(word_list[1]), float(word_list[2])]
    #print(token_probs)
    f = open("nboutput.txt", "w")
    newline = ""
    for file in dev_files:
        f2 = open(file, "r", encoding="latin1")
        sum_ham = math.log(p_ham)
        sum_spam = math.log(p_spam)
        for line in f2:
            line = line.strip('\n')
            word_list = line.split()
            for token in word_list:
                if token.lower() in token_probs:
                    sum_ham += math.log(token_probs.get(token.lower())[0])
                    sum_spam += math.log(token_probs.get(token.lower())[1])
                elif any(c.isdigit() for c in token.lower()) == True:
                    sum_ham += math.log(token_probs.get("--number--")[0])
                    sum_spam += math.log(token_probs.get("--number--")[1])
        if sum_ham > sum_spam:
            f.write(f"{newline}ham\t{file}")
        else:
            f.write(f"{newline}spam\t{file}")
        newline = "\n"
        f2.close()
    f.close()
if __name__ == "__main__":
    main()