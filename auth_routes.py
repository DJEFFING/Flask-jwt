from flask import Blueprint, request
import auth_service as auth_serv


auth = Blueprint('auth',__name__)

# Fonction de création d'un nouvelle utilisateur
@auth.route('/register',methods= ['POST'])
def register():
    user  = request.json['user']
    return auth_serv.register(
        email = user["email"],
        password = user["password"],
        username = user["username"],
        phone_number = user["phone_number"]
    )
    

# Fonction de connexion
@auth.route('/login',methods=['POST'])
def login():
    credentials  = request.json['credentials']
    return auth_serv.login(
        email = credentials['email'] ,
        password = credentials['password']
    )


@auth.route('/logout',methods=['POST'])
def logout():
    return auth_serv.logout()

# Rafraichissement des jetons
@auth.route('/regenerate_token',methods=['POST'])
def regenerate_token():
    refresh_token = request.json.get('refresh_token')
    return auth_serv.regenerate_Ttoken(refresh_token = refresh_token)

    