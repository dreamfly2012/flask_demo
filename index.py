import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing
import logging


app = Flask(__name__)

app.config.from_pyfile('config.py')





# @app.route("/")
# def index():
#     data = [{"name":"menghuiguli","age":"28"},{"name":"lisi","age":"22"},{"name":"wangwu","age":"40"},{"name":"zhaoliu","age":"18"}]
    
#     return render_template("index.html",data=data)

@app.route('/')
def show_entries():
    #FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    #app.logger.basicConfig(format=FORMAT)
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    
    app.logger.debug(d)
    app.logger.error("some thing happen, %s people", 3)
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.before_request
def process_request():
    # 验证表示，任何地址请求都会先执行before_request，所以登录验证就可以在before_request里做用户认证功能了
    print("其他请求之前就执行了process_request")
    # 4.访问/login的时候还没有登录，就会一直重定向到登录页，所以就要设置个白名单,如果请求地址是/login,就返回None
    if request.path == "/login":
        return None
    # 1.登录验证功能
    user = session.get('user_info')
    # 2.如果登录信息正常，什么都不做，程序继续其他执行
    if user:
        return None
    # 3.如果登录验证不通过，就重定向到登录页面
    return redirect("/login")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
       

if __name__ == "__main__":
    handler = logging.FileHandler('flask.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
   
    app.run() 