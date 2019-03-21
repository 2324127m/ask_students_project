function myFunction() {
    // Get the parent class of the answer to edit
    parent_class = event.target.parentNode.classList[0];

    // Replace the text area
    document.getElementsByClassName(parent_class)[0].innerHTML = "<form action='' role='form' method='post'>{{ answer_form.as_p }}</form>";
}