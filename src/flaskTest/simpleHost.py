from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/admin')
def hello_admin():
    return 'Hello admin'

@app.route('/guest/<name>')
def hello_guest(name):
    return 'Hello %s as a guest' %name

@app.route('/user/<name>')
def hello_world(name):
    if str(name).lower() == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', name=name))
    return 'Hello World %s' %str(name)

@app.route('/user/<name>')



if __name__ == '__main__':
   app.run(host= "0.0.0.0", debug=True, threaded=True)