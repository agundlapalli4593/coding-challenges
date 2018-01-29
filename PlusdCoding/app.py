from flask import *
from flaskext.mysql import MySQL
import os
from apscheduler.schedulers.background import *
import time

# Cron job Function
def jobcron():
    execfile("syndicator.py")

sched = BackgroundScheduler(daemon=True)
sched.add_job(jobcron ,'interval', seconds=40)
sched.start()

mysql = MySQL()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'pulsd_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = _password
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                flash("User Created Succesfully Please login")
                return redirect('/showSignin')
            else:
                flash("User Exsists . Please Log in")
                return redirect('/showSignin')
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # connect to mysql
        con = mysql.connect()
        query = "select * from tbl_user where user_username ='" + _username + "'"
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) > 0:
            if (str(data[0][3]) == _password):
                session['user'] = data[0][0]
                return redirect('/getEvent')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        getEvent()
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/showAddEvents')
def showAddEvents():
    return render_template('addEvents.html')

@app.route('/addEvent', methods=['POST'])
def addEvent():
    try:
        if session.get('user'):
            _eventid = time.strftime("%Y%m%d%H%M")
            _title = request.form['eventTitle']
            _description = request.form['eventDescription']
            _user = session.get('user')
            _date = request.form['eventdate']
            _time = request.form['eventtime']
            _loc = request.form['eventloc']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tbl_event(event_id,event_title,event_description,event_user_id,event_date,event_time,event_location) values (%s,%s,%s,%s,%s,%s,%s)",
                ([_eventid],[_title], [_description], [_user], [_date],[_time],[_loc]))
            cursor.execute(
                "INSERT INTO tbl_events_log(event_id,status) values (%s,false)",([_eventid]))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('/getEvent')
            else:
                return render_template('error.html', error='An error occurred!')
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/getEvent')
def getEvent():
    try:
        if session.get('user'):
            _user = session.get('user')
            con = mysql.connect()
            cursor = con.cursor()
            cursor.execute("select * from tbl_event e,tbl_events_log l  where e.event_id=l.event_id and e.event_user_id = %s", ([_user]))
            data = cursor.fetchall()
            print(data)
            return render_template('userHome.html', data=data)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    app.run(port=5002)


