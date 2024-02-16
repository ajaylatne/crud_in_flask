from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/b29'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)


    class Employee(db.Model):
        eid = db.Column(db.Integer, primary_key=True)
        ename = db.Column(db.String(30))
        esal = db.Column(db.Float)

        def __str__(self):
            return f'{self.eid}  {self.ename}'


    db.create_all()


@app.route('/insert', methods=['GET', 'POST'])
def insert_view():
    if request.method == 'POST':
        ename = request.form.get('ename')
        esal = request.form.get('esal')
        obj = Employee(ename=ename, esal=esal)
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('show_view'))
    return render_template('insert.html')


@app.route('/show')
def show_view():
    obj = Employee.query.all()
    return render_template('show.html', obj=obj)


@app.route('/update/<int:pk>/', methods=['GET', 'POST'])
def update_view(pk):
    obj = Employee.query.get(pk)
    if request.method == 'POST':
        obj.ename = request.form.get('ename')
        obj.esal = request.form.get('esal')
        db.session.commit()
        return redirect(url_for('show_view'))
    return render_template('update.html', obj=obj)


@app.route('/delete/<int:pk>/', methods=['GET', 'POST'])
def delete_view(pk):
    obj = Employee.query.get(pk)
    if request.method == 'POST':
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for('show_view'))
    return render_template('delete.html', obj=obj)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
