from flask import Flask, render_template, request, redirect, url_for, flash  # add flask modules
from flask_sqlalchemy import SQLAlchemy  # add flask_sqlalchemy module for database
from datetime import datetime
import urllib.request as req
import os
import random

app = Flask(__name__)

location = os.path.abspath(os.getcwd()) + "/todo.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{location}' # add absolute path to db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # load modification in db
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)  # start sqlalchemy

class Task(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(80), nullable=False)
   created_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.now)

   def __repr__(self):
       return f'Todo : {self.name}'


def shorturl(url):
  try:
    # set the api of a url shortner to a var
    apiurl = "http://tinyurl.com/api-create.php?url="
    # append parameter to the api
    web = apiurl + url
    # with urllib.request.urlopen(web) as response:
    response = req.urlopen(web).read()
    return response.decode("utf-8")
  except Exception as e:
    return "error"

# create endpoints
@app.route("/", methods=['POST', 'GET'])
# @flask_optimize.optimize()
def home():
  if request.method == "POST": # run this when request is post
    name = request.form['name']
    name = shorturl(name)
    if name == "error":
      flash("Enter valid URL!!")
    else:
      new_task = Task(name=name)
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
  else:
     tasks = Task.query.order_by(Task.created_at).all()  # order task by duration
  return render_template("home.html", tasks=tasks)  # render home.html 

@app.route('/delete/<int:iden>')
# @flask_optimize.optimize()
def delete(iden):
   task = Task.query.get_or_404(iden)

   try:
       db.session.delete(task)
       db.session.commit()
       return redirect('/')
   except Exception as e:
       return "There was a problem deleting data."

@app.errorhandler(404)
# @flask_optimize.optimize()
def errror_404_page(error):
  return render_template("error.html")


if __name__ == "__main__":
  app.run()