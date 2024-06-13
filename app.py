from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SIP_DATABASE.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(student_id):
    return StudentData.query.get(int(student_id))


class StudentData(UserMixin, db.Model):
    # __tablename__ = 'student_data'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    other_name = db.Column(db.String(250))
    date_of_birth = db.Column(db.String(250))
    phone = db.Column(db.String(250))
    email = db.Column(db.String(250))
    student_email = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    level = db.Column(db.String(250))
    student_type = db.Column(db.String(250))
    enrollment_date = db.Column(db.String(250))
    graduation_date = db.Column(db.String(250))
    degree_programmes = db.Column(db.String(250))
    undergraduate_programmes = db.Column(db.String(250))
    guardian_name = db.Column(db.String(250))
    guardian_email = db.Column(db.String(250))
    guardian_phone = db.Column(db.String(250))
    guardian_address = db.Column(db.String(250))
    password = db.Column(db.String(250))

    def get_id(self):
        return self.student_id


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        student = StudentData.query.filter_by(student_id=username).first()

        if not student:
            flash('Student ID not found, please try again')
        elif student.password != password:
            flash('Incorrect password, please try again')
        else:
            login_user(student)
            return redirect(url_for('home'))

    return render_template('index.html', logged_in=current_user.is_authenticated)


# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         student = StudentData.query.filter_by(student_id=username).first()
#
#         if not student:
#             flash('Student ID not found, please try again')
#         else:
#             hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
#             if not check_password_hash(student.password, hashed_password):
#                 flash('Incorrect password, please try again')
#             else:
#                 login_user(student)
#                 return redirect(url_for('home'))
#
#     return render_template('index.html', logged_in=current_user.is_authenticated)


@app.route('/home')
@login_required
def home():
    data = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'other_name': current_user.other_name,
        'student_email': current_user.student_email,
        'gender': current_user.gender
    }
    return render_template('home.html', logged_in=current_user.is_authenticated, data=data)


@app.route('/account')
def account():
    data = {
        'student_id': current_user.student_id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'other_name': current_user.other_name,
        'date_of_birth': current_user.date_of_birth,
        'phone': current_user.phone,
        'email': current_user.email,
        'student_email': current_user.student_email,
        'gender': current_user.gender,
        'level': current_user.level,
        'student_type': current_user.student_type,
        'enrollment_date': current_user.enrollment_date,
        'graduation_date': current_user.graduation_date,
        'degree_programmes': current_user.degree_programmes,
        'undergraduate_programmes': current_user.undergraduate_programmes,
        'guardian_name': current_user.guardian_name,
        'guardian_email': current_user.guardian_email,
        'guardian_phone': current_user.guardian_phone,
        'guardian_address': current_user.guardian_address,
        'password': current_user.password
    }
    cohort = int(data['enrollment_date'].split('-')[0]) - 1
    return render_template('account.html', data=data, cohort=cohort, logged_in=current_user.is_authenticated)


@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/evaluation')
def evaluation():
    return render_template('evaluation.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
