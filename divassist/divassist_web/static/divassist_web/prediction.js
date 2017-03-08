$(document).ready(function() {
    var setMapHeight = function() {
        var mapHeight = $(window).height() - $("#map-preamble").outerHeight();
        $("#map").css({
            "height": mapHeight.toString() + "px"
        });
    }

    setMapHeight();
    $(window).resize(setMapHeight);

    $("#prediction-submit").hover(function() {
        $(this).css("background-color", "#0091EA"); // Light Blue A700
    } , function() {
        $(this).css("background-color", "#3DB7E4");
    });
});