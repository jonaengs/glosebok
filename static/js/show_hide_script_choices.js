window.onload = function() {
    const script_input = document.getElementById('id_script');
    const options = Array.from(script_input.children).slice();
    let language_input = document.getElementById('id_language');
    language_input.onchange = get_script_choices;
    if (language_input.value === "") {
        script_input.parentElement.style.display = 'none';
    }

    let xhttp = new XMLHttpRequest();
    xhttp.responseType = 'json';
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {  // success
            setup_script_input(this.response);
        }
    };

    function get_script_choices() {
        let language_id = language_input.value;
        let url = '/match-scripts/?language=' + language_id;
        xhttp.open('GET', url);
        xhttp.send();  // calls setup_script_input with received data
    }

    function setup_script_input(data) {
        Array.from(script_input.children).forEach(child => child.remove());  // remove all script choices
        if (data.length) { // if relevant scripts were found, put those back as available choices
            script_input.parentElement.style.display = 'block';
            let new_children = data
                .map(script => options.find
                    (elem => elem.value == script.id));  // value and id are not the same type.
            new_children.forEach(child => script_input.appendChild(child));
        } else {
            script_input.parentElement.style.display = 'none';
            script_input.appendChild(options[0]);
        }
    }
};




