$(document).ready(function(){
  $('#change_pass').click(function(){
    var current=$("#passwd").val();
    var newpass=$("#new_passwd").val();
    var repeat= $("#repeat_passwd").val();
    if(newpass == repeat){
      payload={password:        current,
               new_password:    newpass}
      $.getJSON('/_change_pass', payload, function(data){
        switch(data['status']){
          case "no match":
            setStatus("The entered password is wrong!", "danger");
            break;
          case "success":
            setStatus("Changed your password!", "success");
            break;
          case "failed":
            setStatus("An error occured! Could not save changes", "danger");
            break;
        }
        $("#passwd").val("");
        $("#new_passwd").val("");
        $("#repeat_passwd").val("");
      })
    }else{
      setStatus("The new passwords don't match!", "danger")
    }
  });
   $('[id^="edit-"]').click(function(){
     uid=this.id.split("-")[1];
     row=$("#action-"+uid);
     cells=row.find('td');
     alert(cells[0].innerHTML)
   });

})
