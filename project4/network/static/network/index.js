document.addEventListener("DOMContentLoaded", () =>  {

  const pagination = document.querySelector("#pagination");

  pagination.style.display = "none";

  window.onscroll = () =>  {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight)  {
      pagination.style.display = "block";
      console.log("Reached at the end");
    }
  }

  document.querySelectorAll("#like").forEach(function(button) {

    button.onclick = function()  {
      if (document.querySelector("#current_username") === null) {
        window.location.href = "/login";
      }
      else {
        if (!button.disabled)  {
          button.disabled = true;
          let action = "";
          const id = this.dataset.id;
          const likes = document.querySelector(`#likes_${id}`);
          if (this.className === "far fa-heart")  {
            this.setAttribute("class", "fas fa-heart");
            action = "like";
            likes.innerText = parseInt(likes.innerText) + 1; 
          }
          else if (this.className === "fas fa-heart")  {
            this.setAttribute("class", "far fa-heart");
            action = "unlike";
            likes.innerText = parseInt(likes.innerText) - 1; 
          }
          
          const req = new Request(
            "/like",
            {headers: {"X-CSRFToken": getCookie("csrftoken")}} 
          );
          fetch(req, {
            method: "PUT", 
            mode: "same-origin",
            body: JSON.stringify({
              id: `${id}`,
              action: `${action}`
            })
          })
          .then(response => response.json())
          .then(data =>  {
            console.log(data);
            button.disabled = false;
          });
        }
      }
    }
  });


/*--------------bs jquery----------*/
$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('whatever') // Extract info from data-* attributes
  var modal = $(this);
  modal.find('#msg').text("") 
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // 
  fetch(`/get_post/${id}`)  
  .then(response => response.json())
  .then(data => {
    console.log(data);

    const editButton = document.querySelector("#edit-button");

    const edit = document.querySelector("#message-text");

    edit.value = data["body"]; 



    editButton.onclick = function()  {
      if (edit.value.length != 0)  {

        console.log(edit.value);

        $('#exampleModal').modal('hide'); 
        const request = new Request(
          "/edit_post",
          {headers: {"X-CSRFToken": getCookie("csrftoken")}}
        );
        
        fetch(request, {
          method: "POST",
          mode: "same-origin" ,
          body: JSON.stringify({
            id: `${id}`,
            content: `${edit.value}`
          })
        })
        .then(response => response.json())
        .then(data => {
          console.log(data)
          location.reload();
        })


      }
      else  {
       modal.find('#msg').text("Please Enter Proper Text");
      }

    }

  });


})


  





  
  if (document.querySelector("#following") != undefined) { 

    document.querySelector("#following").onclick = function()  {

      let action = this.innerText;
      const username = document.querySelector("#username").innerText;
      const followersCount = document.querySelector("#followers");
      let number = parseInt(followersCount.innerText.split(" ")[0]);
      
      let change = "";

      
      if (action === "Unfollow")  {
        change = "Follow";
        number -= 1; 
      }
      else if (action === "Follow"){
        change = "Unfollow";
        number += 1;
      }


        const req = new Request( 
          "/follow",
          {headers: {"X-CSRFToken": getCookie("csrftoken")}}
        );
        fetch(req, {
            method: "POST",
            mode: "same-origin", 
            body: JSON.stringify({
              username: `${username}`,
              action: `${action}`
            })
          })
        .then(response => response.json())
        .then(data => {
          console.log(data, change)
        });
        this.innerText = change;
        followersCount.innerText = number + " Followers";
    }
  }



  



});


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
