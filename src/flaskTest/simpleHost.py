from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/admin')
def hello_admin():
    return 'Hello admin'

@app.route('/guest/<name>')
def hello_guest(name):
    return 'Hello %s as a guest' %name

@app.route('/success/<name>')
def hello_world(name):
    if str(name).lower() == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', name=name))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('hello_world', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('hello_world', name=user))

if __name__ == '__main__':
   app.run(host= "0.0.0.0", debug=True, threaded=True)