$(document).ready(function() {
    var containerWidth = $("#load-window-body").width() - 5;
    $("#load-window-body").css({
        "width": containerWidth.toString() + "px"
    });
    console.log("load window set: " + containerWidth);
});