from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text.db'
db = SQLAlchemy(app)


class Text(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    title = db.Column(db.Text,
                      nullable=False
                      )
    text = db.Column(db.Text,
                     nullable=False)


class User(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    name = db.Column(db.String(10),
                     nullable=False
                     )
    password = db.Column(db.String(20),
                         nullable=False
                         )


class User_Information(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    age = db.Column(db.Integer,
                    nullable=False
                    )
    height = db.Column(db.Integer,
                       nullable=False
                       )
    educational_institution = db.Column(db.String(50),
                                        nullable=False
                                        )
    country = db.Column(db.String(50),
                        nullable=False
                        )


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        post = Text(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create.html')


@app.route('/posts')
def posts():
    posts = Text.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        try:
            s = db.session.query(User).filter(User.name==username).all()
            if password == s[0].password:
                current_user = User.query.filter_by(name=username).first()
                current_user.id = s[0].id
                return redirect('/')
        except Exception as e:
            print(e)
    else:
        return render_template('login.html')


@app.route('/regisrter', methods=['GET', 'POST'])
@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        user = User(name=username,
                    password=password
                    )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'При входе возникла ошибка'
    else:
        return render_template('register.html')


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        age = request.form['age']
        height = request.form['height']
        educational_institution = request.form['educational_institution']
        country = request.form['country']
        user_info = User_Information(age=age,
                                     height=height,
                                     educational_institution=educational_institution,
                                     country=country
                                     )
        try:
            db.session.add(user_info)
            db.session.commit()
            return redirect('/create')
        except Exception:
            return 'При прохождении проверки произошла ошибка'
    else:
        return render_template('check.html')


@app.route('/buy')
def buy():
    return render_template('buy.html')


if __name__ == '__main__':
    app.run(debug=True)