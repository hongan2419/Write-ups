# URL
https://ch9.sbug.se/
# Description
Guess what the flag is, and we will tell you if you're right!
## First glance
Just like the description say, this website take our input and check if it's the flag or not.

Howevery, nothing was sent to server, so this is a client-side checking. So this write up is almost about how do I debug, if you just want to check for the flag, go straight [here](#final-step).
## Setup
- This write up using Google Chrome web browser, and chrome dev tools. So a basic knowledge about chrome dev tools should be required.
- Burp Suite
- A web server to serve file (if you don't have one, you can use https://webhook.site/ for as an alternative solution)
## Pretty the source and serve it from our server
When I have to deal with objuscated javascript, the first thing I do is try to pretty the source and serve it in my server. Its advantage will be more clear when the process go on.

View the page source, we see that there are 4 script file
![image](https://user-images.githubusercontent.com/39065934/126716322-dce6aa58-fcc2-4bac-81b3-bf45318e7843.png)
We only focus on the `main.js` since other 3 should be a third party script. Open chrome dev tool, navigate to `Sources` tab, and go to `main.js` file
![image](https://user-images.githubusercontent.com/39065934/126716627-44ec25e9-839c-4e07-81b2-fed322c51a30.png)
Then pretty-print the source, any copy the prettied source to our server. Now to go Burp, in the `Proxy` tab, choose `Options` sub tab, and go to `Match and Replace`
![image](https://user-images.githubusercontent.com/39065934/126717128-91317885-aa77-4eff-b0f1-990fa9f805ed.png)

Click add, in the `Type` field, choose `Response body`, the `Match` and `Replace` field is what we want to replace in the source, so in this case, `Match` is `<script src="staticfiles/js/main.js"></script>`, and `Replace` is `<script src="$yourserver"></script>`
![image](https://user-images.githubusercontent.com/39065934/126717348-d22d5660-3cbc-430b-9173-3e39c788b7a1.png)

After that, refresh the browser, now you should see that the `main.js` replaced with `$yourserver`
![image](https://user-images.githubusercontent.com/39065934/126717461-3b241079-ff2a-48a7-9007-68bc1b5cf5d5.png)

## Remove jquery clear the path
At the beginning, I can't catch the event when submit the input. Adding event listener breakpoint doesn't works too. So after stucking in a while, I tried to remove the jquery script using Burp.
![image](https://user-images.githubusercontent.com/39065934/126717898-60b77027-2c41-48cc-bae9-f2f931584074.png)

Now the page throw an error
![image](https://user-images.githubusercontent.com/39065934/126717986-98db12f2-887c-4d6b-852b-04ce63cb7107.png)
Ignore 2 first error, we can see that there is an error in the `main.js` file. So quickly set a breakpoint there, and refresh the site, and check for the variable
![image](https://user-images.githubusercontent.com/39065934/126724444-5f09e830-1c10-491d-818b-7c29c21fd76a.png)

Up to this point, we can guess that `t6[0][0]` is `jquery $` and the code in line `2084` could be written as 
```javascript
$('.input2').each(doSomething);
```
but that's is not enough. Since there is suspicious function `j7G.n3(19)`, which only take 1 integer argument, I quickly write a snipper to print out all it content
```javascript
for (var i = 0; i < 30; i++)
  console.log(j7G.n3(i));
```
and this is the result (Please note that this happen on the breakpoint)

![image](https://user-images.githubusercontent.com/39065934/126725073-6ffdb6d9-86b7-4a2a-8bb3-7c4cb2af4ad8.png)


Okey so the "Corrent!" seem promising, but if we try to find `j7G.n3(17)` in the source code, it doesn't appear :confused:. Let's move on and take a look. We have a "#send", which should be the jquery select for the button, also there is a "click" string after it, so it can be `$('#send').click`. Let's check it by search `j7G.n3(27)`

![image](https://user-images.githubusercontent.com/39065934/126725281-2f06264a-ab60-4d60-b0dc-5295e8ebd706.png)

It is what we expected! A `j7G.n3(27)` follow with `j7G.n3(28)`. Remove the breakpoint on `2084`, and set a breakpoint on `1976`. Go to Burp and turn off removing the jquery, then refresh the page. Now try to input anything and click the button, the breakpoint should hit now.

## Patching the error and travel through countless meaningless function
By keep pressing F11 to make sure we remain on this function, after some loop, we see that we hit a condition

![image](https://user-images.githubusercontent.com/39065934/126725942-29c95614-4467-479c-b53e-83f0c1c1ace5.png)

Try to read current variable, we have `Z6[6]` hold our input, and `j7g.n3(30)` is "length"

![image](https://user-images.githubusercontent.com/39065934/126726206-9030bd2f-2fa9-40e3-ab81-9d9ad60b5c1a.png)

so this must be a check if our input's length is greater than 29 or not, currently our input is "test1234" and the length is 8. Keep pressing F11, and we hit a case where the bad end happen.

![image](https://user-images.githubusercontent.com/39065934/126726365-776c3544-b559-436b-b008-670290a51a39.png)
![image](https://user-images.githubusercontent.com/39065934/126726387-d38f4170-56b0-4bd4-b072-c01d2116993b.png)

By previous investigate, we know that the "Not correct!" string will be display onto our screen. Let's turn off the debug by pressing F8 now, and try a longer input (longer than 29 char, ofcourse). I simply slam the keyboard, and get the input `1234567890qwertyuiopasdfghjklzxcvbnm`. Now it time for the advantage of hosting the js file. We can't not set the breakpoint at line `1982` because the dev tool doesn't allow it, but we can do it by adding a `debugger;` command before it so now we can freely stop at anywhere.
![image](https://user-images.githubusercontent.com/39065934/126726886-dc2d518e-be92-43e9-b2ca-eb4159818c8b.png)

Refresh the page, fill in and hit the button, now we can hit the length condition without setting breakpoint on devtool anymore

![image](https://user-images.githubusercontent.com/39065934/126726953-f0a11cbb-a807-4a3e-92a0-781bb85c58fb.png)

Keep pressing F11, and we will hit a new branch of code.

![image](https://user-images.githubusercontent.com/39065934/126727140-9ee62975-beeb-4e3c-8c9c-44e951ab04a5.png)

This using async function, so we cant simply press F9 to hit there. But first, let's take a look at the flow. `h2` is the result of `Z(Z6[6])`, with `Z6[6]` is our input, then as we already know `t6[0][0])(j7G.n3(31))[j7G.O3(32)](h2)` mean `$('#result').html(h2)`, so `Z()` could be the checking flag function. Search `Z(` lead to it's defination on line `2312`. This function is quite long, but most of its is buggy and prevent you to continue. By audit the code, we can see that `Z()` have 2 return as follow
```javascript
function Z(i8) {
    j7G.I7G();
    var J6 = [arguments];
    J6[3] = j7G.o6()[35][26][6];
    for (; J6[3] !== j7G.o6()[9][34][6]; ) {
        switch (J6[3]) {
  ...
        case j7G.e6()[26][36][33]:
            return h(J6[0][0]);
            break;
        case j7G.o6()[5][18][34]:
            return j7G.S4(j7G.n3(8)) ? j7G.n3(3) : j7G.n3(9);
            break;
  ...
}
```

Let's try to make a breakpoint (from now, make a breakpoint mean adding `debugger;`) on `Z()` to see what is going on. If you try to run it by pressing F11, it will crash at some point. You can simply remove the bugging line and keep continue. But since we know that only 2 return line above is important, we should focus on it. After jump in `Z()`, `J6[0][0]` now is our input, but `j7G.S4` is not even a function :fearful:. I simply patch the code in line `2315` (initialize value for `J6[3]`) into 
```
J6[3] = jj7G.e6()[26][36][33];
```
to make it hit function `h()`

## Almost there
Similar to `Z()`, `h()` also contain a bunch of meaningless and buggy code, so keep patching and continue, which lead us to function `O()`. Although this function still contain some meaning less code, there is something different.
```javascript
function O(K8) {
    var K6 = [arguments];
    j7G.k7G();
    K6[2] = j7G.o6()[2][19][33];
    for (; K6[2] !== j7G.e6()[10][22][6]; ) {
        switch (K6[2]) {
        case j7G.e6()[32][36][30][21]:
            ...
            K6[8] = K6[0][0][2][j7G.n3(2)](0);
            K6[4] = K6[8] << 20;
            K6[2] = j7G.o6()[3][2][15];
            break;
        case j7G.o6()[7][9][37]:
            return j7G.z4(j7G.n3(16)) ? j7G.O3(9) : j7G.O3(3);
            break;
        case j7G.e6()[36][5][18]:
            K6[6] = K6[4] >> (j7G.A4(j7G.n3(15)) ? 6 : 5);
            K6[2] = j7G.o6()[0][3][36];
            break;
        case j7G.e6()[31][35][12]:
            K6[2] = K6[6] === 1097728 ? j7G.e6()[36][7][8] : j7G.o6()[13][37][16];
            break;
        case j7G.o6()[2][27][35]:
            return s(K6[0][0]);
            break;
        }
    }
}
```
With `K6[0][0]` is our input, `K6[8] = K6[0][0][2][j7G.n3(2)](0);` can be rewrite as `K6[8] = input[2].charCodeAt(0)`, and chaining into `K6[4] = K6[8] << 20`, after that `K6[6] = K6[4] >> 5`  (because `j7G.A4(j7G.n3(15))` return false), and finally compare if `K6[6] == 1097728`. So we simplify it into 
```
if ((input[2] << 20) >> 5 === 1097728)
  return true;
return false;
```
So, we extract `input[2] = String.fromCharCode((1097728 << 5) >> 20)`. However this is not right, because the result is a char "!", while the flag format is "SBCTF{", which mean `input[2]` should be "C" instead. By assume that the function `j7G.A4` is wrong, we have `input[2] = String.fromCharCode((1097728 << 6) >> 20)`, which now yeild a letter "C" as we expected. Keep moving to the function `s()`, we'll see a similar check.
```javascript
function s(M8) {
    var M6 = [arguments];
    M6[5] = j7G.e6()[8][32][27];
    for (; M6[5] !== j7G.o6()[25][31][10]; ) {
        switch (M6[5]) {
        case j7G.e6()[37][9][5]:
            return j7G.n3(9);
            break;
        case j7G.o6()[37][27][27]:
            return U(M6[0][0]);
            break;
        case j7G.o6()[31][4][24]:
            M6[5] = M6[7] === 1344 ? j7G.e6()[9][24][6] : j7G.o6()[14][28][35];
            break;
        case j7G.o6()[11][14][3]:
            M6[3] = M6[0][0][3][j7G.O3(2)](0);
            M6[4] = M6[3] << 20;
            M6[7] = M6[4] >> 16;
            M6[5] = j7G.o6()[28][11][33];
            break;
        }
    }
}
```
This function checking if `(input[3] << 20) >> 16 == 1344`, so we can reverse into `input[3] = String.fromCharCode((1344 << 16) >> 20)`, which is a letter "T", the process now more clear. But instead of keep following the function, I instead search for the pattern `[0][0][$positive]` for quickly grep the code.

## Final step
Searching through all the source code with pattern `[0][0][$position]` to get to the checking function of `$position`. Since we know the flag format is `SBCTF{...`, we should check from the position `6`, but for make sure, I will double check if the position `5` is a `{` or not. Search `[0][0][5]` give this function 
```javascript
function H(T8) {
  ...
        case j7G.e6()[38][31][3]:
            g6[3] = g6[6] === 251904 ? j7G.e6()[2][36][27] : j7G.e6()[3][24][11];
            break;
        case j7G.e6()[28][3][36]:
            g6[8] = g6[0][0][5][j7G.n3(2)](0);
            g6[4] = g6[8] << 14;
            g6[6] = g6[4] >> 3;
  ...
}
```
We only interesting in 2 part, first is the shifting, and second is the checking value, so we can describe the checking function above as follow 
```javascript
if ((input[5] << 14) >> 3 == 251904)
  return true;
else
  return false;
```
and therefore we can see that `input[5] = String.fromCharCode((251904 << 3) >> 14)`, which is equivalent to `input[5]='{'`, so our approach is good. Repeat with `[0][0][6]`,
we have
```javascript
function M(u8) {
  ...
        case j7G.e6()[16][24][12][15]:
            i6[1] = i6[0][0][6][j7G.O3(2)](0);
            i6[2] = i6[1] << 20;
            i6[6] = i6[2] >> 14;
            i6[9] = j7G.e6()[16][9][21];
            break;
        case j7G.o6()[30][25][30]:
            i6[9] = i6[6] === 7616 ? j7G.o6()[20][30][15] : j7G.e6()[13][21][17];
            break;
  ...
}
```
so `input[6] = String.fromCharCode((7616) << 14 >> 20)`, or `input[6] = 'w'`. Keep repeating the process, and we have following javascript code to gain the flag
```javascript
var input = new Array(30)
input[0] = 'S'
input[1] = 'B'
input[2] = 'C'
input[3] = 'T'
input[4] = 'F'
input[5] = String.fromCharCode((251904 << 3) >> 14)
input[6] = String.fromCharCode((7616) << 14 >> 20)
input[7] = String.fromCharCode((104 << 2) >> 3)
input[8] = String.fromCharCode((21248 << 5) >> 13)
input[9] = String.fromCharCode((760 << 5) >> 8)
input[10] = String.fromCharCode((29696 << 8) >> 16)
input[11] = String.fromCharCode((147456 << 7) >> 18)
input[12] = String.fromCharCode((26624 << 16) >> 25)
input[13] = String.fromCharCode((112640 << 11) >> 22)
input[14] = String.fromCharCode((1520 << 5) >> 9)
input[15] = String.fromCharCode((172032 << 8) >> 19)
input[16] = String.fromCharCode((7104 << 7) >> 13)
input[17] = String.fromCharCode((2528 << 11) >> 16)
input[18] = String.fromCharCode((97280 << 7) >> 17)
input[19] = String.fromCharCode((800 << 2) >> 5)
input[20] = String.fromCharCode((13440 << 3) >> 10)
input[21] = String.fromCharCode((35840 << 10) >> 19)
input[22] = String.fromCharCode((1120 << 4) >> 8)
input[23] = String.fromCharCode((784 << 9) >> 13)
input[24] = String.fromCharCode((101376 << 10) >> 20)
input[25] = String.fromCharCode((29952 << 15) >> 23)
input[26] = String.fromCharCode((1728 << 6) >> 10)
input[27] = String.fromCharCode((3801088 << 4) >> 19)
input[28] = String.fromCharCode((516096 << 9) >> 22)
input[29] = String.fromCharCode((1024000 << 5) >> 18)
flag = input.join('')
console.log("Flag:", flag)
```
![image](https://user-images.githubusercontent.com/39065934/126715315-94f97f61-f5ca-43ee-a0a1-315151c6eba9.png)

We have the correct flag, `SBCTF{w4S_tH47_ToO_diFF1cult?}`, but even the original website cannot check wether if this is the right flag or not :joy:
![image](https://user-images.githubusercontent.com/39065934/126715928-d9975836-6547-48a2-9240-a64c66897cf0.png)

