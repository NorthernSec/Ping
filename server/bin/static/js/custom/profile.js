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
    payload={action: cells[0].innerHTML, target: cells[1].innerHTML}
    $.getJSON('/_get_action_details', payload, function(data){
      $("#method").val(data['action'])
      $("#target").val(data['target'])
      $("#username").val(data['username'])
      $("#message").val(data['message'])
    });
  });
  $('[id^="remove-"]').click(function(){
    uid=this.id.split("-")[1];
    row=$("#action-"+uid);
    cells=row.find('td');
    payload={action: cells[0].innerHTML, target: cells[1].innerHTML}
    $.getJSON('/_remove_action', payload, function(data){
      switch(data['status']){
        case "success":
          setStatus("Removed action", "success");
          // use data["actions"] to re-fill table
          break;
        case "invalid_user_action":
          setStatus("This action could not be completed because the data was manipulated elsewhere.", "warning");
          break;
        case "fraude_attempt":
          setStatus("Please don't try to manipulate calls... We don't appreciate that.", "error");
          break;
      }
    });
  });
})
