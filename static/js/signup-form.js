/*


                <small id="usernameHelpBlock" class="form-text col-sm-12 text-muted px-3">
                    How you will be identified on the site.
                    Up to 30 characters, allowed: letters, digits and @/./+/-/_ only.
                </small>


                <small id="emailHelpBlock" class="form-text col-sm-12 text-muted ml-auto px-3">
                    We will send an account activation email
                    to this address, so make sure you can access it.
                </small>


                <small id="password1HelpBlock" class="form-text col-sm-12 text-muted ml-auto px-3">
                    Password must be at least 9 characters, not similar to your username,
                    and including numbers and letters.
                </small>


                <small id="password2HelpBlock" class="form-text col-sm-12 text-muted ml-auto px-3">
                    Type in your password again to confirm it is correct.
                </small>
 */

$(document).ready(function () {

    // validate signup form on keyup and submit
    $("#register-form").validate({
        rules: {
            username: {
                required: true,
                minlength: 2,
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
                required: "Please enter a username",
                minlength: "Your username must consist of at least 2 characters",
            },
            password1: {
                required: "Please provide a password",
                minlength: "Your password must be at least 8 characters long",
            },
            password2: {
                required: "Please provide a password",
                minlength: "Your password must be at least 8 characters long",
                equalTo: "Please enter the same password as above",
            },
            email: "Please enter a valid email address",
        }
    });

});

