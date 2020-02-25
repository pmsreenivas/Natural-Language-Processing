import sys
import os


def main():
    #print(len(sys.argv))
    directory = str(sys.argv[1])
    #print(directory)
    spam_files = set()
    ham_files = set()
    for dirpath, dirnames, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(dirpath, file)
                if "spam" in file:
                    spam_files.add(file_path)
                elif "ham" in file:
                    ham_files.add(file_path)
                    #print(file_path)
    #print(len(spam_files))
    #print(len(ham_files))
    num_spam_files = len(spam_files)
    num_ham_files = len(ham_files)
    num_total_files  =  num_spam_files + num_ham_files
    num_needed = int(0.1 * num_total_files)
    num_spam_needed = int(0.5  * num_needed)
    num_ham_needed = int(0.5 * num_needed)
    num_spam_left = num_spam_needed
    num_ham_left  =  num_ham_needed
    spam_tokens = dict()
    ham_tokens = dict()
    all_tokens = dict()
    num_spam_tokens = 0
    num_ham_tokens = 0
    for file in spam_files:
        f = open(file, "r", encoding="latin1")
        for line in f:
            line.strip('\n')
            word_list = line.split()
            for token in word_list:
                spam_tokens[token.lower()] = spam_tokens.get(token.lower(), 0) + 1
                all_tokens[token.lower()] = all_tokens.get(token.lower(), 0) + 1
                num_spam_tokens += 1
        f.close()
        num_spam_left -= 1
        if num_spam_left == 0:
            break
    num_ham_left += num_spam_left
    for file in ham_files:
        f = open(file, "r", encoding="latin1")
        for line in f:
            line.strip('\n')
            word_list = line.split()
            for token in word_list:
                ham_tokens[token.lower()] = ham_tokens.get(token.lower(), 0) + 1
                all_tokens[token.lower()] = all_tokens.get(token.lower(), 0) + 1
                num_ham_tokens += 1
        f.close()
        num_ham_left -= 1
        if num_ham_left == 0:
            break
    #num_spam_tokens = len(spam_tokens)
    #num_ham_tokens = len(ham_tokens)
    num_tokens = len(all_tokens)
    f = open("nbmodel.txt", "w", encoding="latin1")
    f.write(f"PROBABILITIES {(num_ham_files)/(num_ham_files + num_spam_files)} {(num_spam_files)/(num_ham_files + num_spam_files)}\n")
    for token in all_tokens.keys():
        f.write(f"{token} {(1 + ham_tokens.get(token, 0))/(num_tokens + num_ham_tokens)} {(1 + spam_tokens.get(token, 0))/(num_tokens + num_spam_tokens)}\n")
    f.close()
    #print(ham_tokens)
    #print(len(spam_tokens))
    #print(len(ham_tokens))

if __name__ == "__main__":
    main()
