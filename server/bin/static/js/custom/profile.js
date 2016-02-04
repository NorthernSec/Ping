$(document).ready(function(){
  $('#change_pass').click(function(){
    var current=$("#passwd").val();
    var newpass=$("#new_passwd").val();
    var repeat= $("#repeat_passwd").val();
    if(newpass == repeat){
      payload={password: current,  new_password: newpass}
      $.getJSON('/_change_pass', payload, function(data){
        parseStatus(data['status'])
        $("#passwd").val("");
        $("#new_passwd").val("");
        $("#repeat_passwd").val("");
      })
    }else{
      parseStatus("pass_mismatch")
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
      if(parseStatus(data['status'])){
        // use data["actions"] to re-fill table
      }
    });
  });
})
