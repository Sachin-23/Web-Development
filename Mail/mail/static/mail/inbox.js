document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#show-mail').style.display = 'none';

//  document.querySelector("#submitMail").addEventListener("click", () => replyMail(this));
  document.querySelector("#submitMail").onclick = sendMail;
 
  // to archive the mail
  document.querySelector("#archiveMail").onclick = archiveMail;
 
  //add event handler to reply
  document.querySelector("#reply_email").onclick = replyMail;
   
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#show-mail').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#show-mail').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch all the emails 
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(email => {
      //console.log(email);

      //check if user has received any mails 
      if (email.length == 0)  {
        const div = document.createElement("div");
        div.innerText = "No emails received or sent yet.";
        div.setAttribute("class", "alert alert-warning");
        document.querySelector("#emails-view").appendChild(div);
      }
      else {
        for(let i = 0; i < email.length; i++)  {
          
          // create new div for every email user has received
          let div = document.createElement("div");

          // get email view
          const emailView = document.querySelector("#emails-view");
          div.setAttribute("id", `${email[i].id}`); 
          div.setAttribute("class", "email");
          let subject = email[i].subject.split(" ")
          
          // check if the subject is more than 3 words
          if (subject.length > 3)  {
            subject = subject[0] + " " + subject[1] + " " + subject[2] + "...";
          }
          else  {
            subject = email[i].subject;
          }
          
          // add email-sender, email-subject & email-timestamp inside the div
            div.innerHTML = `<span class="sender">${email[i].sender}</span> \
                            <span class="subject">${subject}</span> \
                            <span class="timestamp">${email[i].timestamp}</span>`;
          
          // check if the mail has been read
          if (email[i].read)  {
            div.style.backgroundColor = "#c0c0c0";
          }
          else  {
            div.style.backgroundColor = "white";
          }

          
          // add event click to every div
          div.addEventListener("click", function()  {

            
            // fetch the email details
            fetch(`/emails/${this.id}`)
            .then(response => response.json())
            .then(email => {
              //console.log(email);
              document.querySelector("#from").innerHTML = `<span><b>From:</b> ${email.sender}</span>`;
              document.querySelector("#to").innerHTML = `<span><b>To:</b> ${email.recipients.join(", ")}</span>`;
              document.querySelector("#subject").innerHTML = `<span><b>Subject:</b> ${email.subject}</span>`;
              document.querySelector("#timestamp").innerHTML = `<span><b>Timestamp:</b> ${email.timestamp}</span>`;
              document.querySelector("#email_body").innerText = email.body;
              document.querySelector('#emails-view').style.display = 'none';
              document.querySelector('#show-mail').style.display = 'block';
              document.querySelector("#reply_email").dataset.id = `${email.id}`; 
              const archive = document.querySelector("#archiveMail");
              if (mailbox != "sent")  {
                archive.dataset.id = `${email.id}`; 
                if (email.archived)  {
                  archive.innerText = "Unarchive";
                }
                else  {
                  archive.innerText = "Archive";
                }
              }
              else  {
                archive.style.display = "none";  
              }
            });

            // send a PUT request and set the mail as read
            fetch(`/emails/${this.id}`,  {
              method: "PUT",
              body: JSON.stringify({
                read: true
              })
            })
            //add response condition
            .then(response => {
              //console.log(response);
            })
            
          });

          // add all email to the emailView
          emailView.appendChild(div);
        }
      }
    });
}

function sendMail()  {
  console.log("what is happening ?")
  const to = document.querySelector("#compose-recipients").value
  const subject = document.querySelector("#compose-subject").value
  const body = document.querySelector("#compose-body").value
  const div = document.querySelector("#warning");
  if ( to == "" || body == "" || subject == "")  {
    div.innerText= "Please checking for any missing field";
    div.setAttribute("class", "alert alert-danger");
  }
  else {
    div.innerText= "";
    div.removeAttribute("class");
    //console.log(to, subject, body);
    fetch("/emails",  {
      method: "POST",
      body: JSON.stringify({
        recipients: to,
        subject: subject,
        body: body
      })
    })
      .then(response => response.json())
      .then(result => { 
//        console.log(result);
//        console.log("done interacting with webserver");
        if ("error" in result)  {
          div.setAttribute("class", "alert alert-danger");
          div.innerText = result["error"];
        }
        else if("message" in result)  {
//          div.setAttribute("class", "alert alert-success");
//          div.classList.add("alert alert-success");
//          div.innerText = result["message"];
          load_mailbox("sent");
        }
      });
  }
  return false;
}


function replyMail()  {
  document.querySelector('#show-mail').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Show compose view and hide other views
  

  fetch(`/emails/${this.dataset.id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.slice(0, 3) === "Re:")  {
      document.querySelector('#compose-subject').value = email.subject;
    }
    else  {
      document.querySelector('#compose-subject').value = "Re: " + email.subject;
    }
    document.querySelector('#compose-body').value = "On " + email.timestamp + " " + email.sender + " wrote: " + email.body + "\n";
  });

  // Clear out composition fields
}


function archiveMail()  {
  if (this.innerText === "Archive")  {
    fetch(`/emails/${this.dataset.id}`,  {
      method: "PUT",
      body: JSON.stringify({
        archived: true
      })
    })
    .then(response => response.json)
    .then(data => {
      load_mailbox("archive");
    });
  }
  else  {
    fetch(`/emails/${this.dataset.id}`,  {
      method: "PUT",
      body: JSON.stringify({
        archived: false
      })
    })
    .then(response => response.json)
    .then(data => {
      load_mailbox("inbox");
    });
  }
}
