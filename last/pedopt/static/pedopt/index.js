"use strict";

document.addEventListener("DOMContentLoaded", function()  {

  const wishlist = document.getElementById("wishlist"); 
  if (wishlist)  {
    wishlist.onclick = function()  {
      const id = wishlist.dataset.id;
      const request = new Request(
       "/wishlist",
        {headers: {"X-CSRFToken": getCookie("csrftoken")}}
      );

      fetch(request, {
        method: 'PUT',
        mode: "same-origin",
        body: JSON.stringify({
            id: `${id}`,
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status == 200) { 
          if (wishlist.src.search("fill") > 0)  {
            wishlist.src = "http://127.0.0.1:8000/static/pedopt/wishlist.svg";
            wishlist.alt = "add to wishlist"
          }
          else  if (wishlist.src.search("wishlist") > 0)  {
            wishlist.src = "http://127.0.0.1:8000/static/pedopt/wishlist_fill.svg";
            wishlist.alt = "remove from wishlist";
          }
        }
      });
    }
  }
  

  const findPet = document.getElementById("find_pet");
  const message = document.querySelector("#message");
  if (findPet)  {
    findPet.onsubmit = function()  {
      for (let i = 0; i < this.length - 1; i++)  {
        if (this[i].value == "Select")  {
          message.innerText = "Please select a option.";
          message.style.display = "block";
          return false;
        }
      }
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
