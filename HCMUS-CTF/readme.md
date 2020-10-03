# HCMUS-CTF 2020 write ups
## Web Exploitation
### BonAppetit
Đọc cookie để được flag
### Quelcome
Biết được đây là graphQL, enum qua các document bằng {__schema{}}
### Math
Truy cập vào trang web, ta thấy web cho 1 dãy các phép tính, và ta cần tìm ra kết quả của phép tính có độ dài dài nhất trong số đó. 
Tuy nhiên các phép tính lại được bọc giữa các chuỗi làm nhiễu như `"Calculate them", "hurry up!", "awww"`, nên cần filter chúng trước.  
``` python
for equation in equations:
		for data in filterData:
			equation = equation.replace(data, '')
		realEquations.append(equation)
```
sau đó tìm chuỗi dài nhất và tính nó
``` python
maxI = 0
maxLength = 0
for i in range(0, len(realEquations)):
    if len(realEquations[i]) > maxLength:
        maxLength = len(realEquations[i])
        maxI = i
result = eval(realEquations[maxI])
```
Full script exploit nằm ở ./Math/exploit.py  
**Flag: HCMUS-CTF{1+2_3_32_1_H0w_d0_u_4Ut0?}**
## Programming
### Pluzz
Lấy giá trị bên file a cộng lần lượt với giá trị bên file b, sau đó chuyển về acsii
### Email
Làm theo yêu cầu  
### Bruce Lee
Netcat vào server, thử nhập HCMUS-CTF vào, ta được dãy 9 số 1, tương ứng với 9 chữ cái đúng.
Bruce force lần lượt từng ký tự để được flag
## OSINT
### Resume
Dùng John the Ripper để tìm ra pass của file nén. Ta được file pdf là resume của anh Tran-Thanh-Hung  
Tìm linkedin và tra contact info, ta được email ```glutamo_team_ctf_funny@yahoo.com```  
**Flag: HCMUS-CTF{glutamo_team_ctf_funny@yahoo.com}**
### Email
Giải nén ra, ta được các file .eml.  
Dùng vscode để đọc các file đó, ta thấy các email này còn đính kèm các file khác. Dùng tools để đưa từ base64 sang file, kết hợp đọc MIME của file, ta được file docx và file .xlxs. Xem thông tin của file word ta thấy được comment ```HCMUS-CTF{metadata}```  
**Flag: HCMUS-CTF{metadata}**

## Forensics
### OutdatedBrowser
Down file `main.js` về, tạo 1 trang index.html
``` html
<html>
    <script src="main.js"></script>
</html>>
```
Mở lên bằng Internet Explorer, sau đó bấm F12 và chuyển sang tab console.  
Chạy đoạn script sau
``` javascript
var stm = base64ToStream(serialized_obj);
var fmt = new ActiveXObject('System.Runtime.Serialization.Formatters.Binary.BinaryFormatter');
var al = new ActiveXObject('System.Collections.ArrayList');
var d = fmt.Deserialize_2(stm);
al.Add(undefined);
console.log(d.DynamicInvoke(al.ToArray()).FullName);
```
**Flag: HCMUS-CTF{Example-Assembly-from-Glutamo-Team}**
### OooCooRoo
Dùng tools OCR để scan ảnh sau đó decode hex, từ ảnh 2 ta được chuỗi hex `48434D55532D4354467B596F755F6B6E6F775F61626F75745F4F43525F796F755F616E6F746865725F6F6E655F776974685F4E4C507D`  
Decode hex tiếp ta được flag  
**Flag: HCMUS-CTF{You_know_about_OCR_you_another_one_with_NLP}**

## Cryptography
### Aliens
Dùng The Standard Galactic để giải mã
### Log1
Dùng thuật toán Pohlic-Hellman để tìm x
### Log2
Dùng thuật toán Pohlic-Hellman để tìm x2

## Forensics
### RecoverMe
Dùng tools R-Studio để recover lại dữ liệu từ file .img  
Ta được đoạn đầu của flag bằng tools deep sound
Đoạn thử 2 bằng cách chạy file binary
Đoạn thử 3 bằng cách đọc file excel
Đoạn thử 4 bằng cách đọc binary của file ảnh shhhh