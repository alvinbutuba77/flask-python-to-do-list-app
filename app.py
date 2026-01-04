#Imports
from flask import Flask, render_template
from flask import request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import session

#My app setup
app = Flask(__name__)
Scss(app)

#stage 2, creating db config

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# when deploying,
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



#stage 2, db model

#data class  ~ row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())
    
    #represents how objects of the MyTask will look like
    def __repr__(self):
        return f"Task {self.id}"


# when deploying, place this here
with app.app_context():
    db.create_all()


#creating routes to webpages
#home page

# stage 3, adding functionality, sending data to db
@app.route("/", methods=["POST", "GET"])
def index():

    # if adding a task to db
    if request.method == "POST":
        current_task = request.form['content']# capturing data from form in index.html
        new_task = MyTask(content=current_task)# object of db model
        
        try:
            # creating db session and committing object to db
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")# return to homepage
        
        except Exception as e:# error handling
            print(f"ERROR:{e}")
            return f"ERROR:{e}"

    # see current tasks, query db model
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()#query the model to return all tasks by order
        return render_template('index.html', tasks=tasks)

    



# stage 3, delete and edit routes
# delete a task
@app.route("/delete/<int:id>")
def delete(id:int):# id in MyTask
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"



# edit a task
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):# id in MyTask
    edit_task = MyTask.query.get_or_404(id)
    if request.method == "POST": #if new data is being sent
        edit_task.content = request.form['content']#assigning to content property
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return f"ERROR:{e}"
    else:
       return render_template("edit.html", task = edit_task)




#running and debugging application 
if __name__ == "__main__":

    app.run(debug=True)

# when deploying change to if __name == "__main__"