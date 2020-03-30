function checkAns(e) {
    let input = e.target;
    let correct_value = input.getAttribute('correct');
    if (input.value.toLowerCase() === correct_value) {
        input.style.borderColor = 'green';
    } else {
        input.style.borderColor = 'red';
        document.getElementById(input.id+'-label').innerText += ' = ' + correct_value;
    }
    input.setAttribute('disabled', true);
    focusNextInput(input);
}

function focusNextInput(elem) {
    let next = elem.nextElementSibling;
    if (next === null) {
        let parent = elem.parentElement;
        if (parent !== null) {
            focusNextInput(parent.nextElementSibling.firstElementChild)
        }
    }
    else if (next.classList.contains('answer-input')) {
        next.focus();
    } else {
        focusNextInput(next);
    }
}