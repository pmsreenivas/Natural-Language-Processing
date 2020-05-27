f = open("accuracy_apple_carrot.txt", "r")

corr = 0
wro = 0
tot = 0

for line in f:
    if line.split():
        a,b = line.split()
        if not a == b:
            wro += 1
        else:
            corr += 1
        tot += 1

print(corr/tot)
print(wro/tot)

f.close()