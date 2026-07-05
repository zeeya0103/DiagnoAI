import { useState } from "react";
import axios from "../api/axios";
import { FaRobot, FaPaperPlane } from "react-icons/fa";

function ChatWidget() {

    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        {
            sender: "AI",
            text: "Hello! I'm DIAGNOAI. How can I help you today?"
        }
    ]);

    const sendMessage = async () => {

        if (!message.trim()) return;

        const userMessage = {
            sender: "You",
            text: message
        };

        setMessages(prev => [...prev, userMessage]);

        try {

            const res = await axios.post("/chatbot", {
                message
            });

            setMessages(prev => [
                ...prev,
                {
                    sender: "AI",
                    text: res.data.reply
                }
            ]);

        } catch {

            setMessages(prev => [
                ...prev,
                {
                    sender: "AI",
                    text: "Unable to connect to AI."
                }
            ]);

        }

        setMessage("");

    };

    return (

        <div className="card">

            <h2 style={{color:"#d62828"}}>

                <FaRobot/> AI Chat

            </h2>

            <div
                style={{
                    height:"350px",
                    overflowY:"auto",
                    marginTop:"20px",
                    marginBottom:"20px"
                }}
            >

                {

                    messages.map((msg,index)=>(

                        <div
                            key={index}
                            style={{
                                background:
                                msg.sender==="AI"
                                ? "#fff8dc"
                                : "#1976d2",
                                color:
                                msg.sender==="AI"
                                ? "#000"
                                : "#fff",
                                padding:"12px",
                                marginBottom:"10px",
                                borderRadius:"10px"
                            }}
                        >

                            <b>{msg.sender}</b>

                            <br/>

                            {msg.text}

                        </div>

                    ))

                }

            </div>

            <div
                style={{
                    display:"flex",
                    gap:"10px"
                }}
            >

                <input
                    value={message}
                    onChange={(e)=>setMessage(e.target.value)}
                    placeholder="Ask something..."
                />

                <button
                    className="primary-btn"
                    onClick={sendMessage}
                >
                    <FaPaperPlane/>
                </button>

            </div>

        </div>

    );

}

export default ChatWidget;