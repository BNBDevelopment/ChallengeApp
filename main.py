from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__, template_folder='')


@app.route('/bet',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return "Hello World!"
   else:
      user = request.args.get('name')
      return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)