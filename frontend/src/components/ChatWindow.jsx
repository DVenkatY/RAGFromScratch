import React, { useState, useRef, useEffect } from 'react';
import { api } from '../services/api';

const ChatWindow = ({ tableName }) => {
    const [messages, setMessages] = useState([
        { text: "Hello! How can I assist you?", sender: "bot" }
    ]);
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping]);

    const handleSend = async () => {
        if (!input.trim()) return;

        if (!tableName) {
            setMessages(prev => [...prev, { text: "⚠️ Please upload and ingest a document before asking questions!", sender: "bot" }]);
            return;
        }

        const userQuery = input;
        setInput("");
        setMessages(prev => [...prev, { text: userQuery, sender: "user" }]);
        setIsTyping(true);

        try {
            const data = await api.searchAndChat(userQuery, tableName);
            
            let botReply = `${data.answer}\n\n`;
            
            if (data.sources && data.sources.length > 0) {
                botReply += "---\n**Sources:**\n";
                data.sources.forEach((source, idx) => {
                    const page = source.metadata?.page_number || "?";
                    botReply += `* [Page ${page}] Match score: ${(source.similarity * 100).toFixed(1)}%\n`;
                });
            }

            setMessages(prev => [...prev, { text: botReply, sender: "bot" }]);
        } catch (error) {
            setMessages(prev => [...prev, { text: `❌ Error: ${error.message}`, sender: "bot" }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex-1 flex flex-col p-4">
            {/* Header */}
            <div className="bg-blue-600 text-white p-4 rounded-xl shadow">
                <h2 className="text-xl font-semibold">AI Chatbot</h2>
                {tableName && <p className="text-xs text-blue-200 mt-1">Connected: {tableName}</p>}
            </div>

            {/* Chat History */}
            <div className="flex-1 overflow-y-auto mt-4 space-y-3">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`p-3 max-w-[60%] rounded-xl whitespace-pre-wrap ${
                            msg.sender === "user"
                                ? "ml-auto bg-blue-500 text-white"
                                : "bg-white shadow"
                        }`}
                    >
                        {msg.text}
                    </div>
                ))}
                
                {isTyping && (
                    <div className="p-3 max-w-[60%] rounded-xl bg-white shadow italic text-sm text-gray-500">
                        Searching and generating response...
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Chat Input Bar */}
            <div className="flex mt-4 gap-2">
                <input
                    type="text"
                    placeholder={tableName ? "Type your message..." : "Upload a document first..."}
                    className="flex-1 p-3 border rounded-xl focus:outline-none"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    disabled={!tableName || isTyping}
                />
                <button
                    onClick={handleSend}
                    disabled={!tableName || isTyping || !input.trim()}
                    className={`px-4 py-2 rounded-xl transition font-medium ${
                        tableName && input.trim() ? "bg-blue-600 text-white hover:bg-blue-700" : "bg-gray-300 text-gray-500 cursor-not-allowed"
                    }`}
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatWindow;