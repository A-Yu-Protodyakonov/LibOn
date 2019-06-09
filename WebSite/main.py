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


@app.route('/user_profile')
def user_profile():
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    data_= tuple()
    check = cursor.execute("""select BOOK.BOOK_ID, BOOK.BOOK_NAME, BOOK.AUTHOR, BOOK.RENTAL_TIME 
                            from BOOK 
                            where BOOK.BOOK_ID IN ( 
                            select _ORDER.BOOK_ID 
                            from _ORDER 
                            where USER_ID = {})""".format(current_user.id)).fetchall()
    for item in check:
        second_check = cursor.execute("""select START_DATE 
                                        from _ORDER 
                                        where BOOK_ID = {} and USER_ID = {} 
                                        """.format(item[0], current_user.id)).fetchone()
        date_ = datetime.strptime(second_check[0], '%Y-%m-%d').date() + timedelta(days=item[3])
        data_ += ((item[0], item[1], item[2], date_.strftime('%Y-%m-%d')),)
    return render_template('profile_user.html', name=current_user.memberName, surname=current_user.memberLastname,
                            data=data_)


@app.route('/admin_profile')
def admin_profile():
    return render_template('profile_admin.html', name=current_user.memberName, surname=current_user.memberLastname)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    return render_template('add_book.html', err='')


@app.route('/Add_book', methods=['GET', 'POST'])
def Add_book():
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    global current_user
    if request.form['book_type'] == 'on':
        b = 2
    else:
        b = 1
    check = cursor.execute("""select * from BOOK where BOOK_NAME = \"{}\" and Author = \"{}\" and 
                            PUBLISH_YEAR = \"{}\" and BOOK_TYPE = {};""".format(
        request.form['name'], request.form['author'], request.form['publish_year'], b)).fetchone()
    if check is None:
        id_ = cursor.execute("SELECT MAX(BOOK_ID) FROM BOOK;").fetchone()
        if id_[0] is None:
            id_ = (0,)
        book = Book(id_[0]+1, request.form['name'], request.form['rubric_name'], request.form['author'],
                    request.form['publish_year'], request.form['rental_time'], request.form['book_type'])
        current_user.add_book(book)
        return render_template('success_add.html')
    else:
        return render_template('add_book.html', err='Такая книга уже существует')


@app.route('/rubric')
def rubric():
    check = request.args.get('val', '')
    # session['page'] = check
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    id_ = cursor.execute("""select RUBRIC_ID from RUBRIC where RUBRIC_NAME = \"{}\";""".format(check)).fetchone()
    column_ = ('BOOK_NAME', 'AUTHOR', 'PUBLISH_YEAR')
    books = cursor.execute("""select BOOK_ID, BOOK_NAME, AUTHOR, PUBLISH_YEAR from BOOK 
    where RUBRIC_ID = {};""".format(id_[0])).fetchall()
    return render_template('unitpoetry.html', name=check, book=books, column=column_, b=b, type=user_type)


@app.route('/rubric_book')
def rubric_book():
    check = request.args.get('val', '')
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    book = cursor.execute("""select * from BOOK where BOOK_ID = \"{}\";""".format(check)).fetchone()
    book = book[:-1]
    if user_type == 'Admin':
        return render_template('book1_admin.html', book=book)
    else:
        return render_template('book1.html', book=book, b=b)


@app.route('/Add_to_order', methods=['GET', 'POST'])
def Add_to_order():
    check = dict(request.form)
    global current_user
    for x in check.keys():
        if check[x] == 'Заказать':
            ans = int(x)
    current_user.add_to_order(ans)
    return redirect(url_for('user_profile'))


@app.route('/Delete_book', methods=['GET', 'POST'])
def Delete_book():
    check = dict(request.form)
    global current_user
    for x in check.keys():
        if check[x] == 'Удалить':
            ans = int(x)
    current_user.delete_book(ans)
    return redirect(url_for('main_page'))


@app.route('/Delete_from_order', methods=['GET', 'POST'])
def Delete_from_order():
    check = dict(request.form)
    global current_user
    for x in check.keys():
        if check[x] == 'Удалить':
            ans = int(x)
    current_user.delete_from_order(ans)
    return redirect(url_for('user_profile'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    check = request.form['Поиск']
    column_ = ('BOOK_NAME', 'AUTHOR', 'PUBLISH_YEAR')
    connect = sqlite3.connect(app.config['DATABASE'])
    cursor = connect.cursor()
    cursor.execute("""select BOOK_ID, BOOK_NAME, AUTHOR, PUBLISH_YEAR from BOOK where BOOK_NAME 
    like '%{}%' or BOOK_NAME like '%{}%'""".format(
        check.title(), check.lower()))
    data_ = cursor.fetchall()
    return render_template('search.html', book=data_, b=b, type=user_type, column=column_)


if __name__ == '__main__':
    app.jinja_env.filters['zip'] = zip
    app.run(debug=True)
    session.clear()
