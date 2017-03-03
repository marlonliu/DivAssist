$(document).ready(function() {
    var setMapHeight = function() {
        var mapHeight = $(window).height() - $("#map-preamble").outerHeight();
        $("#map").css({
            "height": mapHeight.toString() + "px"
        });
    }

    setMapHeight();
    $(window).resize(setMapHeight);
});