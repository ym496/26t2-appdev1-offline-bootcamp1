from flask import Flask,request,render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
db = SQLAlchemy(app)

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
    
# @app.route('/dashboard/<username>')
# def user_dashboard(username):
#     user_key = username.lower()
#     if user_key in USER_PROFILES:
#         return render_template('user_dashboard.html', profile=USER_PROFILES[user_key])
#     return "<h1>User Workspace Profile Not Found</h1>", 404

# @app.route('/artist/<artist_name>')
# def artist_portal(artist_name):
#     artist_key = artist_name.lower()
#     catalog = ARTIST_CATALOGS.get(artist_key, [])
#     return render_template('artist_portal.html', artist_name=artist_name.title(), catalog=catalog)

# @app.route('/artist/<artist_name>/upload', methods=['POST'])
# def artist_upload(artist_name):
#     artist_key = artist_name.lower()
    
#     title = request.form.get('track_title')
#     genre = request.form.get('track_genre')
    
#     if title and genre:
#         new_track = {"title": title, "genre": genre, "streams": "0"}
        
#         if artist_key not in ARTIST_CATALOGS:
#             ARTIST_CATALOGS[artist_key] = []
        
#         ARTIST_CATALOGS[artist_key].append(new_track)
        
#     return redirect(f'/artist/{artist_key}')

# @app.route('/admin')
# def admin_panel():
#     return render_template(
#         'admin_panel.html', 
#         metrics=ADMIN_METRICS["stats"], 
#         flagged_items=ADMIN_METRICS["flagged"]
#     )

# @app.route('/songs')
# def songs():
#     return render_template('songs.html', songs=SONGS)

# @app.route('/songs/<int:song_id>')
# def song_details(song_id):
#     song = SONGS[song_id]
#     if song:
#         return render_template('song_info.html', song=song)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    role = db.Column(db.String(12), nullable=False)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=True)
    lyrics = db.Column(db.Text, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)