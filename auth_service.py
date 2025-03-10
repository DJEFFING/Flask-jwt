import jwt
from datetime import datetime, timedelta
from functools import wraps
from  models import User,Token,db
from main import bcrypt
from config import Config
from flask import jsonify, make_response,request,redirect,url_for


# Verification des jetons
def token_required(func):
    @wraps(func)
    def decoded(*args, **kargs):
        # token = request.headers.get('Authorization')
        access_token = f"Bearer {request.cookies.get("access_token")}" # ✅ Récupérer le token depuis le cookie
        refresh_token = request.cookies.get("refresh_token")  # ✅ Récupérer le refresh_token
        
        if not access_token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            
            access_token = access_token.split(" ")[1] #Supprime le mot bearer
            payload = jwt.decode(access_token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']  # Supposons que l'ID de l'utilisateur est stocké dans 'user_id'
        
        except jwt.ExpiredSignatureError:
             # 🔄 Si l'access_token est expiré, on tente d'utiliser le refresh_token
            return regenerate_token(refresh_token = refresh_token)
            # return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            print(f"Erreur lors de la vérification du token: {e}")
            return jsonify({'message': 'Token error'}), 500
        return func(user_id,*args, **kargs)

    return decoded


# Fonction de création d'un nouvelle utilisateur
def register( email, password, username=None, phone_number=None, profil_url=None, description=None):
    newUser = User(
        email=email,
        password = password,
        username = username,
        phone_number = phone_number,
        profil_url = profil_url,
        description = description,
    )
    db.session.add(newUser)
    db.session.commit()
    return jsonify({'message':'utilisateur crée avec succès!'}), 201




# Fonction de connexion
def login(email, password):
    user = User.query.filter_by(email = email).first()
    if user and bcrypt.check_password_hash(user.password , password = password) :
        return generate_token(user_id = user.id, email = user.email, username = user.username)
    else:
        return make_response('Unable to verify',403, {'WWW-Authenticate': 'Basic realm : "Authentication Failed!"'})


# Fonction de deconnexion
def logout():
    refresh_token = request.cookies.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token missing'}), 400
    try:
        # Invalider le jeton de rafraîchissement (liste noire ou suppression de la base de données)
        # invalidate_refresh_token(refresh_token) # fonction a implémenter
        
        response = make_response(jsonify({'message':"deconnection reussie"}),200)
        
        # Supprimer les cookies en mettant une expiration passée
        response.set_cookie("access_token", "", expires=0, httponly=True, samesite="Strict")
        response.set_cookie("refresh_token", "", expires=0, httponly=True, samesite="Strict")
        
        return response
    
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la déconnexion: {e}")
        return jsonify({'message': 'Déconnexion error'}), 500


# Generation des jetons
def generate_token(user_id,email,username):

    #Generate Acces Token
    access_token = jwt.encode({
        'user_id': user_id,
        'email' : email,
        'username' : username,
        'exp' : datetime.utcnow() + timedelta(seconds=60)
    },Config.SECRET_KEY,algorithm='HS256')

    # Jeton de rafraîchissement (Refresh Token)
    refresh_token = jwt.encode({
        'user_id': user_id,
        'email' : email,
        'username' : username,
        'exp' : datetime.utcnow() + timedelta(days=30)
    },Config.REFRESH_TOKEN,algorithm='HS256')

    new_refresh_token = Token(token = refresh_token)
    db.session.add(new_refresh_token) # Ajout du nouveau token a la liste des token
    db.session.commit()
    token = {
        'access_token': access_token, 
        'refresh_token': refresh_token
    }

    response = make_response(jsonify({"message ": "Connexion réussie","token": token}), 200)
    response.set_cookie("access_token",access_token, httponly=True,samesite="Strict") # 🔥 Cookie sécurisé
    response.set_cookie("refresh_token",refresh_token,httponly=True,samesite="Strict")
    return response



# Rafraichissement des jetons
def regenerate_token(refresh_token):
        
    refresh_token_db = Token.query.filter_by( token =  refresh_token).first()

    if not refresh_token or not refresh_token_db:
        return jsonify({'message':'Refresh token missing'}),400
    try:
        paload = jwt.decode(refresh_token, Config.REFRESH_TOKEN,algorithms=['HS256'])
        user_id = paload['user_id']
        email = paload['email']
        username = paload['username']

        # Regenerate Acces Token
        access_token = jwt.encode({
            'user_id': user_id,
            'email' : email,
            'username' : username,
            'exp' : datetime.utcnow() + timedelta(seconds=600)
        }, Config.SECRET_KEY,algorithm='HS256')
        print("------------------ nouveau token ----------------------")

        # response = make_response(jsonify({'message':'token reinitaliser','access_token': access_token},200))
        response = make_response()
        response.set_cookie("access_token",access_token, httponly=True,samesite="Strict") # 🔥 Cookie sécurisé
        return response
    
    except jwt.ExpiredSignatureError:
        return redirect(url_for('main.login'))
        # return jsonify({'message': 'Refresh token expired'}), 401
    
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401
    
    except Exception as e:
        print(f"Erreur lors du rafraîchissement du token: {e}")
        return jsonify({'message': 'Refresh token error'}), 500


def invalidate_refresh_token(refresh_token):
    refresh_token = Token.query.filter_by( token = refresh_token).first()
    db.session.delete(refresh_token)
    db.session.commit()
    
