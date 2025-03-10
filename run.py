from main import create_app, db
from models import init_db

app =  create_app()

if __name__ == "__main__":
    # with app.app_context():
    #     init_db()
    #     db.create_all()
    #     print("La base de donnée a été crée -----------------------")
    app.run(debug = True)