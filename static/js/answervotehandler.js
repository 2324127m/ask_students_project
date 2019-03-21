$(document).ready( function() {

    $('.like-btn').click(function() {
        let answer_id = event.target.id;
        answer_id.strip
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

    $('#like-' + String(answer)).text(new_likes);
    $('#dislike-' + String(answer)).text(new_dislikes);

}
