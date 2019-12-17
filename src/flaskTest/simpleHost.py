from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin')
def hello_admin():
    return 'Hello admin'

@app.route('/guest/<name>')
def hello_guest(name):
    return render_template('guest.html', name=name)
    #return 'Hello %s as a guest' %name

@app.route('/success/<name>')
def hello_world(name):
    if str(name).lower() == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', name=name))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # handle the post method.
        user = request.form['nm']
        return redirect(url_for('hello_world', name=user))
    elif request.method == 'GET':
        # handle the get method.
        user = request.args.get('nm')
        return redirect(url_for('hello_world', name=user))

@app.route('/guest', methods = ['POST', 'GET'])
def hello_name():
    """ handle the user input.
    """
    if request.method == 'POST':
        #score = int(request.form['nm'])
        #dict = {'phy':50,'che':60,'maths':70}
        result = request.form
        return render_template('result.html', marks = 12, result = result)

if __name__ == '__main__':
   app.run(host= "0.0.0.0", debug=True, threaded=True)