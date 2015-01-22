$(document).ready(function() {

  var ready = false, leftBoarder, rightBoarder,
    $leftName, $rightName, $leftAv, $rightAv, uuid, hmac;

  var init = function(){
    $leftName = $('#leftboarder');
    $rightName = $('#rightboarder');
    $leftAv = $('#leftav');
    $rightAv = $('#rightav');
  }

  var getBoarders = function() {
    $.get("/twoboarders", function(data) {

      leftBoarder = data.leftboarder;
      rightBoarder = data.rightboarder;
      uuid = data.matchuuid;
      hmac = data.hmac

      $leftName.text(leftBoarder.boarder_name);

      if (leftBoarder.av) {
        $leftAv.attr("src", "http://duc0plcpp9l5c.cloudfront.net/static/images/avs/"+leftBoarder.av);
        $leftAv.show();
      } 
      else {
        $leftAv.attr("src","");
	$leftAv.hide()
      }

      $rightName.text(rightBoarder.boarder_name);

      if (rightBoarder.av) {
        $rightAv.attr("src", "http://duc0plcpp9l5c.cloudfront.net/static/images/avs/"+rightBoarder.av);
        $rightAv.show();
      } 
      else {
        $rightAv.attr("src","");
	$rightAv.hide()
      }

      ready = true;
    }, "json");
  };

  var keyUpHandler = function(event) {
    if(event.which == 37) {
      declareWinner("left");
    } else if (event.which == 39) {
      declareWinner("right");
    }
  };

  var declareWinner = function(winner) {
    if (!ready) return;
    ready = false;
    $rightAv.hide();
    $leftAv.hide();
    $rightName.text('');
    $leftName.text('');

    var dataToPost=JSON.stringify({leftid:leftBoarder.boarder_name,rightid:rightBoarder.boarder_name,winner:winner,uuid:uuid,hmac:hmac});
    $.ajax({
        type: "POST",
        url: "/mash",
        data: dataToPost,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });

    getBoarders();
  }

  init();
  getBoarders();
  $(document).on('keyup',keyUpHandler);
  $(document).on('click', '#leftav', function(){
    declareWinner("left");
  });
  $(document).on('click', '#rightav', function(){
    declareWinner("right");
  });
  $(document).on('click', '#leftboarder', function(){
    declareWinner("left");
  });
  $(document).on('click', '#rightboarder', function(){
    declareWinner("right");
  });
});
