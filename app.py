from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_list.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)
    
    def __repr__(self):
        return '<Item %r'%self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        name = request.form['name']
        price = float(request.form['price'])

        new_item = Item(name =name, price = price)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error with db commit.'
    else:
        items = Item.query.all()
        return render_template('index.html', items = items)
if __name__ == '__main__':
    app.run(debug=True)
