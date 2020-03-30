window.onload = function() {
    const script_input = document.getElementById('id_script');
    const options = Array.from(script_input.children).slice();
    script_input.setAttribute('disabled', "");

    document.getElementById('id_language').onchange = get_script_choices;


    let xhttp = new XMLHttpRequest();
    xhttp.responseType = 'json';
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {  // success
            setup_script_input(this.response);
        }
    };

    function get_script_choices(e) {
        let language_id = e.target.value;
        let url = '/match-scripts/?language=' + language_id;
        xhttp.open('GET', url);
        xhttp.send();
    }

    function setup_script_input(data) {
        Array.from(script_input.children).forEach(child => child.remove());
        if (data.length) {
            script_input.removeAttribute("disabled");
            let new_children = data.map(language => options[language.id]);
            new_children.forEach(child => script_input.appendChild(child));
        } else {
            script_input.setAttribute("disabled", "");
            script_input.appendChild(options[0]);
        }
    }
};




