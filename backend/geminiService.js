require('dotenv').config();
const { GoogleGenerativeAI } = require("@google/generative-ai");

// Ensure the API key is set and logged for debugging
if (!process.env.GEMINI_API_KEY) {
    console.error('GEMINI_API_KEY is not defined. Make sure it is set in the .env file.');
    process.exit(1);
}

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const generateContent = async (prompt) => {
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContent(prompt);
        return result.response.text();
    } catch (error) {
        console.error("Error generating content:", error);
        throw error;
    }
};

module.exports = { generateContent };
