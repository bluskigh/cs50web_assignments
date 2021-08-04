// global scope
var compose_form;
var emails_view;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  compose_form = document.querySelector("#compose-form");
  compose_form.addEventListener("submit", function(e) {

    e.preventDefault();
    fetch("/emails", {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json"
      }),
      body: JSON.stringify({
        recipients: compose_form.querySelector("#compose-recipients").value,
        subject: compose_form.querySelector("#compose-subject").value,
        body: compose_form.querySelector("#compose-body").value
      })
    })
    .then(async r => await r.json())
    .then(r => {
      load_mailbox("sent");
    }).catch(e => {alert(e.error);console.log(e);})
  })
});

function remove_all_children(parent) {

  while (parent.children.length > 0) {
    parent.removeChild(parent.children[0]);
  }
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function prefill_composition_form() {

  compose_email();
  // load composition form with appropriate values
  compose_form.querySelector("#compose-recipients").value = window.localStorage.getItem("sender");
  // final subject that is going to be used as the value for the subject input
  let final_sub = '';
  if (window.localStorage.getItem("subject").slice(0, 3) != "Re:") {
    final_sub = "Re: ";
  }
  compose_form.querySelector("#compose-subject").value = `${final_sub}${window.localStorage.getItem("subject")}`;
  compose_form.querySelector("#compose-body").value = `On ${window.localStorage.getItem("timestamp")} ${window.localStorage.getItem("sender")} wrote: ${window.localStorage.getItem("body")} \n`;
}

function load_mailbox(mailbox) {

  if (emails_view == null) {
    emails_view = document.querySelector("#emails-view");
  }
  // fetching all the emails under "mailbox"
  fetch(`/emails/${mailbox}`)
  .then(async r => await r.json())
  .then(r => {

    // iterating through the emails
    for (const email of r) {
      const container = document.createElement("div");
      container.classList.add("email-item", "center");
      container.dataset.emailId = email.id;
      container.dataset.something = 'soemtiging';

      // checking if the email has been read, if so change background color
      if (email.read) {
        container.style.background = "rgb(120, 120, 120)";
        container.style.color = "rgb(240, 240, 240)";
      }

      // left side contains sender and the subject
      const left = document.createElement("span");
      left.classList.add("email-info", "center");

      const who = document.createElement("p");
      // recipients joined together with ','
      const r_values = Object.values(email.recipients).join();
      if (mailbox == "sent") {
        who.classList.add('sent-recipient');
        who.innerText = r_values;
      } else {
        who.classList.add('from-sender');
        who.innerText = email.sender;
      }

      const subject = document.createElement("p");
      subject.innerText = email.subject;
      subject.classList.add("subject");

      const timestamp = document.createElement("p");
      timestamp.innerText = email.timestamp;

      left.appendChild(who);
      left.appendChild(subject);

      container.appendChild(left);
      container.appendChild(timestamp);

      // onclick even listener runs code in function when the container is clicked
      container.addEventListener("click", function() {

        // if the container is not marked as read, do so
        if (!email.read) {
          // update that the email has been read
          fetch(`/emails/${email.id}`, {
            method: "PUT",
            headers: new Headers({
              "Content-Type": "application.json"
            }),
            body: JSON.stringify({
              read: true 
            })
          })
          .catch(e => {alert(e.error);console.log(e);})
        }

        // get email information
        fetch(`/emails/${email.id}`)
        .then(async r => await r.json())
        .then(_ => {

          emails_view.innerHTML = `
          <p><strong>From: </strong>${email.sender}</p>
          <p><strong>To: </strong>${r_values}</p>
          <p><strong>Subject: </strong>${email.subject}</p>
          <p><strong>Timestamp: </strong>${email.timestamp}</p>
          <button onclick='prefill_composition_form()'>Reply</button>
          `;

          // store in local storage(used in function prefill_composition_form)
          window.localStorage.setItem("sender", email.sender);
          window.localStorage.setItem("subject", email.subject);
          window.localStorage.setItem("body", email.body);
          window.localStorage.setItem("timestamp", email.timestamp);

          // Deciding what archive button to display 
          if (mailbox == "inbox") {
            emails_view.innerHTML += `<button class="danger" onclick="archive(this, true)" data-email-id="${email.id}">Archive</button>`;
          } else if (mailbox == "archive") {
            emails_view.innerHTML += `<button class="danger" onclick="archive(this, false)" data-email-id="${email.id}">Un-Archive</button>`;
          }

          emails_view.innerHTML += `
          <hr>
          <p>${email.body}</p>
          `;
        }).catch(e => {alert(e.error); console.log(e);})
      })

      // finally, appending the container to the emails_view
      emails_view.appendChild(container);
    }
  }).catch(e => {alert(e.error);console.log(e);})

  // Show the mailbox and hide other views
  emails_view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function archive(object, value) {

  // setting the archived status to value
  fetch(`/emails/${object.dataset.emailId}`, {
    method: "PUT",
    headers: new Headers({
      "Content-Type": "application/json"
    }),
    body: JSON.stringify({
      archived: value 
    })
  })
  .then(async r => await r.json())
  .then(_ => {
    load_mailbox("inbox")
  }).catch(_ => {load_mailbox("inbox");})
}