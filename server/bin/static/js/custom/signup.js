$(document).ready(function(){
  $('#token_request').click(function(){
    var email   =$("#username").val();
    payload={email:    email}
    $.getJSON('/_request_token', payload, function(data){
      switch(data['status']){
        case "success":
          setStatus("Token sent to your e-mail", "success");
          break;
        case "mail failed":
          setStatus("We failed to send you the token", "danger");
          break;
        case "invalid mail":
          setStatus("Your email doesn't seem to be complient", "danger");
          break;
        case "invalid domain":
          setStatus("We do not allow this domain", "danger");
          break;
        case "user exists":
          setStatus("This e-mail is already registered", "danger");
          break;
        default:
          setStatus("A problem occurred with the server!", "danger");
      }
    })
  });
  $('#create').click(function(){
    var email   =$("#username").val();
    var password=$("#password").val();
    var repeat  =$("#repeat").val();
    var token   =$("#token").val();
    if(password == repeat){
      payload={email:    email,
               password: password,
               token:    token};
      $.getJSON('/_create_account', payload, function(data){
        switch(data['status']){
          case "success":
            setStatus("Your account was created! You can now log in", "success");
            break;
          case "already exists":
            setStatus("A user with this email already registred!", "danger");
            break;
          case "invalid token":
            setStatus("The token/email combination doesn't match!", "danger");
            break;
          default:
            setStatus("A problem occurred with the server!", "danger");
        }
      })
    }else{
      setStatus("The passwords don't match!", "danger")
    }
    $("#password").val("");
    $("#repeat").val("");
  });
})
