import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Environment variables SECRET and MONGO_URI set in Heroku dashboard in production

app.secret_key = os.getenv("SECRET")
app.config["MONGO_URI"] = os.getenv("MONGO_URI") # Creating a link to the MongoDB with Flask application
app.config["MONGO_DBNAME"] = "task_manager"

mongo = PyMongo(app) # To create an instance of PyMongo

@app.route('/') # Route decorator & default test 
@app.route('/get_tasks') # 'get_tasks' becomes the default decorator due to / in place

def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find()) # redirect to existing tasks_html template. Plus, supply a tasks collection returned from making a call to Mongo. find() returns everything.
    
@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
    categories=mongo.db.categories.find()) # Allows task categories in MongoDB to connect with addtask.html file
    
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks # This is the tasks collection 
    tasks.insert_one(request.form.to_dict()) # when submitting info to URI, its submmited in form of a request object
    return redirect(url_for('get_tasks')) # We then grab the request object, show me the form & convert form to dict for Mongo to understand.
    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    # Find a particular task, parameter passed is 'id', looking for a match to 'id' in MongoDB, then wrapped for editing purposes.  
    all_categories = mongo.db.categories.find() # Reuse much of the layout in 'add_task' function, but with pre-populated fields.
    return render_template('edittask.html', task=the_task, categories=all_categories)

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks # Access to the tasks collection in mongo.db
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description':request.form.get('task_description'),
        'due_date':request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)}) # We access the tasks collection & call to remove selected task. 
    return redirect(url_for('get_tasks'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find()) # Aim is to do a find on the categories table in MongoDB & render result in categories.html file.

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))

@app.route('/update_category/<category_id>', methods=['POST']) # ID required to target the correct document in mongo
def update_category(category_id):
    categories = mongo.db.categories
    categories.update({'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)}) # We access the tasks collection & call to remove selected task. 
    return redirect(url_for('get_categories'))

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories # This is the categories collection 
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories')) 

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
    port=int(os.environ.get('PORT', "5000")),
    debug=False) # We access the category in MongoDB, find one that matches and update.
    

