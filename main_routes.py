from flask import Blueprint, request, render_template
from auth_service import token_required

main = Blueprint('main',__name__)

@main.route('/')

def register():
    return render_template('register.html')

@main.route('/login', methods =  ['GET'])
def login():
    return render_template('login.html')

@main.route('/dashboard')
@token_required
def dashboard(user_id):
    return render_template('dashboard.html',user_id = user_id)


@main.route('/dashboard/view')
def show_dashboard():
    return render_template('dashboard.html')  # Affiche la page HTML