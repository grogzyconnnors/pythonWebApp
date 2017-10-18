import flask
import sqlite3
import datetime
import time
import os


db = sqlite3.connect('imageApp.db')
cur = db.cursor()



app = flask.Flask(__name__)
app.secret_key = '9c84aa92yt923c8rt55hrg5^' # secret key for session

@app.route('/')
def index():
    if 'username' in flask.session:

        image_names = os.listdir('./static')
        cur.execute('''SELECT file_name, username, date, time FROM images''')
        image_list = cur.fetchall()
        length = len(image_list)
        # print(length)
        print(image_names)
        print(image_list)

        return flask.render_template("profile.html", name=flask.session['username'], image_names=image_names,
                                     image_list=image_list, length=length)
    else:
                                                                # Increment variable
        image_names = os.listdir('./static')                                    # create list of image names
        cur.execute('''SELECT file_name, username, date, time FROM images''')   # select image details from table
        image_list = cur.fetchall()                                             # create list from results
        length = len(image_list)
        # print(length)
        # print(image_names)
        # print(image_list)

        return flask.render_template('index.html', image_names=image_names, image_list=image_list,
                                      length = length) # return index and relevant variables


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']

        cur.execute("SELECT username from users where username = (?)", [username])
        userexists = cur.fetchone()
        if userexists:
            cur.execute("SELECT password from users where password = (?)", [password])
            passwordcorrect = cur.fetchone()
            if passwordcorrect:

                flask.session['username'] = username
                return flask.redirect(flask.url_for('index'))
            else:
                error = 'Incorrect Password'

        else:
            error = 'Incorrect Username'


    return flask.render_template('login.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        name = flask.request.form['name']
        surname = flask.request.form['surname']

        cur.execute("SELECT username from users where username = (?)", [username])
        userexists = cur.fetchone()
        if userexists:
            error = 'Username taken'


        else:
            cur.execute("INSERT INTO users( username, password, name, surname) VALUES('%s','%s','%s','%s')" 
            %(username, password, name, surname))
            db.commit()
            return flask.render_template("reg_complete.html")



    return flask.render_template("register.html", error=error)


@app.route("/images", methods=["GET", "POST"])
def upload_image():
    error = None


    if flask.request.method == "GET":
        return flask.render_template("upload-form.html")
    else:
        file = flask.request.files["image"]
        file.save("static/"+file.filename)

        filename = file.filename                                        # stores correctly formatted db values
        user = flask.session['username']
        date_uploaded = datetime.date.today().strftime('%d-%m-%Y')
        time_uploaded = time.strftime("%H:%M")

        cur.execute("INSERT INTO images( file_name, username, date, time) VALUES('%s','%s','%s','%s')"
                    % (filename, user, date_uploaded, time_uploaded))
        db.commit()

        return flask.redirect(flask.url_for('index'))




app.run()