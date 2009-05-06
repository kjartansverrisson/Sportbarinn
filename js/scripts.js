var calendar;

$(document).ready(function(){


	if(location.pathname.substring(0,17) == '/admin/navigation' && $("#id_model").val() != 'page'){
		$("#reference").parent().hide();
	}
	
	$("#id_model").change(function(event){
		event.preventDefault();
		if(event.target.value != 'page'){
			$("#reference").parent().hide("slow");			
		}else {
			$("#reference").parent().show("slow");
		} 
	});
	
	$("form#contact_form").submit(function(){
		alert("PRfa");
		$.post("/samband", {
			id_name: $("id_name").val(),
			id_email: $("id_email").val(),
			id_telephone: $("id_telephone").val(),
			id_message: $("id_message").val()
		}, function(xml){
			$("#messages").empty();
			$("#messages").prepend("Skilaboð send").show("slow");
		})
	})
});

function instCal(){
	
}

function laodEditor()
{
	var myEditor = new YAHOO.widget.SimpleEditor('id_content', {
	    height: '500px',
	    width: '100%',
		handleSubmit: true,
	    dompath: true //Turns on the bar at the bottom
	});
	myEditor.render();
}

function loadCalendar(calendar){
	if(calendar instanceof YAHOO.widget.Calendar){
		calendar.show();
	} else {
		calendar = new YAHOO.widget.Calendar("cal1Container");
		calendar.selectEvent.subscribe(function(){
			var arrDates = calendar.getSelectedDates();
			var date = arrDates[0];
			var displayMonth = date.getMonth() + 1; 
			var displayYear = date.getFullYear(); 
			var displayDate = date.getDate();
			$("#id_game_date").val( displayDate + "." + displayMonth + "." + displayYear );
			calendar.hide();
		})
		calendar.render();
	}
}

