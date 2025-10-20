from flask import Flask
from routes.routes import routes
from datetime import datetime

app = Flask(__name__, template_folder='views/html')

# Configuração da secret key do Flask
app.secret_key = 'lumina_admin_secret_key_2024'

@app.context_processor
def inject_now():
    # Injeta a data e hora atual para uso nos templates
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)