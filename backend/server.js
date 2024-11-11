const express = require('express');
const cors = require('cors');
const { generateContent } = require('./geminiService');

const app = express();
const PORT = 5000; // This port should match your Angular `environment.ts` settings

app.use(cors());
app.use(express.json());

app.post('/api/generate', async (req, res) => {
    try {
        const { prompt } = req.body;
        if (!prompt) {
            return res.status(400).json({ error: 'Prompt is required' });
        }

        const response = await generateContent(prompt);
        res.json({ response });
    } catch (error) {
        res.status(500).json({ error: 'Error generating content' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
