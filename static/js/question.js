$(document).ready(function () {

    // validate answer form on keyup and submit
    $("#answer_form").validate({
        rules: {
            text: {
                required: true,
                rangelength: [1, 4096]
            },
        },
        messages: {
            text: {
                required: "Please enter an answer you wish to post",
                rangelength: "Your answer must be no more than 4096 characters long"
            },
        },
        errorPlacement: function (error, element) {
            var name = element.attr("name");
            $("#errors_" + name).append(error);
            $("#errors_" + name).addClass("custom-error-style"); 
        }
    });
});

// User must confirm they want to delete question
$(function() {
    $('.delete-question').click(function() {
        return window.confirm("Are you sure you want to delete your question?");
    });
});

// User must confirm they want to delete answer
$(function() {
    $('.delete-answer').click(function() {
        return window.confirm("Are you sure you want to delete your answer?");
    });
});