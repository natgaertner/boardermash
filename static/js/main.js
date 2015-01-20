
$(document).ready(function() {
	function getboarders() {
	$.get("/twoboarders", function(data) {
	    $("#leftboarder").html(data['leftboarder']['boarder_name']);
	    $("#leftboarder").data("id", data['leftboarder']['boarder_name']);
	    if (data['leftboarder']['av']){
            	$("#leftav").attr("src", "/static/images/avs/"+data['leftboarder']['av']);
		$("#leftav").show();
	    } else {
		$("#leftav").attr("src","");
		$("#leftav").hide();
	    }
	    $("#rightboarder").html(data['rightboarder']['boarder_name']);
	    $("#rightboarder").data("id", data['rightboarder']['boarder_name']);
	    if (data['rightboarder']['av']){
            	$("#rightav").attr("src", "/static/images/avs/"+data['rightboarder']['av']);
		$("#rightav").show();
	    } else {
		$("#rightav").attr("src","");
		$("#rightav").hide();
	    }
	}, "json");
	};
	getboarders();

	function debounce(fn, delay) {
		var timer = null;
		return function () {
			var context = this, args = arguments;
			clearTimeout(timer);
			timer = setTimeout(function () {
				fn.apply(context, args);
			}, delay);
		};
	};

	function mash(event) {
		var winner;
		if(event.which == 37) {
			winner = "left";
		} else if (event.which == 39) {
			winner = "right";
		} else {
			$(document).bind('keydown',mash);
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
	};
	$(document).bind('keydown', debounce(mash,100));
});
