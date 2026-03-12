const API = "https://ridecare-chatbot.onrender.com/chat"

const session_id = "web_widget_user"
const phone = "9999999999"

/* Floating button */

const button = document.createElement("div")

button.innerText = "💬"

button.style.position = "fixed"
button.style.bottom = "20px"
button.style.right = "20px"
button.style.background = "#ffcc00"
button.style.width = "60px"
button.style.height = "60px"
button.style.borderRadius = "50%"
button.style.display = "flex"
button.style.alignItems = "center"
button.style.justifyContent = "center"
button.style.cursor = "pointer"
button.style.fontSize = "25px"
button.style.boxShadow = "0 4px 10px rgba(0,0,0,0.3)"

document.body.appendChild(button)

/* Chat container */

const chat = document.createElement("div")

chat.style.position = "fixed"
chat.style.bottom = "100px"
chat.style.right = "20px"
chat.style.width = "320px"
chat.style.height = "420px"
chat.style.background = "#1e1e1e"
chat.style.color = "white"
chat.style.borderRadius = "10px"
chat.style.display = "none"
chat.style.flexDirection = "column"
chat.style.boxShadow = "0 8px 20px rgba(0,0,0,0.4)"

document.body.appendChild(chat)

/* Header */

const header = document.createElement("div")
header.innerText = "RideCare Assistant"
header.style.padding = "10px"
header.style.background = "#333"
header.style.fontWeight = "bold"

chat.appendChild(header)

/* Messages */

const messages = document.createElement("div")

messages.style.flex = "1"
messages.style.padding = "10px"
messages.style.overflowY = "auto"

chat.appendChild(messages)

/* Input area */

const inputArea = document.createElement("div")
inputArea.style.display = "flex"

const input = document.createElement("input")

input.placeholder = "Describe your bike issue..."
input.style.flex = "1"
input.style.padding = "10px"
input.style.border = "none"

const send = document.createElement("button")
send.innerText = "Send"
send.style.padding = "10px"

inputArea.appendChild(input)
inputArea.appendChild(send)

chat.appendChild(inputArea)

/* Toggle chat */

button.onclick = () => {

    chat.style.display = chat.style.display === "none" ? "flex" : "none"

}

/* Add message bubble */

function addMessage(text, sender){

    const bubble = document.createElement("div")

    bubble.innerText = text

    bubble.style.margin = "8px"
    bubble.style.padding = "8px 12px"
    bubble.style.borderRadius = "8px"
    bubble.style.maxWidth = "80%"

    if(sender === "user"){
        bubble.style.background = "#4fc3f7"
        bubble.style.alignSelf = "flex-end"
    } else {
        bubble.style.background = "#555"
        bubble.style.alignSelf = "flex-start"
    }

    messages.appendChild(bubble)

    messages.scrollTop = messages.scrollHeight

}

/* Typing indicator */

function typingIndicator(){

    const typing = document.createElement("div")

    typing.innerText = "Bot is typing..."

    typing.id = "typing"

    typing.style.fontSize = "12px"
    typing.style.opacity = "0.7"

    messages.appendChild(typing)

    messages.scrollTop = messages.scrollHeight

}

/* Remove typing */

function removeTyping(){

    const typing = document.getElementById("typing")

    if(typing) typing.remove()

}

/* Send message */

async function sendMessage(){

    const text = input.value

    if(!text) return

    addMessage(text,"user")

    input.value=""

    typingIndicator()

    const res = await fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            text:text,
            session_id:session_id,
            phone:phone
        })
    })

    const data = await res.json()

    removeTyping()

    addMessage(data.reply,"bot")

}

send.onclick = sendMessage

/* Enter to send */

input.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        sendMessage()
    }

})

/* Welcome message */

setTimeout(()=>{
    addMessage("Hello! I can help diagnose your bike issues or book a service.", "bot")
},1000)

