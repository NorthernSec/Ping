$(document).ready(function(){
  $('#login').click(function(){
    var user=$("#username").val();
    var pwd =$("#password").val();
    payload={username: user,
             password: pwd}
    $.getJSON('/_login', payload, function(data){
      switch(data['status']){
        case "no match":
          setStatus("Wrong user/password combination!", "danger");
          break;
        case "user dead":
          setStatus("This user is already marked as dead!", "danger");
          break;
        case "success":
          window.location = "/profile";
          break;
        default:
          setStatus("A problem occurred with the server!", "danger");
      }
    })
  });
})

