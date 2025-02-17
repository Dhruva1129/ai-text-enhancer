import React, { useState } from "react";
import axios from "axios";
import "./TextEnhancer.css";

const TextEnhancer = () => {
    const [text, setText] = useState("");
    const [tone, setTone] = useState("formal");
    const [enhancedText, setEnhancedText] = useState("");
    const [loading, setLoading] = useState(false);

    const handleEnhance = async () => {
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:8000/enhance", { 
                text, 
                tone 
            });
            setEnhancedText(response.data.enhanced_text);
        } catch (error) {
            console.error("Error enhancing text:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>AI-Powered Text Enhancer</h1>
            <textarea 
                value={text} 
                onChange={(e) => setText(e.target.value)} 
                placeholder="Enter text..." 
            />
            <div className="tone-buttons">
                <button className={tone === "formal" ? "active" : ""}  onClick={() => setTone("formal")}>Formal</button>
                <button className={tone === "casual" ? "active" : ""} onClick={() => setTone("casual")}>Casual</button>
                <button className={tone === "sarcastic" ? "active" : ""} onClick={() => setTone("sarcastic")}>Sarcastic</button>
                <button className={tone === "poetic" ? "active" : ""} onClick={() => setTone("poetic")}>Poetic</button>
            </div>
            <button className="enhace-btn" onClick={handleEnhance}>Enhance</button>
            <h2>Enhanced Text:</h2>
            <p>{loading ? "Generating..." : enhancedText}</p>
        </div>
    );
};

export default TextEnhancer;
