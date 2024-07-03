import flask
from flask import Flask, render_template, request, url_for, redirect, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DSTV'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# LOGIN CONFIG
manager = LoginManager()
manager.init_app(app)


@manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE IN DB with the UserMixin


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", loggedin=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data_user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
        if data_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hash_pass = generate_password_hash(request.form.get("password"),
                                           method='pbkdf2:sha256',
                                           salt_length=8
                                           )
        new_user = User(email=request.form.get('email'),
                        password=hash_pass,
                        name=request.form.get("name"),
                        )
        db.session.add(new_user)
        db.session.commit()
        load_user(new_user)
        return redirect(url_for('secrets'))
    return render_template("register.html",loggedin=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        ima_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not ima_user:
            flash("The email does not exist, please try again")
            return redirect(url_for('login'))
        elif not check_password_hash(ima_user.password, password):
            flash("Incorrect password, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(ima_user)
            logged_in = True
            return redirect(url_for('secrets'))
    return render_template("login.html",loggedin=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, loggedin=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route('/download')
@login_required
def download():
    return send_file('static/files/cheat_sheet.pdf')  # including as_attachment = True, will download the file


if __name__ == "__main__":
    app.run(debug=True)
