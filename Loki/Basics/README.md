# URL
https://ch9.sbug.se/
# Description
Guess what the flag is, and we will tell you if you're right!
## First glance
Just like the description say, this website take our input and check if it's the flag or not.

Howevery, nothing was sent to server, so this is a client-side checking. So this write up is almost about how do I debug, if you just want to check for the flag, go straight [here](#markdown-header-final-step).
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
