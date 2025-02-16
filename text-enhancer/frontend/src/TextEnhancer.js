import React, { useState } from "react";
import axios from "axios";
import "./TextEnhancer.css";

const TextEnhancer = () => {
    const [text, setText] = useState("");
    const [tone, setTone] = useState("formal");
    const [enhancedText, setEnhancedText] = useState("");

    const handleEnhance = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/enhance", { 
                text, 
                tone 
            });
            setEnhancedText(response.data.enhanced_text);
        } catch (error) {
            console.error("Error enhancing text:", error);
        }
    };

    return (
        <div className="container">
            <h1>AI-Powered Text Enhancer</h1>
            <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Enter text..." />
            <select onChange={(e) => setTone(e.target.value)}>
                <option value="formal">Formal</option>
                <option value="casual">Casual</option>
                <option value="sarcastic">Sarcastic</option>
                <option value="poetic">Poetic</option>
            </select>
            <button onClick={handleEnhance}>Enhance</button>
            <h2>Enhanced Text:</h2>
            <p>{enhancedText}</p>
        </div>
    );
};

export default TextEnhancer;
