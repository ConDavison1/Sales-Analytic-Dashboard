from werkzeug.security import generate_password_hash
from models import db, User
from app import app

with app.app_context():
    users = User.query.all()

    for user in users:
        hashed_password = generate_password_hash(user.password)
        user.password = hashed_password
        db.session.commit()

    print("All passwords have been hashed and updated.")

    #DONT RUN THIS FILE AGAIN AFTER RUNNING IT ONCE
