const colors = ["#4285F4", "#00A1F1", "#34A853", "#7CBB00", "#FBBC05", "#FFBB00", "#EA4335", "#F65314"];
const logo_heading = document.querySelector('#logo_heading'); 
var previous = Math.floor(Math.random() * colors.length);
for (const letter of "CS50 Project One") {
    var current = Math.floor(Math.random() * colors.length);
    while (current - 1 == previous || current + 1 == previous) {
        current = Math.floor(Math.random() * colors.length);
    }
    const span = document.createElement('span');
    span.style.color = colors[current];
    span.innerText = letter;
    logo_heading.appendChild(span);
}
const input_container = document.querySelector('#input');
const clear_image = input_container.querySelector('#clear_image');
const input = input_container.querySelector('input');
function blink_clear_image() {
    if (input.value.length > 0) {
        if (clear_image.classList.contains('hidden')) {
            clear_image.classList.remove('hidden');
        }
    } else {
        if (!clear_image.classList.contains('hidden')) {
            clear_image.classList.add('hidden');
        }
    }
}
// Did not want to add two event listeners to the input, but had to becauase when ctrl + delete is done, keydown does not detect it, but keyup does. Could use "change" but what if the user is still on the input, then it will never hide the clear_image...
input.addEventListener('keydown', function() {
    blink_clear_image();
})
input.addEventListener('keyup', function() {
    blink_clear_image();
})
input_container.addEventListener('mouseenter', function() {
    input_container.style.borderColor = 'gray';
})
input_container.addEventListener('mouseleave', function() {
    input_container.style.borderColor = 'initial';
})
clear_image.disabled = true;
clear_image.addEventListener('click', function() {
    input.value = "";
})
