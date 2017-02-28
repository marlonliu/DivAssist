$(document).ready(function() {
    var setGreeting = function() {
        var d = new Date();
        var h = d.getHours();
        var word;
        var time;
        if (h >= 6 && h <= 11) {
            word = "morning";
            time = 0;
        } else if (h >= 12 && h <= 17) {
            word = "afternoon";
            time = 1;
        } else {
            word = "evening";
            time = 2;
        }
        $("#greeting-time").text(word);
    }

    // Set greeting and landing page based on time.
    setGreeting();
});