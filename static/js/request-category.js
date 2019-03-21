$(document).ready(function () {

    // validate signup form on keyup and submit
    $("#request-category").validate({
        rules: {
            name: {
                required: true,
                rangelength: [2, 64]
            },
            description: {
                required: true,
                rangelength: [30, 512]
            },
        },
        messages: {
            name: {
                required: "Please enter the name of the category you are requesting.",
                rangelength: "You must provide a name that is at least 2 and at most 64 characters"
            },
            description: {
                required: "Please enter a reason as to why you want this category.",
                rangelength: "You must provide a reason that is least 30 and at most 512 characters"
            },
        },
        errorPlacement: function (error, element) {
            var name = element.attr("name");
            $("#errors_" + name).append(error);
            $("#errors_" + name).addClass("custom-error-style");
        }
    });

});
