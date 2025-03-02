const MESSAGE_TEMPLATE = document.getElementById("message-template");
const MESSAGES_BOX = document.getElementById("id_chat_item_container");

const chatSocket = new WebSocket(
    "ws://" + window.location.host + `/ws${window.location.pathname}?user_id=${user_id}`,
);

chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};

chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

document.querySelector("#id_message_send_input").focus();
document.querySelector("#id_message_send_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        document.querySelector("#id_message_send_button").click();
    }
};

document.querySelector("#id_message_send_button").onclick = function (e) {
    var messageInput = document.querySelector("#id_message_send_input").value;
    chatSocket.send(JSON.stringify({
        type: "send_message",
        chat_id: chat_id,
        user_id: user_id,
        user_name: user_name,
        text: messageInput,
        datetime: toString(new Date())
    }));
    document.querySelector("#id_message_send_input").value = "";
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    let message_dev = MESSAGE_TEMPLATE.cloneNode(true);
    message_dev.id = "";
    message_dev.style = "";

    let container_message = message_dev.querySelector(".message-info");
    
    container_message.querySelector(".message-user").textContent = data.username;
    container_message.querySelector(".message-text").textContent = data.message;
    container_message.querySelector(".message-time").textContent = data.sended_at;

    console.log(data.user_id);
    console.log(user_id);
    if (data.user_id == user_id) {
        message_dev.className = `localuser ${message_dev.className}`;
        console.log(message_dev.className);
    };

    document.querySelector("#id_chat_item_container").appendChild(message_dev);
    scrollMSGBoxToBottom();
};

function scrollMSGBoxToBottom() {
    MESSAGES_BOX.scrollTop = MESSAGES_BOX.scrollHeight;
};

console.log(user_id);
scrollMSGBoxToBottom();