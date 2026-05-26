import os

class BaseConfig:
    """Configurações bases do servidor Abyssus."""
    DEBUG = False
    TESTING = False
    PORT = int(os.environ.get("PORT", 5000))
    HOST = os.environ.get("HOST", "0.0.0.0")

class DevelopmentConfig(BaseConfig):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True

class ProductionConfig(BaseConfig):
    """Configurações para ambiente de produção (otimizações e logs)."""
    DEBUG = False

class TestingConfig(BaseConfig):
    """Configurações isoladas para testes automatizados."""
    TESTING = True
    DEBUG = True

def get_config():
    """Resolve dinamicamente qual classe de configuração usar com base no ambiente."""
    env = os.environ.get("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    return DevelopmentConfig
