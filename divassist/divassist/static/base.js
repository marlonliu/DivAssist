$(document).ready(function() {
    var setCopyrightYear = function() {
        d = new Date();
        yr = d.getFullYear();
        $("#cur-year").text(yr.toString());
    }

    setCopyrightYear();
});