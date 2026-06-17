from flask import Flask,request,render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html",last_updated="2024-06-15 12:00:00")

@app.route("/<username>/about",methods=["GET","POST"])
def about(username):
    if request.method == "POST":
        print("Received a POST request to the /about route.")
    return f"<h1>About Page</h1><p>This is the about page of the Flask application.</p>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)