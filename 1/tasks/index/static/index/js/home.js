const todocontainer = document.querySelector('#todocontainer');
const donecontainer = document.querySelector('#donecontainer');
const input = document.querySelector('#form input');
const add = document.querySelector('#form button');

function remove(element) {
    const parentId = element.parentElement.getAttribute('id');
    element.parentElement.removeChild(element);
    if (parentId != 'donecontainer') {
        
            donecontainer.appendChild(element);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const lis = document.querySelectorAll('#todocontainer li');
lis.forEach(item => {
    item.addEventListener('click', function() {
        fetch('/done', {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') 
            }),
            body: JSON.stringify({
                'task': item.innerText
            })
        })
        .then(async r => await r.json())
        .then(r => {
            if(r.success) {
                // for now, just going to refresh the page to inedxe
                window.location = '/';
            } else {
                alert('Could not mark the task as done');
            }
        })
        .catch(e => { console.log(e); })
    })
})

/*
add.addEventListener('click', function() {
    const li = document.createElement('li');
    li.innerText = input.value;
    li.addEventListener('click', function() {
        remove(this)
    })
    input.value = null;
    todocontainer.appendChild(li);
})
*/

const todooption = document.querySelector('#todooption');
const doneoption = document.querySelector('#doneoption');
function toggleActive(element, other) {
    element.disabled = true;
    other.disabled = false;
    todocontainer.classList.toggle('hidden');
    donecontainer.classList.toggle('hidden');
    todooption.classList.toggle('active');
    doneoption.classList.toggle('active');
}
todooption.addEventListener('click', function() {
    toggleActive(this, doneoption);
    input.disabled = false;
    add.disabled = false;
})
doneoption.addEventListener('click', function() {
    toggleActive(this, todooption);
    input.disabled = true;
    add.disabled = true;
})

