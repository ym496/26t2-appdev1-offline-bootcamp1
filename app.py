from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/<username>/about",methods=["GET","POST"])
def about(username):
    if request.method == "POST":
        print("Received a POST request to the /about route.")
    return f"<h1>About Page</h1><p>This is the about page of the Flask application.</p>"

@app.route("/user/<username>")
def user_profile(username):
    return f"<h1>{username.title()}</h1><p>This is the profile page for {username}.</p>"

# fetched from db and stored
USER_PLAYLISTS = {
    "alex": {
        "workout": ["Eye of the Tiger", "Till I Collapse", "Harder, Better, Faster, Stronger"],
        "chill": ["Weightless", "Sunset Lover", "Melancholy Hill"]
    },
    "sam": {
        "coding": ["Resonance", "90s Flanger", "Hackers Theme"],
        "roadtrip": ["Hotel California", "Go Your Own Way", "Fast Car"]
    }
}

@app.route('/user/<username>/playlist/<playlist_name>')
def show_user_playlist(username, playlist_name):
    # Normalize inputs to lowercase to prevent casing mismatches (e.g., "Alex" vs "alex")
    user_key = username.lower()
    playlist_key = playlist_name.lower()

    # 1. Check if the user exists in our data
    if user_key not in USER_PLAYLISTS:
        return f"<h2>User '{username}' not found.</h2>", 404

    # 2. Check if that specific user has that specific playlist
    user_data = USER_PLAYLISTS[user_key]
    if playlist_key not in user_data:
        return f"<h2>Playlist '{playlist_name}' not found for user {username}.</h2>", 404

    # 3. Extract the list of tracks
    tracks = user_data[playlist_key]
    
    # Format the tracklist into an HTML string
    list_items = "".join([f"<li>{track}</li>" for track in tracks])

    return f"""
    <h1>{username.title()}'s "{playlist_name.title()}" Playlist</h1>
    <ul>
        {list_items}
    </ul>
    <a href="/">Back Home</a>
    """

@app.route("/admin/add",methods=["POST"])
def add_track():
    track_name = request.form.get("track_name")
    username = request.form.get("username")

    return f"<h2>Track added successfully!</h2><p>Track: {track_name}</p><p>User: {username}</p><p>Playlist: {playlist_name}</p>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)