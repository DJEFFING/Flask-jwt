
const register = document.getElementById("register");
if (register) {
    register.addEventListener("click", (event) => {
        event.preventDefault(); // desactiver le comportemant par defaut de la page

        const email = document.getElementById("email");
        const username = document.getElementById("username");
        const telephone = document.getElementById("telephone");
        const password = document.getElementById("password");

        if (email.value != '' && telephone.value != '' && password.value != '' && username.value != '') {
            registerForm(email, username, telephone, password);
        } else {
            alert("Tous les champs sont obligatoire.")
        }
    })
}


const login = document.getElementById("login");
if(login){
    login.addEventListener("click", (event)=>{
        const email =  document.getElementById("email");
        const password = document.getElementById("password");

        if(email.value !='' && password.value!=''){
            event.preventDefault()

            console.log("Le bouton de connexion!!")
            console.log("email : ", email.value);
            console.log("password : ", password.value);

            loginForm(email, password);
        }




    })
}

const logout =  document.getElementById("logout");
if(logout){
    logout.addEventListener("click",(event)=>{
        fetchLogout(); // Déconnexion.
    });
}

async function registerForm(email, username, telephone, password,) {
    console.log("Email : ", email.value);
    console.log("Username : ", username.value);
    console.log("Telephone : ", telephone.value);
    console.log("Password : ", password.value);

    const newUser = {
        'email': email.value,
        'phone_number': telephone.value,
        'username': username.value,
        'password': password.value
    }
    try {

        const response = await fetchRegisterForm(newUser);

        if (response.status == 201) {
            alert('Utilisateur a été crée avec succes : ', response.message);
            console.log('Utilisateur a été crée avec succes : ', response.message);
        }
    } catch (error) {
        console.log("une erreur c'est produit : ", error);
    }
}

async function loginForm(email, password) {
    try{
        const credentials = {
            'email' : email.value,
            'password' : password.value
        };
    
        reponse = await fetchLoginForm(credentials);
        const data  = await response.json();
        console.log("Connexion reussi : ", data);
    
        //Stacaker les jetons 
        localStorage.setItem('accessToken',data.token.access_token);
        localStorage.setItem('refreshToken',data.token.refresh_token);
    
        // Rediriger l'utilisateur vers la page d'accueil ou une autre page protégée
        window.location.href = "/dashboard";
    }catch(error){
        console.log("une erreur c'est produit : ", error);
        alert('Échec de la connexion. Veuillez vérifier vos informations d\'identification.');
    }
    
}





async function fetchRegisterForm(newUser) {
    try {
        const response = await fetch("http://127.0.0.1:5000//register", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({ 'user': newUser })
        })

        console.log('la reponse du serveur : ', response)

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response

    } catch (error) {
        console.error('Error fetching protected resource:', error);
        throw error;
    }

}


async function fetchLoginForm(credentials) {
   response = await fetch('http://127.0.0.1:5000/login',{
        method:'POST',
        headers:{
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'credentials' : credentials})
   });

   if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }else{
        return response;
    }

}


async function fetchLogout() {
    const response = await fetch("/logout",{
        method:'POST',
        headers:{
            "Content-Type": "application/json",
        }
    });

    if(response.ok){
        const data = response.json();
        console.log(data.message);
        window.location.href = '/login';
    }else{
        throw new Error(" Une erreur c'est produite ",response.status);
    }
}