from flask import Flask, session
from werkzeug.security import generate_password_hash
import os

from application.models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
app.secret_key = "top secretkey"
db.init_app(app)

with app.app_context():
    import application.controllers
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
            print("🚀 Success: Database unified and admin seeded cleanly!")

if __name__ == '__main__':
    init_database()
    app.run(host='127.0.0.1', port=5000, debug=True)