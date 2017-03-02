$(document).ready(function(){

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
        $("#default-option").attr("dest", $("#default-option").attr("dest") + time.toString() + "/");
    }

    var setPredictionUrl = function() {
        var d = new Date();
        var day = d.getDay();
        var h = d.getHours();
        $("#prediction-option").attr("dest", $("#prediction-option").attr("dest") + day + "/" + h + "/");
    }

    // Set greeting and landing page based on time.
    setGreeting();

    // Set prediction link to include current day and time as default options
    setPredictionUrl();

    $(".second-level-option").hide();

    $(".first-level-option, .second-level-option").hover(
        function() {
            if (!$(this).hasClass("selected")) {
                $(this).animate({
                    "padding-left": "+=1em"
                }, 100);
                $(this).css({
                    "background-color": "#3DB7E4",
                    "color": "#FFFFFF"
                });
            }
        }, 
        function() {
            if (!$(this).hasClass("selected")) {
                $(this).animate({
                    "padding-left": "-=1em"
                }, 150);
                $(this).css({
                    "background-color": "#FFFFFF",
                    "color": "#263238"
                });
            }
        }
    );

    var expandAllSub = function(obj) {
        var cur = obj.next();
        while (cur.hasClass("second-level-option")) {
            cur.show(150);
            cur = cur.next();
        }
    }

    var hideAllSub = function(obj) {
        var cur = obj.next();
        while (cur.hasClass("second-level-option")) {
            cur.hide(200);
            cur = cur.next();
        }
    }

    var removeSelectedProperty = function() {
        $(".selected").animate({"padding-left": "-=1em"}, 150);
        $(".selected").css({
            "color": "#263238",
            "background-color": "#FFFFFF"
        });
        $(".selected").removeClass("selected");
        $(".expanded").removeClass("expanded");
    }

    var executeFunc = function(obj) {
        var func = obj.attr("func");
        if (func === "land") {
            window.location.href = obj.attr("dest");
        } else if (func === "load") {
            var dest = obj.attr("dest");
            console.log(dest);
            $("#load-window").attr("src", dest);
        }
    }

    $(".first-level-option").click(function() {
        if ($(this).attr("func") === "expand") {
            if ($(this).hasClass("expanded")) {
                hideAllSub($(this));
                $(this).removeClass("expanded");
            } else {
                // $(".second-level-option").hide(200);
                // $(".first-level-option").removeClass("expanded");
                expandAllSub($(this));
                $(this).addClass("expanded");
            }
        } else {
            if (!$(this).hasClass("selected")) {
                removeSelectedProperty();
                $(".second-level-option").hide(200);
                $(this).addClass("selected");
                $(this).css({"background-color": "#263238"});
                executeFunc($(this));
            }
        }
    });

    $(".second-level-option").click(function() {
        if (!$(this).hasClass("selected")) {
            removeSelectedProperty();
            $(this).addClass("selected");
            $(this).css({"background-color": "#263238"});
            executeFunc($(this));
        }   
    });

    var adjustIframeSize = function() {
        var iframeW = $("#main-container").innerWidth() - $("#home-nav").outerWidth() - 2 * parseInt($("#main-container").css("padding-left")) - 10;
        console.log("Width=" + iframeW);

        var iframeH = $(window).outerHeight() - $("#nav").outerHeight() - $("#footer").outerHeight() - parseInt($("#main-container").css("padding-top")) * 2;
        if (iframeH < $("#home-nav").outerHeight()) {
            iframeH = $("#home-nav").outerHeight();
        }
        console.log("Height=" + iframeH);

        $("#load-window").css({
            "height": iframeH.toString() + "px",
            "width": iframeW.toString() + "px"
        });
    }

    adjustIframeSize();

    $(window).resize(function() {
        adjustIframeSize();
    });

    $("#home-nav").resize(function() {
        adjustIframeSize();
    });

    // Trigger the click of the default landing page.
    $("#default-option").trigger("click");

});