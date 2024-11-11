import React, { useState } from 'react';
import getGeneratedContent from '../../backend/geminiService';

const YourComponent = () => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');

    const handleGenerate = async () => {
        try {
            const result = await getGeneratedContent(prompt);
            setResponse(result);
        } catch (error) {
            console.error("Error:", error);
            setResponse("An error occurred while generating content.");
        }
    };

    return (
        <div>
            <h1>Gemini AI Text Generator</h1>
            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your prompt here..."
            />
            <button onClick={handleGenerate}>Generate</button>
            {response && (
                <div>
                    <h2>Generated Content:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default YourComponent;
