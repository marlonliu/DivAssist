$(document).ready(function() {
    $(".hidden-details").hide();

    // Set alternating row colors.
    var counter = 0;
    $(".record-entry").each(function() {
        if (counter % 2 === 1) {
            $(this).css({
                "background-color": "#ECEFF1"
            });
        }
        counter += 1;
    });

    $(".show-button").click(function() {
        $(this).parent().parent().find(".hidden-details").show(150);
        $(this).hide()
    });

    $(".hide-button").click(function() {
        var parent = $(this).parent();
        parent.find(".show-button").show();
        parent.find(".hidden-details").hide(200);
    });
});