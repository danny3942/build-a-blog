from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:SecureServer@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self, name , body):
        self.title = name
        self.body = body
    
    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        body = str(request.form['poop'])
        new_blog = Blog(title , body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by().all()
    return render_template('base.html' , blogs=blogs)


@app.route('/blog' , methods=['POST' , 'GET'])
def blog():

    blogs = Blog.query.all()
    return render_template('blog.html' , blogs=blogs)

@app.route('/blogpage' , methods=['POST' , 'GET'])
def blogpage():

    if request.method == 'POST':
        title = request.form['title']
        body = str(request.form['poop'])
        new_blog = Blog(title , body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('blog.html' , blogs=blogs)


@app.route('/blogpost' , methods=['POST' , 'GET'])
def blogpost():

    post = Blog.query.filter_by(id=request.args.get('id')).first()
    return render_template('blogpage.html', blog=post)


@app.route('/newpost' , methods=['POST' , 'GET'])
def newpost():
    if request.method=='POST':    
        name = request.form['title']
        body = str(request.form['poop'])
        if name != "" and body != "" and not(name is None or body is None):
            entry = Blog(name , body)
            db.session.add(entry)
            db.session.commit()
            blog = Blog.query.filter_by(id=entry.id).first()
            return render_template('blogpage.html' , blog=blog)
        else:
            return render_template('blog.html' , err=True, mssg="Title and Content cannot be empty!!!")
    else:
        return render_template('blog.html')


if __name__ == '__main__':
    app.run()