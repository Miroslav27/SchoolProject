const room_name = $("#room-name").val();
const API_URL = "http://127.0.0.1:8000/api/v1/auctions";
var chat_history = ""

let ws = new WebSocket('ws://127.0.0.1:8000/ws/auction/'+room_name);
$('#chat-log').val(chat_history)
$("#chat-message-submit").click(function (){
    const message = $("#chat-message-input").val();
    ws.send(JSON.stringify({'room_name':room_name,"message":message}))
});

ws.onmessage = function(data){
    const message = JSON.parse(data.data).message;
    const username = JSON.parse(data.data).username;
    var now = new Date(Date.now());
    var formatted_time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    chat_history+="("+formatted_time+")"+username + ": " + message+"\n"
    $('#chat-log').val(chat_history)
    $("#chat-message-input").val('')
    $.getJSON(API_URL+"/"+room_name,function(dataJson){
    $("#bid-value").val(parseFloat(dataJson.last_bid_value)+parseFloat(dataJson.bid_step_value))
    $("#bid-user").val(dataJson.last_bid_user)
     });
    console.log(username + ": " + message);
   };

 $('#bid-value-btn').click(function () {
    $.getJSON(API_URL+"/"+room_name,function(dataJson){
    dataJson.last_bid_value = Math.max(parseFloat(dataJson.last_bid_value)+parseFloat(dataJson.bid_step_value), $("#bid-value").val())
    dataJson.last_bid_user = $('#user_id').val()
    if (dataJson.active === true){
    $.ajax({
        type: "PATCH",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/"+room_name+"/",
        data: dataJson,
        success: function(data){
        console.log("PATCH-done")
        }
    })
    const message = "new bid for " +dataJson.last_bid_value
    ws.send(JSON.stringify({'room_name':room_name,"message":message}))
    }
    })
});

 $('#stop-btn').click(function () {
    $.getJSON(API_URL+"/"+room_name,function(dataJson){
    dataJson.active = "false"
    $.ajax({
        type: "PATCH",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/"+room_name+"/",
        data: dataJson,
        success: function(data){
        console.log("PATCH-done")
        }
    })
    const message = "Auction stoped with last value " +dataJson.last_bid_value + " winner id is: " + dataJson.last_bid_user;
    ws.send(JSON.stringify({'room_name':room_name,"message":message}));
    })
});
 $('#start-btn').click(function () {
    $.getJSON(API_URL+"/"+room_name,function(dataJson){
    dataJson.active = "true"
    $.ajax({
        type: "PATCH",
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        url: API_URL+"/"+room_name+"/",
        data: dataJson,
        success: function(data){
        console.log("PATCH-done")
        }
    })
    const message = "Auction (re)-started with last bid value" +dataJson.last_bid_value + " last bidder id is: " + dataJson.last_bid_user;
    ws.send(JSON.stringify({'room_name':room_name,"message":message}));
    })
});