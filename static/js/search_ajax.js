$(document).ready(function(){

    // autocomplete a JQuery UI method which uses AJAX
    // This is handled by the search view via AJAX request.
    $("#nav-search-input").autocomplete({
        source: "/ajax/search/",
        minLength: 2,
    });
});