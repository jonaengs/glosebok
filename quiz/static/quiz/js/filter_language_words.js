let langBoxes = Array.from(document.getElementsByTagName("input"))
    .filter(elem => elem.getAttribute("type") === "checkbox").slice(1);  // list of all language checkbox elements
let allBox = document.getElementById("all-checkbox");
let urlParams = new URLSearchParams(window.location.search);

// check boxes specified in url params
if (urlParams.get('languages') != null) {
    let languages =  urlParams.get('languages').split(",");
    langBoxes.filter(chbox => languages.includes(chbox.value))
        .forEach(chbox => chbox.checked = true);
} else {
    allBox.checked = true;  // if no query is given, all words are returned.
}

function uncheckAllBoxAndReload() {
    allBox.checked = false;
    setParamsAndReload();
}

function setParamsAndReload() {
    let url = window.location.href.split("?")[0];
    let params = langBoxes.filter(chbox => chbox.checked)
        .map(chbox => chbox.value).join(",");
    let query = allBox.checked ? "" : "?languages=" + params;  // if "All" is checked
    window.location.href = url + query;
}