import express from 'express';
import fs from 'fs';
import cors from 'cors';
import path from 'path';

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const dbPath = './backend/db.json';

app.post('/api/login', (req, res) => {
  const { email, senha } = req.body;
  const data = JSON.parse(fs.readFileSync(dbPath));
  const usuario = data.usuarios.find(u => u.email === email && u.senha === senha);

  if (!usuario) return res.status(401).json({ erro: 'Credenciais inválidas' });

  const diasRestantes = Math.ceil(
    (new Date(usuario.validade) - new Date()) / (1000 * 60 * 60 * 24)
  );

  res.json({
    nome: usuario.nome,
    plano: usuario.plano,
    diasRestantes: diasRestantes >= 0 ? diasRestantes : 0
  });
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
