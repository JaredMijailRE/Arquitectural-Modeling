import os, textwrap

def generate_database(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'init.sql'), 'w') as f:
        f.write(textwrap.dedent("""
            CREATE TABLE IF NOT EXISTS systems (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255)
            );
            """
    ).strip())
        
def generate_backend(name, database):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            from flask import Flask, request, jsonify
            import mysql.connector
            
            app = Flask(__name__)
            
            @app.route('/create', methods=['POST'])
            def create():
                data = request.json
                conn = mysql.connector.connect(
                    host='{database}',
                    user='root',
                    password='root',
                    database='{database}'
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO systems (name) VALUES (%s)", (data['name'],))
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify(status="created")
            
            @app.route('/systems')
            def get_systems():
                conn = mysql.connector.connect(
                    host='{database}',
                    user='root',
                    password='root',
                    database='{database}'
                )
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM systems")
                rows = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify(systems=rows)
            
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=80)
            """
        ).strip())
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            RUN pip install flask mysql-connector-python
            CMD ["python", "app.py"]
            """
        ).strip())
        
def generate_frontend(name, backend):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'package.json'), 'w') as f:
        f.write(textwrap.dedent("""
            {
                "name": "frontend",
                "version": "1.0.0",
                "main": "app.js",
                "dependencies": {
                    "express": "^4.18.2",
                    "axios": "^1.6.7"
                }
            }
            """
        ).strip())
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM node:18
            WORKDIR /app
            COPY . .
            RUN npm install
            CMD ["node", "app.js"]
            """
        ).strip())
    with open(os.path.join(path, 'app.js'), 'w') as f:
        f.write(textwrap.dedent(f"""
            const express = require('express');
            const axios = require('axios');
            const app = express();
            
            app.use(express.json());
            app.use(express.urlencoded({{ extended: true }}));
            
            const BACKEND_URL = 'http://{backend}:80';
            
            app.get('/', async (req, res) => {{
                try {{
                    const response = await axios.get(`${{BACKEND_URL}}/systems`);
                    const systems = response.data.systems;
                    let list = systems.map(([id, name]) => `<li>${{name}}</li>`).join('');
                    res.send(`
                        <html>
                        <body>
                            <h1>Frontend</h1>
                            <form method="POST" action="/create">
                                <input name="name" />
                                <button type="submit">Create</button>
                            </form>
                            <ul>${{list}}</ul>
                        </body>
                        </html>
                    `);
                }} catch (err) {{
                    res.status(500).send("Error contacting backend");
                }}
            }});
            
            app.post('/create', async (req, res) => {{
                const name = req.body.name;
                await axios.post(`${{BACKEND_URL}}/create`, {{ name }});
                res.redirect('/');
            }});
            
            app.listen(80, () => console.log("Frontend running on port 80"));
            """
        ).strip())
        
def generate_frontend2(name, backend):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'package.json'), 'w') as f:
        f.write(textwrap.dedent("""
            {
                "name": "frontend",
                "version": "1.0.0",
                "main": "app.js",
                "dependencies": {
                    "express": "^4.18.2",
                    "axios": "^1.6.7"
                }
            }
            """
        ).strip())
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM node:18
            WORKDIR /app
            COPY . .
            RUN npm install
            CMD ["node", "app.js"]
            """
        ).strip())
    with open(os.path.join(path, 'app.js'), 'w') as f:
        f.write(textwrap.dedent(f"""
            const express = require('express');
            const axios = require('axios');
            const app = express();
            
            app.use(express.json());
            app.use(express.urlencoded({{ extended: true }}));
            
            const BACKEND_URL = 'http://{backend}:80';
            
            app.get('/', async (req, res) => {{
                try {{
                    const response = await axios.get(`${{BACKEND_URL}}/systems`);
                    const systems = response.data.systems;
                    let list = systems.map(([id, name]) => `
                        <div class="system-item">
                            <span class="system-icon">🔷</span>
                            <span class="system-name">${{name}}</span>
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
                                * {{
                                    margin: 0;
                                    padding: 0;
                                    box-sizing: border-box;
                                }}
                                
                                body {{
                                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    min-height: 100vh;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    padding: 20px;
                                }}
                                
                                .container {{
                                    background: white;
                                    border-radius: 20px;
                                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                                    padding: 40px;
                                    max-width: 600px;
                                    width: 100%;
                                    animation: fadeIn 0.5s ease-in;
                                }}
                                
                                @keyframes fadeIn {{
                                    from {{ opacity: 0; transform: translateY(-20px); }}
                                    to {{ opacity: 1; transform: translateY(0); }}
                                }}
                                
                                h1 {{
                                    color: #667eea;
                                    font-size: 2.5em;
                                    margin-bottom: 10px;
                                    text-align: center;
                                }}
                                
                                .subtitle {{
                                    text-align: center;
                                    color: #666;
                                    margin-bottom: 30px;
                                    font-size: 1.1em;
                                }}
                                
                                .form-section {{
                                    background: #f8f9fa;
                                    padding: 25px;
                                    border-radius: 15px;
                                    margin-bottom: 30px;
                                }}
                                
                                form {{
                                    display: flex;
                                    gap: 10px;
                                }}
                                
                                input[name="name"] {{
                                    flex: 1;
                                    padding: 15px 20px;
                                    border: 2px solid #e0e0e0;
                                    border-radius: 10px;
                                    font-size: 1em;
                                    transition: all 0.3s ease;
                                }}
                                
                                input[name="name"]:focus {{
                                    outline: none;
                                    border-color: #667eea;
                                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                                }}
                                
                                button {{
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
                                }}
                                
                                button:hover {{
                                    transform: translateY(-2px);
                                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                                }}
                                
                                button:active {{
                                    transform: translateY(0);
                                }}
                                
                                .systems-section {{
                                    margin-top: 20px;
                                }}
                                
                                .section-title {{
                                    color: #333;
                                    font-size: 1.3em;
                                    margin-bottom: 15px;
                                    font-weight: 600;
                                }}
                                
                                .systems-list {{
                                    display: flex;
                                    flex-direction: column;
                                    gap: 10px;
                                }}
                                
                                .system-item {{
                                    background: white;
                                    padding: 15px 20px;
                                    border-radius: 10px;
                                    display: flex;
                                    align-items: center;
                                    gap: 15px;
                                    border: 2px solid #e0e0e0;
                                    transition: all 0.3s ease;
                                    animation: slideIn 0.3s ease-out;
                                }}
                                
                                @keyframes slideIn {{
                                    from {{ opacity: 0; transform: translateX(-20px); }}
                                    to {{ opacity: 1; transform: translateX(0); }}
                                }}
                                
                                .system-item:hover {{
                                    border-color: #667eea;
                                    transform: translateX(5px);
                                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
                                }}
                                
                                .system-icon {{
                                    font-size: 1.5em;
                                }}
                                
                                .system-name {{
                                    font-size: 1.1em;
                                    color: #333;
                                    font-weight: 500;
                                }}
                                
                                .empty-state {{
                                    text-align: center;
                                    padding: 40px;
                                    color: #999;
                                    font-style: italic;
                                }}
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
                                        ${{list || '<div class="empty-state">No systems yet. Create your first one!</div>'}}
                                    </div>
                                </div>
                            </div>
                        </body>
                        </html>
                    `);
                }} catch (err) {{
                    res.status(500).send(`
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100vh;
                                    background: #f44336;
                                    color: white;
                                    margin: 0;
                                }}
                                .error {{
                                    text-align: center;
                                    padding: 40px;
                                    background: rgba(0,0,0,0.2);
                                    border-radius: 10px;
                                }}
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
                }}
            }});
            
            app.post('/create', async (req, res) => {{
                const name = req.body.name;
                await axios.post(`${{BACKEND_URL}}/create`, {{ name }});
                res.redirect('/');
            }});
            
            app.listen(80, () => console.log("Frontend running on port 80"));
            """
        ).strip())

def generate_docker_compose(components):
    path = f'skeleton/'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'docker-compose.yml'), 'w') as f:
        sorted_components = dict(sorted(components.items(), key=lambda
        item: 0 if item[1] == "database" else 1))
        f.write("services:\n")
        db = None
        for i, (name, ctype) in enumerate(sorted_components.items()):
            port = 8000 + i
            f.write(f"  {name}:\n")
            if ctype == "database":
                db = name
                f.write("    image: mysql:8\n")
                f.write("    environment:\n")
                f.write("      - MYSQL_ROOT_PASSWORD=root\n")
                f.write(f"      - MYSQL_DATABASE={name}\n")
                f.write("    volumes:\n")

                f.write(f"      - ./{name}/init.sql:/docker-entrypoint-initdb.d/init.sql\n")

                f.write("    ports:\n")
                f.write("      - '3306:3306'\n")
            else:
                f.write(f"    build: ./{name}\n")
                f.write(f"    ports:\n      - '{port}:80'\n")
                if ctype== "backend":
                    f.write(f"    depends_on:\n      - {db}\n")
        f.write("\nnetworks:\n  default:\n    driver: bridge\n")

def apply_transformations(model):
    components = {}
    backend_name = None
    database_name = None
    for e in model.elements:
        if e.__class__.__name__ == 'Component':
            if e.type == 'backend':
                backend_name = e.name
            elif e.type == 'database':
                database_name = e.name
    for e in model.elements:
        if e.__class__.__name__ == 'Component':
            components[e.name] = e.type
        if e.type == 'database':
            generate_database(e.name)
        if e.type == 'backend':
            generate_backend(e.name, database=database_name)
        elif e.type == 'frontend':
            generate_frontend(e.name, backend=backend_name)
        elif e.type == 'frontend2':
            generate_frontend2(e.name, backend=backend_name)
    generate_docker_compose(components)