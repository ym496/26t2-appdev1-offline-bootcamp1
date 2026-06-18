from flask import Flask,request,render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
db = SQLAlchemy(app)
    
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

def init_database():
    os.makedirs(app.instance_path, exist_ok=True)
    
    with app.app_context():
        db.create_all()        
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            hashed_password = generate_password_hash("admin")
            seeded_admin = User(username='admin', password=hashed_password, role='admin')
            db.session.add(seeded_admin)
            db.session.commit()


# Routes 

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

    user = User.query.filter_by(username=username, role=selected_role).first()
    
    if user:
        
        if selected_role == 'admin':
            return redirect('/admin')
        elif selected_role == 'artist':
            return redirect(f'/artist/{user.username}')
        elif selected_role == 'listener':
            return redirect(f'/dashboard/{user.username}')
            
    return redirect('/')

@app.route('/admin')
def admin_panel():
    metrics_context = {
        'total_users': User.query.filter_by(role='listener').count(),
        'total_artists': User.query.filter_by(role='artist').count()
    }
    return render_template('admin_panel.html', metrics=metrics_context)

@app.route('/dashboard/<username>')
def user_dashboard(username):
    user_record = User.query.filter_by(username=username, role='listener').first_or_404()
    
    profile_context = {
        'name': user_record.username,
        'tier': 'Premium Member',
        'favorites': Song.query.all()
    }
    return render_template('user_dashboard.html', profile=profile_context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        if user_role == 'admin':
            return redirect('/register')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect('/register')

        new_user = User(username=username, password=password, role=user_role)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template('register.html')

if __name__ == '__main__':
    init_database()
    app.run(host='127.0.0.1', port=5000, debug=True)