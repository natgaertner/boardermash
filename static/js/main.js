
$(document).ready(function() {
	function getboarders() {
	$.get("/twoboarders", function(data) {
	    $("#leftboarder").html(data['leftboarder']['boarder_name']);
	    $("#leftboarder").data("id", data['leftboarder']['boarder_name']);
	    $("#rightboarder").html(data['rightboarder']['boarder_name']);
	    $("#rightboarder").data("id", data['rightboarder']['boarder_name']);
	}, "json");
	};
	getboarders();
	$(document).keydown(function(event) {
		var winner;
		if(event.which == 37) {
			winner = "left";
		} else if (event.which == 39) {
			winner = "right";
		} else {
			return;
		}
		$.ajax({
		    async: false,
		    type: "POST",
		    url: "/mash",
		    data: JSON.stringify({leftid:$("#leftboarder").data("id"),rightid:$("#rightboarder").data("id"),winner:winner}),
		    contentType: "application/json; charset=utf-8",
		    dataType: "json"
		});
		getboarders();
	});
});
