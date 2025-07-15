
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const OpenAI = require('openai');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});


app.post('/api/recomendar-perfume', async (req, res) => {
  try {
    const { prompt } = req.body;

    const completion = await openai.createChatCompletion({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'Você é um especialista em perfumes.' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 300,
    });

    res.json({ text: completion.data.choices[0].message.content });
  } catch (error) {
    console.error('Erro:', error.message || error);
    res.status(500).json({ error: 'Erro ao gerar recomendação' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
