from flaskApp.admin.forms import RegistrationForm, LoginForm, SubjectForm, StudentForm, ExampleForm
from flaskApp.models import Students, Subjects, Headmen
from flaskApp import db, bcrypt
# from flask import current_app
from flask import render_template, request, flash, url_for, flash, Blueprint, redirect
from flask_login import login_user, current_user, logout_user, login_required
# crud

ad = Blueprint('admin', __name__)

@ad.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = RegistrationForm()
    form = {'register': RegistrationForm(), 'subject': SubjectForm(), 'student': StudentForm(), 'subjects': ExampleForm()}
    if form['register'].validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form['register'].password.data).decode('utf-8')
        user = Headmen(username=form['register'].username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form["register"].username.data} зарегистрирован!', 'success')
    if form['subject'].validate_on_submit():
        sub = Subjects(string=form['subject'].string.data, subject=form['subject'].subject.data, groups="")
        db.session.add(sub)
        db.session.commit()
        flash(f'Добавлен предмет {form["subject"].subject.data}!', 'success')
    if form['student'].validate_on_submit():
        stud = Students(username=form['student'].student.data, works=0, group=current_user.username[-4::], subject="", priority=0)
        db.session.add(stud)
        db.session.commit()
        flash(f'Добавлен студент {form["student"].student.data}!', 'success')
        return redirect(url_for('admin.admin'))

    if form['subjects'].validate_on_submit():
        temp_sub = Students.query.filter(Students.group == current_user.username[-4::], Students.subject != "").first().subject
        stud = Students.query.filter(Students.group == current_user.username[-4::], Students.subject == temp_sub).all()
        delete = Students.query.filter(Students.group == current_user.username[-4::], Students.subject != temp_sub, Students.subject != "").delete()
        for i in  stud:
            i.subject = ""
        stud = Students.query.filter(Students.group == current_user.username[-4::], Students.subject == "").all()
        for i in form['subjects'].subjects.data:
            sub = Subjects.query.filter(Subjects.string == i.string).first()
            for j in stud:
                new = Students(username=j.username, works=0, group=j.group, subject=i.subject, priority=0)
                db.session.add(new)
            # temp_str = sub.groups.split(sep=",")
            if current_user.username[-4::] not in sub.groups:
                sub.groups += current_user.username[-4::]
            db.session.add(sub)
        Students.query.filter(Students.subject == "").delete()
        db.session.commit()
        # a = "{}".format(form['subjects'].subjects.data[0])
        # list = [a, a[0], a[1]]
        # return a


    # students = Students.query.filter(Students.group == current_user.username[-4::]).all() 
    # for i in range(0, len(students)):
    #     students[i] = f"{i+1}) {students[i].username}"



    # head = Headmen.query.all()
    # s = Subjects.query.all()
    return render_template('admin.html', form=form)

@ad.route("/new")
def new():
    remove_students = Students.query.filter(Students.group == current_user.username[-4::]).all() 
    remove_subjects = Subjects.query.all() 
    for i in remove_students:
        i.priority = 0
        i.works = 0
    for i in remove_subjects:
        if current_user.username[-4::] in i.groups:
            i.groups = i.groups.replace(current_user.username[-4::], '')
    db.session.commit()  
    return redirect(url_for('admin.admin'))

@ad.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_info.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Headmen.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:   
            flash('Не удалось войти. Пожалуйста проверьте имя и пароль!')
    return render_template('login.html', form=form)

@ad.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index_info.index'))