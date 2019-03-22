$(document).ready(function () {

    // validate answer form on keyup and submit
    $("#ask_question_form").validate({
        rules: {
            name: {
                required: true,
                rangelength: [1, 64]
            },
            text: {
                required: true,
                rangelength: [1, 4096]
            },
            category: {
                required: true,
            }
        },
        messages: {
            name: {
                required: "Please enter the question title",
                rangelength: "Your question title must be no more than 64 characters long"
            },
            text: {
                required: "Please enter more question details",
                rangelength: "Your question details must be no more than 4096 characters long"
            },
            category: {
                required: "Please select a category",

            }
        },
        errorPlacement: function (error, element) {
            var name = element.attr("name");
            $("#errors_" + name).append(error);
            $("#errors_" + name).addClass("custom-error-style");
        }
    });
});