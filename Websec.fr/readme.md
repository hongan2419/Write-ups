# WEBSEC.FR WRITE UP
## Level01
Basic SQL injection  
`0 union select id, password from users`  
**Flag: WEBSEC{Simple_SQLite_Injection}**
## Level02
Tương tự như `Natas25`, ta thấy nếu ta có chuỗi `selecselectt` thì sau hàm `preg_replace` ta sẽ được chuỗi `select`  
`0 uniounionn selecselectt id, password frofromm users`  
**Flag: WEBSEC{BecauseBlacklistsAreOftenAgoodIdea}**
## Level03
Ta thấy lệnh `sha1($flag, fa1se)` tham số thứ 2 là **fa1se** chứ không phải **false**, đọc [manual của sha1 trên php](https://www.php.net/manual/en/function.sha1.php) thì ta thấy đây là tham số của `raw_output`, và nếu được set về True thì kết quả trả về sẽ là binary. Và một *feature* của PHP đó là PHP sẽ hiểu chữ fa1se này là chuỗi. Và một chuỗi thì ko phải là false rồi :D, nên nó sẽ ra raw_output.  
Tới đây mình xem tiếp hint của hàm 