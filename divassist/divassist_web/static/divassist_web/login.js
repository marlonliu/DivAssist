$(document).ready(function() {

    $("#submit-button").hover(function() {
        $(this).css("background-color", "#0091EA"); // Light Blue A700
    } , function() {
        $(this).css("background-color", "#3DB7E4");
    });

    $("#error-message").css("width", $("#form-container").width().toString() + "px");
});