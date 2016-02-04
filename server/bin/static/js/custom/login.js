$(document).ready(function(){
  $('#login').click(function(){
    var user=$("#username").val();
    var pwd =$("#password").val();
    payload={username: user,
             password: pwd}
    $.getJSON('/_login', payload, function(data){
      if(parseStatus(data['status'])){
        window.location = "/profile";
      }
    })
  });
})

