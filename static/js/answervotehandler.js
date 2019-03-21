$(document).ready( function() {

    $('.like-btn').click(function() {
        let answer_id = event.target.id;
        voteLike(answer_id);
    })

    $('.dislike-btn').click(function() {
        let answer_id = event.target.id;
        voteDislike(answer_id);
    })
})

function voteLike(answer_id) {
    vote(answer_id, 1);
}

function voteDislike(answer_id) {
    vote(answer_id, 0);
}

function vote(answer_id, vote) {

    $.ajax({
            url : "/ajax/vote/",
            method: 'POST',
            async : true,
            data : {
                answer_id: answer_id,
                vote: vote,
                csrfmiddlewaretoken: CSRF_TOKEN
            },
            success: updatePage
        }
    )
}

function updatePage(result, status, xhr) {
    // Update page with new values.
    let response = JSON.parse(result);
    let answer = response.answer_id;
    let new_likes = response.likes;
    let new_dislikes = response.dislikes;
    let action = response.action;

    $('#like-' + String(answer)).text(new_likes);
    $('#dislike-' + String(answer)).text(new_dislikes);

    let like_btn = $('#like-btn-' + String(answer));
    let dislike_btn = $('#dislike-btn-' + String(answer))

    // Now lets update the button colours
    switch (action) {
        case "like":
            like_btn.prop("src", "/static/images/active-like.png");
            dislike_btn.prop("src", "/static/images/dislike.png");
            break;
        case "dislike":
            like_btn.prop("src", "/static/images/like.png");
            dislike_btn.prop("src", "/static/images/active-dislike.png");
            break;
        case "remove":
            like_btn.prop("src", "/static/images/like.png");
            dislike_btn.prop("src", "/static/images/dislike.png");
            break
    }

}
