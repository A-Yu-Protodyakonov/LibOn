from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename
from User import User
from Administrator import Administrator
from Book import Book
import sqlite3
import os
from _datetime import date,datetime, timedelta

app = Flask(__name__)

app.config.update(DATABASE=os.path.join(os.path.dirname(__file__), 'PT.db'), DEBUG=True, SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')

current_user, user_type, b = None, None, None


@app.route('/')
@app.route('/main_page')
def main_page():
    session.clear()
    session['page'] = "Главная страница"
    global current_user, b
    if current_user is None:
        b = False
    else:
        b = True
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    check = cursor.execute("""select RUBRIC_NAME from RUBRIC;""").fetchall()
    #check1 = cursor.execute("""select RUBRIC_NAME from RUBRIC where RUBRIC_ID%2 == 0;""").fetchall()
    return render_template('main.html', b=b, type=user_type, rubric=check)


@app.route('/log_in')
def log_in():
    global current_user
    current_user = None
    return render_template('auth.html', err='')


@app.route('/registration')
def registration():
    return render_template('registration.html', err="")


@app.route('/Registration', methods=['GET', 'POST'])
def Registration():
    if request.method == 'POST':
        connect = sqlite3.connect(app.config['DATABASE'])
        cursor = connect.cursor()
        check = cursor.execute("SELECT * from USER where E_MAIL = \"{}\" and PASSWORD = \"{}\"".format(
            request.form['email'], request.form['password'])).fetchone()
        if check is None:
            id_ = cursor.execute("SELECT MAX(USER_ID) FROM USER;").fetchone()
            if id_[0] is None:
                id_ = (0,)
            global current_user, user_type
            current_user = User(id_[0]+1, request.form['first_name'], request.form['second_name'],
                                request.form['email'], request.form['password'])
            user_type = 'User'
            cursor.execute("INSERT INTO USER (USER_NAME, USER_LAST_NAME, E_MAIL, PASSWORD) VALUES (\"{}\", \"{}\","
                           "\"{}\",\"{}\")".format(current_user.memberName, current_user.memberLastname,
                                                   current_user.email, current_user.password))
            connect.commit()
            return render_template('success.html')
        else:
            return render_template('registration.html', err="Такой пользователь уже существует.")
    else:
        return redirect(url_for('main_page'))


@app.route('/Log_in', methods=['GET', 'POST'])
def Log_in():
    if request.method == 'POST':
        connect = sqlite3.connect(app.config['DATABASE'])
        cursor = connect.cursor()
        global current_user, user_type
        if current_user is not None:
            return redirect(url_for('user_profile'))
        else:
            check = cursor.execute("select * from USER where E_MAIL = \"{}\" and PASSWORD = \"{}\"".format(
                request.form['email'], request.form['password'])).fetchone()
            if check is None:
                check = cursor.execute("select * from ADMINISTRATOR where E_MAIL = \"{}\" and PASSWORD = \"{}\"".format(
                    request.form['email'], request.form['password'])).fetchone()
                if check is None:
                    return render_template('auth.html', err='Неправильный логин или пароль')
                else:
                    current_user = Administrator(check[0], check[1], check[2], check[3], check[4])
                    user_type = 'Admin'
                    return redirect(url_for('admin_profile'))
            else:
                current_user = User(check[0], check[1], check[2], check[3], check[4])
                user_type = 'User'
                return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.jinja_env.filters['zip'] = zip
    app.run(debug=True)
    session.clear()
