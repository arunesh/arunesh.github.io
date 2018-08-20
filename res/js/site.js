function show() {
    document.getElementById("show-more").style.display = "none";
    document.getElementById("article-expand").style.display = "block";
    var elem = document.getElementById('show-more-list');
    elem.parentNode.removeChild(elem);
}

function hide() {
    document.getElementById("show-more").style.display = "block";
    document.getElementById("article-expand").style.display = "none";
}
