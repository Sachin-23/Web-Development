document.addEventListener("DOMContentLoaded", function()  {

  const pathname = window.location.pathname.slice(1);

/* register and login */
/*------------------------------------------------------------------*/

  if (pathname === "register" || pathname === "login")  {
    
    const register = document.querySelector("#register");
    const login =  document.querySelector("#login");

    eval(`${pathname}.style.display = "block";`);

    document.querySelectorAll("a").forEach(function(a)  {

      a.onclick = function(e)  {
        e.stopPropagation();
        var l = login;
        if (login.style.display === "none" && register.style.display === "block")  {
          register.style.display = "none";
          login.style.display = "block";
          history.pushState("", "", "login");
        }
        else if(login.style.display === "block" && register.style.display === "none")  {
          login.style.display = "none";
          register.style.display = "block";
          history.pushState("", "", "register");
        }
        return false;
      }
      
    });

  }

/*------------------------------------------------------------------*/



});
