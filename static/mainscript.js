var local = {};
local.avatar = "iqlogo.png";

var remote = {};
remote.avatar = "https://developers.viber.com/images/apps/apiai-icon.png";


var accessToken = "3c44974b43934bbdb1fdc030b17df30e";
var baseUrl = "https://api.api.ai/v1/";

function formatTime(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

function insertChat(who, text){
    var control = "";
    var date = formatTime(new Date());
    
     if (who == "local"){
        
         control = '<li style="width:80%;align:right">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +                                                       
                  '</li>';                   
    }else{
        control = '<li style="width:80%;align:right">' +
                        '<div class="msj macro">' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';   
    }
    $("#messages").append(control);
    var objDiv = document.getElementById("messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

$("#chat-panel").on('click',function(){
    $(".innerframe").toggle();
});

function resetChat(){
    $("#messages").empty();
}

$(".mytext").on("keyup", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            insertChat("local", text);              
            $(this).val('');
            queryBot(text)
        }
    }
});

resetChat();
var a=0;
var SESSIONID="TESTINPUT%s"%(++a)

function queryBot(text) {
            $.ajax({
                type: "POST",
                url: baseUrl + "query?v=20150910",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                headers: {
                    "Authorization": "Bearer " + accessToken
                },
                data: JSON.stringify({ query: text, lang: "en", sessionId: SESSIONID }),
                success: function(data) {
                    insertChat("remote",data.result.fulfillment.speech);
                },
                error: function() {
                    insertChat("remote","Sorry My Bot has faced some issues! Please try again later");
                }
            });
    }
$('#reslink').click(function(e){
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "sample.html",
        data: { },
        success: function(data){
            $('#maincont').html(data);
        }
    });
});
