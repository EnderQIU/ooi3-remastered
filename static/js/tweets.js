function renderLink(text) {
    var reg = /(http:\/\/|https:\/\/)((\w|=|\?|\.|\/|&|-)+)/g;
    return text.replace(reg, '<a href="$1$2" target="_blank">$1$2</a>');
}


function renderTweet(tweet) {
    let tweetContent = [
        '<div class="uk-panel">',
        '<h6 class="uk-panel-title">「艦これ」開発/運営</h6>',
        '<div class="uk-badge">',
        tweet.created_at,
        '</div>',
        '<p class="uk-article">',
        renderLink(tweet.text),
        '</p>',
        '<hr>'
    ].join(' ');

    $("#kancolle-staff-tweets-list").append(tweetContent);
}


function showError(message) {
    $("#kancolle-staff-tweets-list").append("<div class=\"uk-alert uk-alert-danger\">" + message + "</div>");
}


function renderTweets(resp) {
    if (resp.message !== 'ok') {
        showError(resp.message);
    }
    else {
        for (let tweet of resp.data) {
            renderTweet(tweet);
        }
    }
}


$(document).ready(function () {
    $.ajax({
        url: '/twitter',
        method: 'GET',
        success: function (result) {
            $("#loading").remove();
            renderTweets(result)
        },
        error: function () {
            $("#loading").remove();
            showError("Error while fetching tweets.")
        }
    })
});
