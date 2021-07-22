p = [0]*6

def gen():
    p[5] = 145 - p[3]
    p[4] = p[3] ^ 71
    p[2] = p[3] ^ 9
    p[1] = p[2] ^ 43
    p[0] = p[1] ^ 49

def check():
    if sum(p) != 502:
        return False
    for i in p:
        if i<=0 or i>=128:
            return False
    return True

for p[3] in range(32, 128):
    gen()
    if (check()):
        for i in p:
            print(i)