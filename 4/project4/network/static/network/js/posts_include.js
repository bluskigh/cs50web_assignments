var postsContainer, nextButton, previousButton, editForm, editTitleInput, editTextInput, userid;

// default page 0 of all posts
var page = 1;

function clearPosts() {

    while(postsContainer.children.length) {
        postsContainer.removeChild(postsContainer.children[0])
    }
}

function like(e) {

    const post_id = this.parentElement.parentElement.parentElement.parentElement.dataset.id;
    var currentState = this.classList.contains("svg-active");
    fetch("/likes", {

        method: !currentState? "POST" : "DELETE",
        mode: "same-origin",
        headers: new Headers({

            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken").value,
            "Content-Type": "application/json"
        }),
        body: JSON.stringify({post_id, liked: !currentState})
    })
    .then(r => {
        if (r.status == 200) {
            const nextSibling = this.nextElementSibling;
            if (!currentState == true) {
                // liked
                nextSibling.innerHTML = `&nbsp;${parseInt(nextSibling.innerText) + 1}&nbsp;`;
                this.classList.add("svg-active")
            } else {
                // unliked
                nextSibling.innerHTML = `&nbsp;${parseInt(nextSibling.innerText) + -1}&nbsp;`;
                this.classList.remove("svg-active")
            }
        } else {
            alert("Something went wrong... (Action: like)")
        }
    }).catch(e => {alert("Something went wrong... (action: like)")})

}

function createPost(post_information, form=null) {

    // creating the post
    const tempContainer = document.createElement("div");
    tempContainer.classList.add("post")
    tempContainer.dataset.id = post_information.id;
    const tempContentContainer = document.createElement("div");
    tempContentContainer.classList.add("post-content")
    const editButton = document.createElement("button");
    editButton.classList.add("edit")
    editButton.innerText = "Edit"
    const who = document.createElement("a");
    who.setAttribute('href', `/users/${post_information.user_id}`)
    who.innerText = post_information.username;
    const header = document.createElement("h3");
    header.innerText = post_information.title;
    const paragraph = document.createElement("p");
    paragraph.innerText = post_information.text;
    const optionsContainer = document.createElement("div");
    optionsContainer.classList.add("options")
    const heartSpan = document.createElement("span");
    const heart = document.createElement("svg");
    heart.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="15px" height="15px" viewBox="0 0 375 375"><defs><clipPath><path class="path" d="M0 21.3L375 21.3 375 353.6 0 353.6ZM0 21.3"/></clipPath></defs><g class="clippath" clip-path="url(#clip1)"><path class="path2" d="M187.5 353.5L183.5 350.8C183.1 350.5 137.4 319.3 92.4 276.2 65.9 250.7 44.6 226.1 29.3 203 9.9 173.5 0 146.1 0 121.8 0 66.5 45.1 21.4 100.4 21.4 121 21.4 140.9 27.7 157.8 39.7 170.1 48.4 180.1 59.5 187.5 72.3 194.9 59.4 204.9 48.3 217.2 39.7 234.1 27.7 254 21.4 274.6 21.4 329.9 21.4 375 66.5 375 121.8L375 121.9C374.8 146 364.8 173.2 345.3 202.6 330 225.7 308.9 250.3 282.3 275.9 237.4 319.2 191.9 350.5 191.5 350.8ZM100.4 35.4C52.8 35.4 14 74.2 14 121.8 14 143.3 23.1 168 41 195.1 55.6 217.3 76.2 241.2 102 265.9 138.5 300.9 175.6 328 187.5 336.4 199.4 327.9 236.3 300.7 272.7 265.6 298.4 240.8 318.9 217 333.6 194.8 351.5 167.7 360.8 143.2 360.9 121.8 360.9 74.2 322.1 35.5 274.5 35.5 239.2 35.5 206.9 57.9 193.9 91.1L187.4 108.1 181 91.1C168.1 57.9 135.8 35.4 100.4 35.4ZM100.4 35.4" style=" stroke:none;"/></g></svg>';
    heart.classList.add("svg")
    heart.setAttribute("height", "15px")
    heart.setAttribute("width", "15px")
    heart.addEventListener("click", like)
    if (post_information.likes.filter(like => like == userid).length == 1) {
        heart.classList.add("svg-active")
    } else {
        heart.classList.remove("svg-active")
    }
    const likesAmount = document.createElement("p");
    likesAmount.innerHTML = `&nbsp;${post_information.likes.length}&nbsp;`;
    likesAmount.style.display = "inline-block";
    const comment = document.createElement("svg");
    comment.classList.add("svg")
    comment.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="15px" height="15px" viewBox="0 0 375 375"><defs><clipPath><path d="M19 21L370.5 21 370.5 374 19 374ZM19 21"/></clipPath></defs><g clip-path="url(#clip1)"><path class="path2" d="M195.2 373C157.2 373 121.1 361 90.6 338.2L30 354.8C27.2 355.5 24.2 354.7 22.1 352.6 20.1 350.5 19.4 347.4 20.3 344.6L40.8 280.4C27.1 254.9 19.9 226.3 19.9 197.5 19.9 100.7 98.6 21.9 195.2 21.9 291.8 21.9 370.5 100.7 370.5 197.5 370.5 294.3 291.9 373 195.2 373ZM92.4 321.5C94.1 321.5 95.9 322 97.3 323.1 125.6 345.3 159.4 357.1 195.2 357.1 283.1 357.1 354.5 285.5 354.5 197.5 354.5 109.4 283.1 37.9 195.2 37.9 107.3 37.9 35.9 109.4 35.9 197.5 35.9 224.7 43 251.7 56.4 275.6 57.4 277.5 57.7 279.9 57 281.9L39.9 335.5 90.2 321.7C90.9 321.5 91.6 321.5 92.4 321.5ZM92.4 321.5" style=" stroke:none;"/></g></svg>';
    heartSpan.appendChild(heart)
    heartSpan.appendChild(likesAmount)
    optionsContainer.appendChild(heartSpan)
    optionsContainer.appendChild(comment)
    // for created or updated 
    const time = document.createElement("time");
    time.setAttribute("datetime", post_information.created)
    time.innerText = (post_information.updated ? "Updated: " : "") + post_information.created;
    if (parseInt(post_information.user_id) == userid) {
        tempContentContainer.appendChild(editButton)
        editButton.addEventListener("click", function() {

            // if the edit form is in a post still, then hide the form, so that the post
            // that was clicked can use it.
            if (editForm.parentElement.classList.contains("post")) {
                hideForm()
            }

            const parentElement = this.parentElement.parentElement;

            // add editing class
            parentElement.classList.toggle("editing");

            const content = parentElement.querySelector(".post-content");
            // TODO add an animation where the content is inactive when we are trying to load
            // the post data, also disable the inputs
            parentElement.appendChild(editForm);

            fetch(`/posts?id=${parentElement.dataset.id}`)
            .then(async r => await r.json())
            .then(r => {
                // information of post recieved, set form edit inputs value to the information recieved.
                editTitleInput.value = r.title;
                editTextInput.value = r.text;
            }).catch(e => {console.log(e);})
        })
    }
    tempContentContainer.appendChild(who)
    tempContentContainer.appendChild(header)
    tempContentContainer.appendChild(paragraph)
    tempContentContainer.appendChild(optionsContainer)
    tempContentContainer.appendChild(time)
    tempContainer.appendChild(tempContentContainer)
    if (form) {
        postsContainer.insertBefore(tempContainer, postsContainer.firstChild)
    } else {
        postsContainer.appendChild(tempContainer)
    }
} 

function morePosts() {

    fetch(`/is_more?page=${page}${document.location.pathname == '/following' ? "&following=True" : ""}`)
    .then(async r => await r.json())
    .then(r => {
        if (r.result) {
            // displaying the button
            nextButton.classList.remove("hidden");
            // TODO what if the user removes hidden in the html inspector and a request is sent 
            // to get more posts, constraint for that
        } else {
            nextButton.classList.add("hidden");
        }
    }).catch(e => console.log(e))
}

///
//// When the page content has loaded
/// 
document.addEventListener("DOMContentLoaded", function() {

    userid = parseInt(document.querySelector("nav").dataset.userId);
    postsContainer = document.querySelector("#posts"); 

    var path = document.location.pathname == "/"; 
    if (document.location.pathname.indexOf("users")) {
        var id = document.location.pathname.split('/');
        id = id[id.length-1];
        path = `/posts?userid=${id}`
    } else if (path) {
        path = "/posts?page=0"
    } else {
        path = "/following"
    }

    editForm = document.querySelector("#edit-form");
    editTitleInput = editForm.querySelector("#id_title");
    editTextInput = editForm.querySelector("#id_text");

    // get all the posts and render in the postsContainer
    fetch(path)
    .then(async r => await r.json())
    .then(r => {
        for (const post of r.posts) {
            createPost(post, null)
        }
    }).catch(e => {console.log(e)})

    // onload of the document check if there are most posts to be displayed 
    morePosts()

    ///
    //// Traversing through posts (previous and next buttons)
    ///
    nextButton = document.querySelector("#next");
    previousButton = document.querySelector("#previous");
    nextButton.addEventListener("click", function() {

        // load all the posts that are on page + 1 from current
        page += 1;
        fetch(`/${path}?page=${page}`)
        .then(async r => await r.json())
        .then(r => {
            if (page >= 1 && previousButton.classList.contains("hidden")) {
                previousButton.classList.remove("hidden")
            }
            morePosts()
            clearPosts()
            for (const post of r.posts) {
                createPost(post)
            }
            window.scrollTo(0, 0)
        }).catch(e => console.log(e))
    })
    previousButton.addEventListener("click", function() {

        page -= 1;
        fetch(`/${path}?page=${page}`)
        .then(async r => await r.json())
        .then(r => {
            if (page == 1 && previousButton.classList.contains("hidden") == false) {
                previousButton.classList.add("hidden")
            }
            morePosts()
            clearPosts()
            for (const post of r.posts) {
                createPost(post, null)
            }
        }).catch(e => console.error(e))
    })

    ///
    ////// EDIT FORM
    ///

    const hideForm = () => {
        // remove editing class
        editForm.parentElement.classList.toggle("editing");

        // move this form from the post to the body and hide
        document.querySelector("body").appendChild(editForm);

        // erasing the input since its not going to belong to anything anymore, when it belongs
        // to a post, then it will be filled with the posts information.
        editTitleInput.value = null;
        editTextInput.value = null;
    };

    editForm.addEventListener("submit", function(e) {

        e.preventDefault();
        // TODO: check on change of the edit form inputs, if changed after Edit ON THE FORM
        // button has been clicked then patch, otherwise if no edit was made do not fetch
        // to server.
        fetch(`/posts?id=${this.parentElement.dataset.id}`, {
            method: "PATCH",
            mode: "same-origin",  // used so that I do not send CSRF token anywher else. good practice. https://docs.djangoproject.com/en/3.2/ref/csrf/#setting-the-token-on-the-ajax-request 
            headers: new Headers({
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken").value,
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                title: editTitleInput.value,
                text: editTextInput.value
            })
        })
        .then(r => {
            // success, edit the text of the post and hide this form
            // replacing the text of the post title and text with the patched version
            editForm.parentElement.querySelector("h3").innerText = editTitleInput.value;
            editForm.parentElement.querySelector("p").innerText = editTextInput.value;
            hideForm()
        }).catch(e => {console.log(e);})
    })

})
