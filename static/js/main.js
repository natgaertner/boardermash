$(document).ready(function() {

  var ready = false, leftBoarder, rightBoarder,
    $leftName, $rightName, $leftAv, $rightAv, uuid; 
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

      $leftName.text(leftBoarder.boarder_name);

      if (leftBoarder.av) {
        $leftAv.attr("src", "http://duc0plcpp9l5c.cloudfront.net/static/images/avs/"+data.leftboarder.av);
        $leftAv.show();
      } 
      else {
        $leftAv.attr("src","");
      }

      $rightName.text(rightBoarder.boarder_name);

      if (rightBoarder.av) {
        $rightAv.attr("src", "http://duc0plcpp9l5c.cloudfront.net/static/images/avs/"+data.rightboarder.av);
        $rightAv.show();
      } 
      else {
        $rightAv.attr("src","");
      }

      ready = true;
    }, "json");
  };

  var mash = function(event) {
    var winner;

    if (!ready) return;

    if(event.which == 37) {
      declareWinner("left");
    } else if (event.which == 39) {
      declareWinner("right");
    }
    
    getBoarders();
  };

  var declareWinner = function(winner) {
    ready = false;
    $rightAv.hide();
    $leftAv.hide();
    $rightName.text('');
    $leftName.text('');
    dataToPass = JSON.stringify({leftid:leftBoarder.boarder_name,rightid:rightBoarder.boarder_name,winner:winner,uuid:uuid});
    $.ajax({
        type: "POST",
        url: "/mash",
        data: dataToPass,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });
  }

  init();
  getBoarders();
  $(document).bind('keyup',mash);
});
