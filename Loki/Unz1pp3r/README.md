# URL
https://ch26.sbug.se
# Description

Our site has been under development for 3 years, can you test it so we can release it?

## First glance


## Bypass javascript?

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