from hashlib import sha1
import string

def make_sha1(s, encoding='utf-8'):
    return sha1(s.encode(encoding)).hexdigest()


print(make_sha1("kaka"))
print(make_sha1("kaka")[0:4])
charset = string.printable
for c1 in charset:
    for c2 in charset:
        for c3 in charset:
            print("Trying: ", c1+c2+c3)
            if make_sha1(c1+c2+c3)[0:4] == "7c00":
                print(c1+c2+c3)
                exit()