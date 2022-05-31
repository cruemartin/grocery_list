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


@app.route('/', methods=['POST', 'GET'])
def index():
    view_list = []
    list_name = ""
    exists = False
    l = 0

    print(request.args.get('list'))

    if request.args.get('list') is not None:
        l = int(request.args.get('list'))

        view_list = Item.query.filter_by(list_id = l).all()
        
        list_name = List.query.filter_by(id = l).first()
        if list_name is not None:
            list_name = list_name.name   
            exists = True
        
    return render_template("index.html", l=l, view_list = view_list, list_name=list_name, exists = exists )

@app.route('/create', methods = ['POST', 'GET'])
def create():
    

    if request.method == 'POST':
        name = request.form['name']
        db.session.add(List(name=name))
        db.session.commit()

    lists = List.query.all()
    return render_template("create.html", lists = lists)


if __name__ == '__main__':
    app.run(debug=True)
