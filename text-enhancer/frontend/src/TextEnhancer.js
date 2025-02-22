import React, { useState } from "react";
import axios from "axios";
import "./TextEnhancer.css";

const TextEnhancer = () => {
    const [text, setText] = useState("");
    const [tone, setTone] = useState("formal");
    const [enhancedText, setEnhancedText] = useState("");
    const [translatedText, setTranslatedText] = useState("");
    const [selectedLanguage, setSelectedLanguage] = useState("en");
    const [loading, setLoading] = useState(false);

    const tones = ["formal", "casual", "sarcastic", "poetic", "happy", "sad"];
    const languages = [
        { code: "en", name: "English" },
        { code: "hi", name: "Hindi" },
        { code: "te", name: "Telugu" },
        { code: "ta", name: "Tamil" },
        { code: "kn", name: "Kannada" },
        { code: "mr", name: "Marathi" },
    ];

    const handleEnhance = async () => {
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:8000/enhance", { text, tone });
            setEnhancedText(response.data.enhanced_text);
        } catch (error) {
            console.error("Error enhancing text:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleTranslate = async () => {
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:8000/translate", { 
                text: enhancedText, 
                language: selectedLanguage 
            });
            setTranslatedText(response.data.translated_text);
        } catch (error) {
            console.error("Error translating text:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSpeak = async (text, lang) => {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        synth.speak(utterance);
    };

    const handleServerSpeak = async (text, lang) => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/speak", { text, language: lang }, { responseType: "blob" });
            const audioUrl = URL.createObjectURL(response.data);
            const audio = new Audio(audioUrl);
            audio.play();
        } catch (error) {
            console.error("Error generating speech:", error);
        }
    };

    return (
        <div className="container">
            <h1>AI-Powered Text Enhancer</h1>
            <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Enter text..." />

            <label>Select Tone:</label>
            <select value={tone} onChange={(e) => setTone(e.target.value)}>
                {tones.map((tone) => (
                    <option key={tone} value={tone}>{tone.charAt(0).toUpperCase() + tone.slice(1)}</option>
                ))}
            </select>

            <button className="enhance-btn" onClick={handleEnhance}>Enhance</button>

            <h2>Enhanced Text:</h2>
            <p>{loading ? "Generating..." : enhancedText}</p>
            {enhancedText && (
                <button onClick={() => handleSpeak(enhancedText, "en")}>🔊 Speak</button>
            )}

            <label>Select Language for Translation:</label>
            <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)}>
                {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                ))}
            </select>

            <button className="translate-btn" onClick={handleTranslate}>Translate</button>

            <h2>Translated Text:</h2>
            <p>{loading ? "Translating..." : translatedText}</p>
            {/* {translatedText && (
                <button onClick={() => handleSpeak(translatedText, selectedLanguage)}>🔊 Speak (Local)</button>
            )} */}
            {translatedText && (
                <button onClick={() => handleServerSpeak(translatedText, selectedLanguage)}>🔊 Speak (Server)</button>
            )}
        </div>
    );
};

export default TextEnhancer;
