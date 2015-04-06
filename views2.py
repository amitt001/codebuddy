from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, redirect, url_for, session
from flask.ext.socketio import SocketIO, emit
import random
import string
import mongosave


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'xxxxxx'
socketio = SocketIO(app)
thread = None
masterdict = {}
codepadlst = [None] * 2   # for maintaining the rooms in codepad
count = 0
uniqid = 'random'


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        if request.form.get('login', None) == 'Sign Up/Login':

            user_email = request.form.get('email', None)
            user_pass = request.form.get('password', None)

            if len(user_email) > 5 and len(user_pass) > 5:
                dbclass = mongosave.mongosave()
                session_id = dbclass.userlogin(user_email, user_pass)
                if (session_id == -1):
                    return 'ERROR: RELOAD'
                if (session_id == -2):
                    return 'User already exists and wrong password for this email'
                session['id'] = session_id
                return redirect(url_for('index'))
            else:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('useremail', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route('/publicpad/<padid>') #unique url
def publicpad(padid):
    session_id = session.get('id', 0)
    if not session_id:
        return redirect(url_for('login'))
    dbclass = mongosave.mongosave()
    valid_check = dbclass.login_check(session_id)
    if valid_check == -1:
        return "Please login again"
    else:
        return render_template('newpad.html', sessionid=session_id)


@app.route('/docpad/<padid>')
def textpad(padid):
    return render_template('docpad.html')


@app.route('/pastepad/<padid>', methods=['GET','POST'])
def pastepad(padid):
    global uniqid 
    uniqid = padid
    checkpad = mongosave.mongosave()
    pasteres =  checkpad.check(padid)#x random data
    if pasteres:
        return render_template("pasteresult.html", result=pasteres)
    else:
        return render_template('pastepad.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form.get('public', None) == 'New Public Codepad':
            codepadurl = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(9))
            return redirect(url_for('publicpad', padid=codepadurl))

        if request.form.get('docpad', None) == 'New Document Pad':
            docpadurl = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(8))
            return redirect(url_for('textpad', padid=docpadurl))

        if request.form.get('paste', None) == 'Paste Pad':
            uniquelink = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(10))
            return redirect(url_for('pastepad', padid=uniquelink))
            
    return render_template("index.html", title="CodeBuddy")


@socketio.on('connect', namespace='/test')
def local_client_connect():
    pass

@socketio.on('dbpaste', namespace='/test')
def test_message(message):
    saveobj = mongosave.mongosave()
    saveobj.save(uniqid, message['data'])
    emit('my response', {'data': message['data']})

@socketio.on('removeid', namespace='/test')
def remove_id(message):
    print 'I am disconnecting\n'
    if message['id'] in codepadlst:
        codepadlst[codepadlst.index(message['id'])] = None

    print codepadlst

@socketio.on('sync', namespace='/test') #code sync
def sync(message):
    #doing all the checks for only two connection allowable
    #########This is not executed for 3rd pad. look into it#########
    data = masterdict.get(message['id'])
    session_id = session['id']
    if not data:
        masterdict[message['id']] = []
        masterdict[message['id']].append(session_id)
        emit('sync response', {'data': message['data'], 'id': session_id, 'url': message['id']}, broadcast=True)
    else:
        if len(data) < 2 and session_id not in data:
            masterdict[message['id']].append(session_id)
            emit('sync response', {'data': message['data'], 'id': session_id, 'url': message['id']}, broadcast=True)            
            print 'MasterDict right now ', masterdict
        if session_id in data:
            emit('sync response', {'data': message['data'], 'id': session_id, 'url': message['id']}, broadcast=True)
        elif len(data)>=2 and session_id not in data:
            emit('error response', {'error': 'CodePad already in use. Ask creater to allow you. Thank you.', 'block': 'yes'})

def fool():
    if codepadlst[0] == None and message['id'] not in codepadlst:
        codepadlst[0] = message['id']
    elif codepadlst[1] == None and message['id'] not in codepadlst:
        codepadlst[1] = message['id']
    elif message['id'] in codepadlst:
        pass
    else:
        emit('error response', {'error': 'CodePad already in use. Ask creater to allow you. Thank you.'})
        return
    emit('sync response', {'data': message['data'], 'id': message['id']}, broadcast=True)


@socketio.on('pingback', namespace='/test') #chek connection
def ping(message):
    print codepadlst
    if message['id'] in codepadlst:
        return
    else:
        try:
            del(codepadlst[codepadlst.index(message['id'])])
        except:
            print('ERROR')


@socketio.on('connect', namespace='/test')
def test_connect():
    pass


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
