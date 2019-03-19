$(document).ready(function () {

    // validate signup form on keyup and submit
    $("#register-form").validate({
        rules: {
            username: {
                required: true,
                rangelength: [2, 30]
            },
            email: {
                required: true,
                email: true,
            },
            password1: {
                required: true,
                minlength: 8,
            },
            password2: {
                required: true,
                minlength: 8,
                equalTo: "#password1",
            },
        },
        messages: {
            username: {
                required: "Please enter a username.",
            },
            password1: {
                required: "Please provide a password.",
            },
            password2: {
                required: "Please provide a password.",
                equalTo: "Please enter the same password as above.",
            },
        },
        errorPlacement: function (error, element) {
            var name = element.attr("name");
            $("#errors_" + name).append(error);
            $("#errors_" + name).addClass("custom-error-style");
        }
    });

});

