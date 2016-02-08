var inUpdate = false;
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

  $('#new-action').click(function(){
    $("#method").val("xmpp");
    $("#target").val("");
    $("#username").val("");
    $("#message").val("");
    inUpdate=false;
    $("#add-action").show();
    $("#update-action").hide();
  });

  $('#add-action').click(function(){
    payload={method:   $("#method").find(":selected").text(),   target:  $("#target").val(),
             username: $("#username").val(), message: $("#message").val() }
    $.getJSON('/_add_action', payload, function(data){
      alert(data['status'])
      parseStatus(data['status'])
    })
  });

  $("#method").on('change', function(){ setTargetPlaceholder() });

  setTargetPlaceholder()
  fillTable();
  activateButtons();
});

function setTargetPlaceholder(){
  switch($("#method").val()){
    case "xmpp":
      $("#target").attr("placeholder", "xmpp account(s), separated by comma (,)");
      break;
    case "irc":
      $("#target").attr("placeholder", "<irc server>[<port>],<users or channels, separated by comma (,)>");
      break;
    case "mail":
      $("#target").attr("placeholder", "e-mail address(es), separated by comma (,)");
      break;
  }
}

function activateButtons(){
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
    inUpdate=true;
    $("#add-action").hide();
    $("#update-action").show();
  });

  $('[id^="remove-"]').click(function(){
    if(confirm("Are you sure you want to delete this action?")){
      uid=this.id.split("-")[1];
      row=$("#action-"+uid);
      cells=row.find('td');
      payload={action: cells[0].innerHTML, target: cells[1].innerHTML}
      $.getJSON('/_remove_action', payload, function(data){
        if(parseStatus(data['status'])){
          fillTable();
        }
      });
    }
  });
}

function fillTable(){
  $.getJSON('/_get_actions', {}, function(data){
    $("#actions > tbody > tr").remove()
    lid=0;
    for(i in data['data']){
      line=data['data'][i];
      uname="";
      if(line['username'] != null){uname=line['username'];}else{uname=line['user'];}
      if(uname.length > 13){uname = uname.substring(0, 10) + "...";}
      if(line.message != null){clss="glyphicon glyphicon-star";}else{clss="";}

      new_line = "<tr id='action-"+lid+"'><td>"+line.action+"</td> <td>"+line.target+"</td> <td>"+uname +"</td>";
      new_line+= "<td><div rel='tooltip' title='"+line.message+"'> <span class='"+clss+"'></span></div></td>";
      new_line+= "<td><span id='edit-"+lid+"' title='edit' class='glyphicon glyphicon-edit' data-toggle='modal' data-target='#editmodal'></span>";
      new_line+= "<span id='remove-"+lid+"' title='remove' class='glyphicon glyphicon-remove'></span></td></tr>";

      $("#actions > tbody").append(new_line);
      lid++;
    }
    activateButtons();
  });
}
