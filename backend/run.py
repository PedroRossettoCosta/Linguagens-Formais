from app import create_app

app = create_app()

if __name__ == '__main__':
    print(f"Iniciando o servidor do Compilador Abyssus na porta {app.config['PORT']}...")
    app.run(
        host=app.config['HOST'], 
        port=app.config['PORT'], 
        debug=app.config['DEBUG']
    )