function getTweets(page, callback) {
    var q = $("#search").val();
    $("#loading").show();

    $.getJSON("/search", {q: q, p:page}, function(data){
        if(data.finished){
            $("#more").hide();
        }

        $.each(data.results, function(i, tweet){

            var buttons = $("<span />")
                             .addClass("buttons")
                             .append($("<abbr />").attr("title", tweet.date)
                                                  .text(tweet.date))
                             .append($("<span/>").text(" - "))
                             .append($("<a />").attr("href", tweet.url)
                                               .text("link"))

            if(tweet.geo){
                var mapsUrl = "http://maps.google.com?q=" + tweet.latitude + "," + tweet.longitude;
                buttons.append($("<span/>").text(" - "))
                       .append($("<a />").attr("href", mapsUrl)
                                               .text("geo"))
            }

            if(tweet.reply){
                var replyUrl = "http://twitter.com/" + tweet.in_reply_to_name + "/status/" + tweet.in_reply_to_id; 
                buttons.append($("<span/>").text(" - "))
                       .append($("<a />").attr("href", replyUrl)
                                               .text("in reply to"))
            }

            $("<li/>")
                     .append($("<span/>").html(tweet.text)).linkify()
                     .append($("<br/>"))
                     .append(buttons)
                     .addClass("tweet")
                     .appendTo("#results")
        });

        $("abbr").timeago();

        window.location.hash = q;
        $("#loading").hide();

        if(callback){
           callback();
        }
    })
}

$(document).ready(function(){

    var hash = window.location.hash;

    if(hash && hash.indexOf("|") > 0){
        $("#search").val(hash.replace("#", ""));
    }

    $("#search").keydown(function(e){
        if(e.keyCode === 13){
            $("#results > hr").remove()
            $("li").remove();

            $("#more").data('page', 1).show();
            getTweets(1);
        }     
    })

    $("#more").click(function(){
        var that = $(this);
        var page = that.data('page') + 1;
        var hr = $("<hr />").appendTo("#results");
        var scroll = $(document).scrollTop();

        getTweets(page, function(){
            that.data('page', page);
            $(document).scrollTop(scroll);
        });

        return false;
    })

    if($("#search").val() != ""){
        getTweets(1);
    }
})
