from flask import Flask,request,render_template, redirect

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html",last_updated="2024-06-15 12:00:00")

@app.route('/login-submit', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        return redirect(f'/dashboard/{username}')
    
    return redirect('/')

MOCK_USER_DATA = {
    "subscription": "Premium Individual",
    "playlists": ["Chill Beats", "Coding Lofi", "Late Night Driving"],
    "songs": [
        {"title": "Blinding Lights", "artist": "The Weeknd"},
        {"title": "Starboy", "artist": "The Weeknd"},
        {"title": "Bohemian Rhapsody", "artist": "Queen"}
    ]
}

@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template(
        'dashboard.html', 
        user_name=username,
        subscription_status=MOCK_USER_DATA["subscription"],
        playlists=MOCK_USER_DATA["playlists"],
        songs=MOCK_USER_DATA["songs"]
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)