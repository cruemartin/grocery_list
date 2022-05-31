from ast import Pass
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_list.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', backref=db.backref('item', lazy=True))
    catagory_id = db.Column(db.Integer, db.ForeignKey('catagory.id'), nullable=False)
    catagory = db.relationship('Catagory', backref=db.backref('catagory', lazy=True))

    def __repr__(self):
        return '<Item %r>'%self.name

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<List %r>' % self.name

class Catagory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Catagory %r>' %self.name


@app.route('/')
def index():
    all_lists = List.query.all()
    return render_template('index.html', all_lists = all_lists)


@app.route('/view_list/<int:list_id>', methods=['GET', 'POST'])
def view_list(list_id):
    print("blah blah")
    print(f"list id : {list_id}")
    item_list = Item.query.filter_by(list_id = list_id).all()
    curr_list = List.query.filter_by(id = list_id).first_or_404(description="Error from list")
    cat = Catagory.query.all()
    return render_template('view_list.html', list = curr_list, items = item_list, catagory = cat)

@app.route('/add_item/<int:list_id>', methods=['POST'])
def add_item(list_id):
    if request.method == 'POST':
        db.session.add(Item(name = request.form['name'], price=float(request.form['price']), list_id = list_id, catagory_id = int(request.form['cat'])))
        db.session.commit()
        return redirect(f'/view_list/{list_id}')
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
