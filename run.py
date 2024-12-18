from app import create_app

app = create_app()

if __name__ == '__main__':
    # Lancement en mode debug pour le développement
    app.run(host='0.0.0.0', port=5000, debug=True)
