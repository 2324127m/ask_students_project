$(function() {
    $('#delete-question').click(function() {
        return window.confirm("Are you sure you want to delete your question?");
    });
});

$(function() {
    $('#delete-answer').click(function() {
        return window.confirm("Are you sure you want to delete your answer?");
    });
});