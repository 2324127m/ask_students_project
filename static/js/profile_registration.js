var loadFile = function (event) {
    var output = document.getElementById('image-preview');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.classList.add('image-preview-dim');
};