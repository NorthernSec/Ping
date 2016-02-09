//Bootstrap tooltip
jQuery(function () {
  $("[rel='tooltip']").tooltip();
});

//Back To Top
jQuery(document).ready(function() {
  var offset = 220;
  var duration = 500;
  jQuery(window).scroll(function() {
    if (jQuery(this).scrollTop() > offset) {
      jQuery('.back-to-top').fadeIn(duration);
    } else {
      jQuery('.back-to-top').fadeOut(duration);
    }
  });
  jQuery('.back-to-top').click(function(event) {
    event.preventDefault();
    jQuery('html, body').animate({scrollTop: 0}, duration);
    return false;
  })
});

//Temporary undo class
(function($){
  $.fn.extend({ 
    removeTemporaryClass: function(className, duration) {
      var elements = this;
      setTimeout(function() {
        elements.addClass(className);
      }, duration);
      return this.each(function() {
        $(this).removeClass(className);
      });
    }
  });
})(jQuery);

//Expand / collapse
jQuery(document).ready(function() {
  jQuery('.colfield').on('click', function (event) {
    if (event.target !== this) return;
    event.preventDefault();
    $(this).toggleClass("semiCollapsed");
  })
});


function setStatus(text, status){
  $("#status").empty();
  $("#status").removeClass();
  $("#status").addClass("alert alert-"+status);
  $("#status").append(text);
}

function parseStatus(status){
  _ok = false;
  switch(status){
    case "logged_in":		_ok=true;break;
    case "pass_updated":	setStatus("Changed your password!",								"success");_ok=true;break;
    case "action_added":	setStatus("New action added.",									"success");_ok=true;break;
    case "action_removed":	setStatus("The action was removed.",								"success");_ok=true;break;
    case "token_sent":		setStatus("Token sent to your e-mail",								"success");_ok=true;break;
    case "account_created":	setStatus("Your account was created! You can now log in",					"success");_ok=true;break;

    case "user_pass_mismatch":	setStatus("Wrong user/password combination!",							"danger"); break;
    case "user_exists":		setStatus("This e-mail is already registered",							"danger"); break;
    case "user_is_dead":	setStatus("This user is already marked as dead!",						"danger"); break;
    case "wrong_pass":		setStatus("The entered password is wrong!",							"danger"); break;
    case "user_action_failed":	setStatus("An error occured! Changes have not been saved!",					"danger"); break;
    case "edit_conflict":	setStatus("This action could not be completed because the data was manipulated elsewhere.",	"warning");break;
    case "fraud_attempt":	setStatus("Please don't try to manipulate calls... We don't appreciate that.",			"danger"); break;
    case "action_exists":	setStatus("A similar action already exists",							"danger"); break;
    case "mail_failed":		setStatus("We failed to send you the token", 							"danger"); break;
    case "invalid_mail":	setStatus("Your email doesn't seem to be complient", 						"danger"); break;
    case "banned_domain":	setStatus("We do not allow this domain",							"danger"); break;
    case "invalid_token":	setStatus("The token/email combination doesn't match!",						"danger"); break;
    case "pass_mismatch":	setStatus("The two password fields are not the same!",						"danger"); break;

    default:
      alert(status)
      setStatus("A problem occurred with the server!", "danger");
  }
  return _ok;
}
