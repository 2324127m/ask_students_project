// User must confirm they want to delete their profile
$(document).ready(function () {
    $('.delete-user-profile').click(function() {
        return window.confirm("Are you 100% sure you want to delete your profile? This cannot be undone!");
    });
});