import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'codeinstituteflask'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_book')
def get_book():
    return render_template("book.html", 
                           book=mongo.db.book.find())


@app.route('/add_book')
def add_book():
    return render_template('addbook.html',
                           categories=mongo.db.categories.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():
    book =  mongo.db.book
    book.insert_one(request.form.to_dict())
    return redirect(url_for('get_book'))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book =  mongo.db.book.find_one({"book_id": ObjectId(book_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editbook.html', book=the_book,
                           categories=all_categories)


@app.route('/update_book/<book_id>', methods=["POST"])
def update_book(book_id):
    book = mongo.db.book
    book.update( {'_id': ObjectId(book_id)},
    {
        'book_name':request.form.get('book_name'),
        'category_name':request.form.get('category_name'),
        'book_description': request.form.get('book_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_book'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.book.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_book'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)