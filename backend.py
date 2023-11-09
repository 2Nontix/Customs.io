from flask import Flask, request, jsonify, make_response, url_for, redirect, session
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.secret_key = 'BenutzerPass123'  # Geheimer SChlüssel für die Session

users = {'admin': 'password'}  # Admin-Account 
user_list = [{'username': 'admin', 'password': 'password'}]  # Admin-Account in Liste einfügen



@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print(f"Received username: {username} and password: {password}") # Ausgabe der Anmeldedaten in der Konsole

        # Überprüfen Sie, ob die Anmeldedaten gesendet wurden
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password are required'})

        # Überprüfen Sie, ob der Benutzer in der Benutzerliste existiert
        if users.get(username) == password:
            session['username'] = username # Speichern Sie den Benutzernamen in der Sitzung
            return redirect(url_for('homepage'))  # Umleitung zur Homepage hinzugefügt
        else:
            print(f"Stored password for {username}: {users.get(username)}") # Ausgabe des Passworts in der Konsole
            return jsonify({'success': False, 'error': 'Incorrect username or password'})
    else:
        response = make_response("Diese Route wird zur Anmeldung verwendet", 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    
    

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username in users:
            return jsonify({'success': False, 'error': 'Username already taken'})
        else:
            users[username] = password
            user_list.append({'username': username, 'password': password})
            return jsonify({'success': True})
    else:
        response = make_response("Diese Route wird zur Registrierung verwendet", 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
  

  
@app.route('/users', methods=['GET'])             #User Liste bekommen
def get_users():
    print("Current users: ", user_list)
    return jsonify(user_list)



@app.route('/homepage')                         #Neue Route für die Homepage
def homepage():
    username = session.get('username', 'Guest')          #Benutzername aus der Session holen
    return "Willkommen auf der Homepage"
    

 
    
    
    
    
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
