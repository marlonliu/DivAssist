$(document).ready(function() {

    // var setContainerHeight = function() {
    //     var objHeight = $("body").height() - $("#nav").height() - $("#padding-block").height();
    //     console.log(objHeight.toString());
    //     $("#main-container").css({
    //         "height": objHeight.toString() + "px"
    //     });
    // }

    // setContainerHeight();

    // $(window).resize(setContainerHeight);

    $("#submit-button").hover(function() {
        $(this).css("background-color", "#0091EA"); // Light Blue A700
    } , function() {
        $(this).css("background-color", "#3DB7E4");
    });
});