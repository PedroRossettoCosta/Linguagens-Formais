import os

class Config:
    """Configurações base do servidor Abyssus."""
    # Ativa o reload automático se o código mudar (ideal para desenvolvimento)
    DEBUG = True 
    
    # Define a porta (usa a do sistema ou 5000 como padrão)
    PORT = int(os.environ.get("PORT", 5000))
    
    # Define o host (0.0.0.0 permite que outras máquinas na rede acessem)
    HOST = os.environ.get("HOST", "0.0.0.0")