import os
import zipfile

project_name = "cumple-mensajes"
public_dir = os.path.join(project_name, "public")
os.makedirs(public_dir, exist_ok=True)

files = {
    os.path.join(public_dir, "index.html"): '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Mensajes de Cumpleaños</title>
  <style>
    body { font-family: Arial; background: #fff0f5; padding: 30px; }
    input, textarea { width: 100%; margin: 10px 0; padding: 10px; border: 1px solid #d63384; }
    button { background: #d63384; color: white; padding: 10px; border: none; }
    .card { background: #fff; border: 2px solid #d63384; padding: 10px; margin: 10px 0; cursor: pointer; }
    .card .content { display: none; }
    .card.opened .content { display: block; }
  </style>
</head>
<body>
  <h1>🎂 Deja tu mensaje</h1>
  <form id="messageForm">
    <input type="text" id="name" placeholder="Tu nombre" required />
    <textarea id="message" placeholder="Tu mensaje..." required></textarea>
    <button type="submit">Enviar</button>
  </form>
  <h2>📬 Cartas</h2>
  <div id="messagesContainer"></div>

  <script>
    async function loadMessages() {
      const res = await fetch('/messages');
      const messages = await res.json();
      const container = document.getElementById('messagesContainer');
      container.innerHTML = '';
      messages.reverse().forEach(({ name, message }) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `<strong>De: ${name}</strong><div class="content"><p>${message}</p></div>`;
        card.addEventListener('click', () => card.classList.toggle('opened'));
        container.appendChild(card);
      });
    }

    document.getElementById('messageForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value;
      const message = document.getElementById('message').value;
      await fetch('/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, message })
      });
      document.getElementById('messageForm').reset();
      loadMessages();
    });

    loadMessages();
  </script>
</body>
</html>
''',
    os.path.join(project_name, "server.js"): '''const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'messages.json');

app.use(express.json());
app.use(express.static('public'));

app.get('/messages', (req, res) => {
  const data = fs.existsSync(DATA_FILE) ? JSON.parse(fs.readFileSync(DATA_FILE)) : [];
  res.json(data);
});

app.post('/messages', (req, res) => {
  const { name, message } = req.body;
  if (!name || !message) return res.status(400).send('Faltan datos');

  const messages = fs.existsSync(DATA_FILE) ? JSON.parse(fs.readFileSync(DATA_FILE)) : [];
  messages.push({ name, message, date: new Date() });

  fs.writeFileSync(DATA_FILE, JSON.stringify(messages, null, 2));
  res.status(201).send('Mensaje guardado');
});

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
''',
    os.path.join(project_name, "messages.json"): "[]",
    os.path.join(project_name, "package.json"): '''{
  "name": "cumple-mensajes",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
''',
    os.path.join(project_name, ".gitignore"): "node_modules\n",
    os.path.join(project_name, "README.md"): "# 🎂 App de Mensajes de Cumpleaños\n\nFormulario web para dejar y ver mensajes de cumpleaños como cartas.\n\n## Cómo correr localmente\n\n```bash\nnpm install\nnpm start\n```\n\nLuego abre: http://localhost:3000\n"
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

zip_filename = f"{project_name}.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for folder, _, filenames in os.walk(project_name):
        for filename in filenames:
            file_path = os.path.join(folder, filename)
            zipf.write(file_path, os.path.relpath(file_path, project_name))

print(f"ZIP creado: {zip_filename}")
