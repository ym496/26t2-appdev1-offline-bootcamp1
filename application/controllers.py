from flask import request, render_template, redirect
from flask import current_app as app
from application.models import db, User, Song
from werkzeug.security import generate_password_hash

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

@app.route('/artist/<username>', methods=['GET', 'POST'])
def artist_portal(username):
    artist_user = User.query.filter_by(username=username, role='artist').first_or_404()
    
    if request.method == 'POST':
        title = request.form.get('track_title')
        genre = request.form.get('track_genre')
        lyrics = request.form.get('track_lyrics')
        
        new_song = Song(title=title, genre=genre, lyrics=lyrics, artist_id=artist_user.id)
        db.session.add(new_song)
        db.session.commit()
        return redirect(f'/artist/{username}')
        
    catalog_songs = Song.query.filter_by(artist_id=artist_user.id).all()
    return render_template('artist_portal.html', artist_name=artist_user.username, catalog=catalog_songs)

@app.route('/song/<int:song_id>')
def song_detail(song_id):
    song = Song.query.get_or_404(song_id)
    artist_user = User.query.get(song.artist_id)
    return render_template('song_detail.html', song=song, artist_name=artist_user.username)

@app.route('/song/update/<int:song_id>', methods=['POST'])
def update_song(song_id):
    song_to_edit = Song.query.get_or_404(song_id)
    new_title = request.form.get('updated_title')
    new_genre = request.form.get('updated_genre')
    
    if new_title: song_to_edit.title = new_title
    if new_genre: song_to_edit.genre = new_genre
        
    db.session.commit()
    uploader_account = User.query.get(song_to_edit.artist_id)
    return redirect(f'/artist/{uploader_account.username}')

@app.route('/song/delete/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    song_to_destroy = Song.query.get_or_404(song_id)
    uploader_account = User.query.get(song_to_destroy.artist_id)    
    db.session.delete(song_to_destroy)    
    db.session.commit()
    return redirect(f'/artist/{uploader_account.username}')