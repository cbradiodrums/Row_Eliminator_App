from flask_sqlalchemy import SQLAlchemy


# Create a DB object from SQLAlchemy
DB = SQLAlchemy()


# Make a User table using SQLAlchemy
class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'

# Make a Tweet table using SQLAlchemy
class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(
        DB.BigInteger, 
        DB.ForeignKey('user.id'),
        nullable=False
    )
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet: {self.text}>'