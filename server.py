from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
first_time = True


class User(db.Model):
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    clv = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return '<User %s %f>' % (self.username, self.clv)


@app.route('/predictions/<username>')
def get_customer_clv(username):
    user = User.query.filter_by(id=username).first_or_404()
    data = {
        'user_id': user.id,
        'clv': user.clv
    }
    return jsonify(data)
