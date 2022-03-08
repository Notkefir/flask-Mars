from flask import Flask, url_for, render_template, make_response, request, jsonify
from werkzeug.utils import redirect

from data.news import News
from data.jobs import Jobs
from data.users import User
from data import db_session

from werkzeug.exceptions import abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import LoginForm, RegisterForm
from forms.jobsadd import JobsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            surname=form.surname.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.team_leader_id = form.team_leader_id.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/promotion')
def promotion():
    return '''Человечество вырастает из детства.<br>
Человечеству мала одна планета.<br>
Мы сделаем обитаемыми безжизненные пока планеты.<br>
И начнем с Марса!<br>
Присоединяйся!'''


@app.route('/image_mars')
def image():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}" 
                    alt="здесь должна была быть картинка, но не нашлась">
                    Вот она красная планета!
                  </body>
                </html>"""


def users_add():
    user1 = User()
    user1.surname = "Scott"
    user1.name = "Ridley"
    user1.age = 21
    user1.position = "captain"
    user1.speciality = "research engineer"
    user1.address = "module_1"
    user1.email = "scott_chief@mars.org"

    user2 = User()
    user2.surname = "Scoty"
    user2.name = "Red"
    user2.age = 13
    user2.position = "helper"
    user2.speciality = "doctor"
    user2.address = "module_1"
    user2.email = "scoty_doc@mars.org"

    user3 = User()
    user3.surname = "Bredly"
    user3.name = "Crug"
    user3.age = 25
    user3.position = "matros"
    user3.speciality = "research doctor"
    user3.address = "module_2"
    user3.email = "bredly_dadly@mars.org"

    user4 = User()
    user4.surname = "Jony"
    user4.name = "Cromwell"
    user4.age = 32
    user4.position = "matros"
    user4.speciality = "engineer"
    user4.address = "module_3"
    user4.email = "jony_syyns@mars.org"

    db_sess = db_session.create_session()
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.add(user4)
    db_sess.commit()


def jobs_add():
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader_id = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()


def news_add():
    db_sess = db_session.create_session()
    news = News(title="Первая новость", content="Привет блог!",
                user_id=1, is_private=False)

    user = db_sess.query(User).filter(User.email == "email@email.ru").first()
    news2 = News(title="Вторая новость", content="Уже вторая запись!",
                 user=user, is_private=False)
    news3 = News(title="Первая новость", content="Привет блог!",
                 user_id=1, is_private=False)

    db_sess.add(news2)
    db_sess.add(news3)
    db_sess.commit()


def user_get():
    db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id == 1).first()
    for user in db_sess.query(User).all():
        print(user)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # users_add()
    # news_add()
    # user_get()
    # jobs_add()
    app.run(port=8080, host='127.0.0.1')
