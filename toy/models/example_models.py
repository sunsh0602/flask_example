from toy import db


class ExampleUser(db.Model):
    __tablename__ = 'example_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<ExampleUser %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)
