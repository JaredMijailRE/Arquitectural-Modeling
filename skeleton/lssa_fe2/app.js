const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const BACKEND_URL = 'http://lssa_be:80';

app.get('/', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/systems`);
        const systems = response.data.systems;
        let list = systems.map(([id, name]) => `
            <div class="system-item">
                <span class="system-icon">🔷</span>
                <span class="system-name">${name}</span>
            </div>
        `).join('');
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>System Manager</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }

                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }

                    .container {
                        background: white;
                        border-radius: 20px;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                        padding: 40px;
                        max-width: 600px;
                        width: 100%;
                        animation: fadeIn 0.5s ease-in;
                    }

                    @keyframes fadeIn {
                        from { opacity: 0; transform: translateY(-20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }

                    h1 {
                        color: #667eea;
                        font-size: 2.5em;
                        margin-bottom: 10px;
                        text-align: center;
                    }

                    .subtitle {
                        text-align: center;
                        color: #666;
                        margin-bottom: 30px;
                        font-size: 1.1em;
                    }

                    .form-section {
                        background: #f8f9fa;
                        padding: 25px;
                        border-radius: 15px;
                        margin-bottom: 30px;
                    }

                    form {
                        display: flex;
                        gap: 10px;
                    }

                    input[name="name"] {
                        flex: 1;
                        padding: 15px 20px;
                        border: 2px solid #e0e0e0;
                        border-radius: 10px;
                        font-size: 1em;
                        transition: all 0.3s ease;
                    }

                    input[name="name"]:focus {
                        outline: none;
                        border-color: #667eea;
                        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                    }

                    button {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 10px;
                        font-size: 1em;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    }

                    button:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                    }

                    button:active {
                        transform: translateY(0);
                    }

                    .systems-section {
                        margin-top: 20px;
                    }

                    .section-title {
                        color: #333;
                        font-size: 1.3em;
                        margin-bottom: 15px;
                        font-weight: 600;
                    }

                    .systems-list {
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                    }

                    .system-item {
                        background: white;
                        padding: 15px 20px;
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        gap: 15px;
                        border: 2px solid #e0e0e0;
                        transition: all 0.3s ease;
                        animation: slideIn 0.3s ease-out;
                    }

                    @keyframes slideIn {
                        from { opacity: 0; transform: translateX(-20px); }
                        to { opacity: 1; transform: translateX(0); }
                    }

                    .system-item:hover {
                        border-color: #667eea;
                        transform: translateX(5px);
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
                    }

                    .system-icon {
                        font-size: 1.5em;
                    }

                    .system-name {
                        font-size: 1.1em;
                        color: #333;
                        font-weight: 500;
                    }

                    .empty-state {
                        text-align: center;
                        padding: 40px;
                        color: #999;
                        font-style: italic;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 System Manager</h1>
                    <p class="subtitle">Create and manage your systems</p>

                    <div class="form-section">
                        <form method="POST" action="/create">
                            <input name="name" placeholder="Enter system name..." required />
                            <button type="submit">✨ Create</button>
                        </form>
                    </div>

                    <div class="systems-section">
                        <h2 class="section-title">📋 Your Systems</h2>
                        <div class="systems-list">
                            ${list || '<div class="empty-state">No systems yet. Create your first one!</div>'}
                        </div>
                    </div>
                </div>
            </body>
            </html>
        `);
    } catch (err) {
        res.status(500).send(`
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background: #f44336;
                        color: white;
                        margin: 0;
                    }
                    .error {
                        text-align: center;
                        padding: 40px;
                        background: rgba(0,0,0,0.2);
                        border-radius: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="error">
                    <h1>⚠️ Error</h1>
                    <p>Error contacting backend</p>
                </div>
            </body>
            </html>
        `);
    }
});

app.post('/create', async (req, res) => {
    const name = req.body.name;
    await axios.post(`${BACKEND_URL}/create`, { name });
    res.redirect('/');
});

app.listen(80, () => console.log("Frontend running on port 80"));