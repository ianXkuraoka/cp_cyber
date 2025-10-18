from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClickSeguro - Agendamento</title>
</head>
<body>
    <h1>ClickSeguro - Sistema de Agendamento</h1>
    <form method="POST" action="/login">
        <label>Usuario:</label>
        <input type="text" name="username"><br>
        <label>Senha:</label>
        <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    {% if message %}
    <p>{{ message|safe }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    # VULNERABILIDADE PROPOSITAL: XSS - sem validacao de entrada
    message = f"Tentativa de login com usuario: {username}"
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
