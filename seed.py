from app import app, db, User, Song, Playlist, PlaylistTrack

def seed_database():
    print("⏳ Opening database session workspace...")
    
    with app.app_context():
        
        print("🧹 Dropping old tables and rebuilding clean schemas...")
        db.drop_all()
        db.create_all()
        
        print("🌱 Injecting core user accounts...")
        admin = User(username="admin", password="adminpass", role="admin")
        artist = User(username="mujic guy", password="artistpass", role="artist")
        listener = User(username="ym496", password="userpass", role="listener")
        
        db.session.add_all([admin, artist, listener])
        db.session.commit() 
        
        print("🎵 Injecting artist catalog songs with detailed family-friendly lyrics...")
        song1 = Song(
            title="Counting Stars", 
            genre="Pop Rock", 
            lyrics=(
                "[Chorus]\n"
                "Lately, I've been, I've been losing sleep\n"
                "Dreaming about the things that we could be\n"
                "But baby, I've been, I've been praying hard\n"
                "Said, no more counting dollars\n"
                "We'll be, we'll be counting stars\n"
                "Yeah, we'll be counting stars\n\n"
                "[Verse 1]\n"
                "I see this life, like a swinging vine\n"
                "Swing my heart across the line\n"
                "And in my face is flashing signs\n"
                "Seek it out and ye shall find\n"
                "Old, but I'm not that old\n"
                "Young, but I'm not that bold\n"
                "And I don't think the world is sold\n"
                "I'm just doing what we're told\n\n"
                "[Pre-Chorus]\n"
                "I, I, I, I feel something right\n"
                "And doing the wrong thing\n"
                "I, I, I, I feel something right\n"
                "And doing the wrong thing\n"
                "I couldn't lie, couldn't lie, couldn't lie\n"
                "Everything that kills me makes me feel alive\n\n"
                "[Chorus]\n"
                "Lately, I've been, I've been losing sleep\n"
                "Dreaming about the things that we could be\n"
                "But baby, I've been, I've been praying hard\n"
                "Said, no more counting dollars\n"
                "We'll be, we'll be counting stars\n"
                "Lately, I've been, I've been losing sleep\n"
                "Dreaming about the things that we could be\n"
                "But baby, I've been, I've been praying hard\n"
                "Said, no more counting dollars\n"
                "We'll be, we'll be counting stars"
            ), 
            artist_id=artist.id
        )
        
        song2 = Song(
            title="Viva La Vida", 
            genre="Alternative Rock", 
            lyrics=(
                "[Verse 1]\n"
                "I used to rule the world\n"
                "Seas would rise when I gave the word\n"
                "Now in the morning, I sleep alone\n"
                "Sweep the streets I used to own\n\n"
                "[Verse 2]\n"
                "I used to roll the dice\n"
                "Feel the fear in my enemy's eyes\n"
                "Listen as the crowd would sing\n"
                "\"Now the old king is dead, long live the king\"\n\n"
                "[Verse 3]\n"
                "One minute, I held the key\n"
                "Next the walls were closed on me\n"
                "And I discovered that my castles stand\n"
                "Upon pillars of salt and pillars of sand\n\n"
                "[Chorus]\n"
                "I hear Jerusalem bells a-ringing\n"
                "Roman Cavalry choirs are singing\n"
                "Be my mirror, my sword and shield\n"
                "My missionaries in a foreign field\n"
                "For some reason I can't explain\n"
                "Once you'd gone, there was never, never an honest word\n"
                "And that was when I ruled the world"
            ), 
            artist_id=artist.id
        )
        
        db.session.add_all([song1, song2])
        db.session.commit()
        
        print("📝 Creating custom listener playlist structures...")
        user_playlist = Playlist(name="Late Night Vibes", user_id=listener.id)
        db.session.add(user_playlist)
        db.session.commit()
        
        print("🔀 Mapping songs into playlists...")
        mapping = PlaylistTrack(playlist_id=user_playlist.id, song_id=song1.id)
        db.session.add(mapping)
        db.session.commit()
        
        print("🌟 Success: Database seeding pipeline run completed perfectly!")

if __name__ == "__main__":
    seed_database()