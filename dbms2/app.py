from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
 
app = Flask(__name__, instance_relative_config=True)
app.debug = True

 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
 
# Settings for migrations
migrate = Migrate(app, db)
 
# Models
class Library(db.Model):
    # Id : Field which stores unique id for every row in
    # database table.
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(20), unique=False, nullable=False)
    author_name = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(15), nullable=True)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Book_name : {self.book_name}, status: {self.status}"

# function to render index page
@app.route('/')
def index():
    libraries = Library.query.all()
    return render_template('index.html', libraries=libraries)
 
@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    libraries = Library.query.filter(Library.book_name.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', libraries=libraries, query=search_query)
 
# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    # In this function we will input data from the
    # form page and store it in our database. Remember
    # that inside the get the name should exactly be the same
    # as that in the html input fields
    book_name = request.form.get("book_name")
    author_name = request.form.get("author_name")
    status = request.form.get("status")
 
    # create an object of the Profile class of models and
    # store data as a row in our datatable
    if book_name != '' and author_name != '' :
        p = Library(book_name=book_name, author_name=author_name, status=status)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
 
@app.route('/delete/<int:id>')
def erase(id):
     
    # deletes the data on the basis of unique id and
    # directs to home page
    data = Library.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    library = Library.query.get(id)
    if library:
        if request.method == 'POST':
            # Update book_name, author_name, and status if form is submitted
            new_book_name = request.form.get('book_name')
            new_author_name = request.form.get('author_name')
            new_status = request.form.get('status')

            if new_book_name:
                library.book_name = new_book_name
            if new_author_name:
                library.author_name = new_author_name
            if new_status:
                library.status = new_status

            db.session.commit()
            return redirect('/')

        # Render the update_profile.html page
        return render_template('update_profile.html', data=library)

    return redirect('/')

 
if __name__ == '__main__':
    app.run()