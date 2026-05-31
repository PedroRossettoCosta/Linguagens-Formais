from flask import Flask
from flask_cors import CORS
from app.config import get_config

def create_app():
    app = Flask(__name__)
    
    # Carrega a configuração dinâmica com base no ambiente
    config_obj = get_config()
    app.config.from_object(config_obj)
    
    # Configura CORS para permitir chamadas seguras da IDE no Frontend
    CORS(app)
    
    # Registro de Blueprints de rotas
    from app.routes.compiler import compiler_bp
    app.register_blueprint(compiler_bp)
    
    return app
