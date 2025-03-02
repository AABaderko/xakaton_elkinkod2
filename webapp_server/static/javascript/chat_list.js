const chatSocketsList = [];

chat_id_list.forEach((chat_id) => {
    chatSocketsList[chat_id] = new WebSocket("ws://" + window.location.host + `/ws/chat/${chat_id}/`);
})

chatSocketsList.forEach((chatSocket) => {
    chatSocket.onopen = function (e) {
        console.log("The connection was setup successfully !");
    };
    
    chatSocket.onclose = function (e) {
        console.log("Something unexpected happened !");
    };
    
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        var div = document.createElement("div");
        div.innerHTML = data.username + " : " + data.message;
        document.querySelector("#id_chat_item_container").appendChild(div);
    };
});
