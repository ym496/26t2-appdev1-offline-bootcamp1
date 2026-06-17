from flask import Flask,request,render_template, redirect

app = Flask(__name__)


USER_PROFILES = {
    "cly": {
        "name": "clyrmze",
        "tier": "Premium Individual",
        "favorites": [
            {"title": "Blinding Lights", "artist": "The Weeknd"},
            {"title": "Bohemian Rhapsody", "artist": "Queen"}
        ]
    }
}

ARTIST_CATALOGS = {
    "the-weeknd": [
        {"title": "Blinding Lights", "genre": "Pop", "streams": "3.4 Billion"},
        {"title": "Starboy", "genre": "R&B", "streams": "2.9 Billion"}
    ]
}

ADMIN_METRICS = {
    "stats": {"total_users": 142500, "total_artists": 840, "storage_used": 42.8},
    "flagged": [
        {"id": 1042, "title": "Unreleased Leak Track", "artist": "Unknown Artist", "reason": "Copyright Claim"},
        {"id": 1099, "title": "Loud Static Noise Loop", "artist": "GlitchBot", "reason": "Audio Corruption File"}
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login-submit', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    selected_role = request.form.get('user_role')
    
    if not username or not password:
        return redirect('/')

    if selected_role == 'admin':
        return redirect('/admin')
        
    elif selected_role == 'artist':
        artist_slug = username.lower().replace(" ", "-")
        return redirect(f'/artist/{artist_slug}')
        
    elif selected_role == 'listener':
        return redirect(f'/dashboard/{username.lower()}')
        
    return redirect('/')
    
@app.route('/dashboard/<username>')
def user_dashboard(username):
    user_key = username.lower()
    if user_key in USER_PROFILES:
        return render_template('user_dashboard.html', profile=USER_PROFILES[user_key])
    return "<h1>User Workspace Profile Not Found</h1>", 404

@app.route('/artist/<artist_name>')
def artist_portal(artist_name):
    artist_key = artist_name.lower()
    catalog = ARTIST_CATALOGS.get(artist_key, [])
    return render_template('artist_portal.html', artist_name=artist_name.title(), catalog=catalog)

@app.route('/artist/<artist_name>/upload', methods=['POST'])
def artist_upload(artist_name):
    artist_key = artist_name.lower()
    
    title = request.form.get('track_title')
    genre = request.form.get('track_genre')
    
    if title and genre:
        new_track = {"title": title, "genre": genre, "streams": "0"}
        
        if artist_key not in ARTIST_CATALOGS:
            ARTIST_CATALOGS[artist_key] = []
        
        ARTIST_CATALOGS[artist_key].append(new_track)
        
    return redirect(f'/artist/{artist_key}')

@app.route('/admin')
def admin_panel():
    return render_template(
        'admin_panel.html', 
        metrics=ADMIN_METRICS["stats"], 
        flagged_items=ADMIN_METRICS["flagged"]
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)