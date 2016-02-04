$(document).ready(function(){
  $('#token_request').click(function(){
    var email   =$("#username").val();
    payload={email:    email}
    $.getJSON('/_request_token', payload, function(data){
      parseStatus(data['status'])
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
        parseStatus(data['status'])
      })
    }else{
      parseStatus("pass_mismatch")
    }
    $("#password").val("");
    $("#repeat").val("");
  });
})
