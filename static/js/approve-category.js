
function deleteCategoryRequest() {
    return window.confirm("Are you 100% sure you want to delete this request? This cannot be undone!");
}

$(document).ready(function() {
    $('.approve-category').click(function() {
        return window.confirm("Are you sure you want to approve this category? The description you submit here will be the PUBLIC description!");
    });,
    $('.delete-category-request').click(function() {
        return window.confirm("Are you 100% sure you want to delete this request? This cannot be undone!");
    });
});
