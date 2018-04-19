from flask import Flask, request, render_template, url_for, session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, Email

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oluwasogo:ogundowole@localhost/hub2four7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_random_key'


class sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


db.create_all()


class LoginForm(Form):
    email = TextField('email', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired()])


@app.route('/')
def index():
    return render_template('index.html', urls=url_dict)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('email'):
        logged_in = "You are already logged in"
        return render_template("login.html", logged_in=logged_in, urls=url_dict)
    form = LoginForm(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = sign.query.filter_by(email=email, password=password).first()
        if not existing_user:
            not_exist = "Incorrect username or password"
            return render_template('login.html', not_exist=not_exist, urls=url_dict)
        session['email'] = email
        login = "You are now logged in."
        return render_template("profile.html", login=login, urls=url_dict)
    if form.errors:
        not_login = "Something isn't right, please reload page and try again"
        return render_template("login.html", not_login=not_login, urls=url_dict)
    return render_template("login.html", urls=url_dict)


@app.route('/signup', methods=["POST"])
def signup():
    try:
        full_name = request.form['full_name']
        password = request.form['password']
        email = request.form['email']
        confirm = request.form['confirm']
        if confirm != password:
            not_match = "Passwords doesn't match"
            return render_template("login.html", not_match=not_match, urls=url_dict)
        existing_user = sign.query.filter_by(email=email)
        if not existing_user:
            existing_user = "Sorry, this email has been registered"
            return render_template("login.html", existing_user=existing_user, urls=url_dict)
        user = sign(full_name=full_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        msg = "You have succesfully signed up. Proceed to login"
        return render_template("login.html", msg=msg, urls=url_dict)
    except Exception as e:
        return (str(e))


@app.route('/me')
def user_dashboard():
    if "email" not in session:
        login_first = "please login first"
        return render_template("login.html", login_first=login_first, urls=url_dict)
    email = session.get("email")
    return render_template('profile.html', urls=url_dict, email=email)


@app.route('/requests')
def user_requests():
    email = session.get("email")
    return render_template('request.html', urls=url_dict, email=email)


@app.route('/profile')
def view_profile():
    email = session.get("email")
    return render_template('viewprofile.html', urls=url_dict,email=email)


@app.route('/subscribe')
def subscribe():
    email = session.get("email")
    return render_template('settings.html', urls=url_dict,email=email)


@app.route('/demoOnly')
def demo():
    email = session.get("email")
    return render_template('demos.html', urls=url_dict, email=email)


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        log_out = 'You have successfully logged out.'
        return redirect(url_for('index', logout=log_out))
    return redirect(url_for('index'))


with app.test_request_context() as f:
    url_index = url_for('index')
    url_login = url_for('login')
    url_sign = url_for("signup")
    url_me = url_for('user_dashboard')
    url_request = url_for('user_requests')
    url_subscribe = url_for('subscribe')
    url_profile = url_for('view_profile')
    url_demo = url_for('demo')
    url_dict = {
        'url_index': url_index,
        'url_login': url_login,
        'url_signup': url_sign,
        'url_me': url_me,
        'url_request': url_request,
        'url_subscribe': url_subscribe,
        'url_profile': url_profile,
        'demo': url_demo,
    }

if __name__ == '__main__':
    app.run(debug=True)
