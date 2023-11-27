from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, widgets
from wtforms_sqlalchemy.orm import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskApp.models import Headmen, Subjects, Students

class RegistrationForm(FlaskForm):
    username = StringField('Имя', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, username):
        user = Headmen.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя уже занято. Выберите другое!')

class LoginForm(FlaskForm):
    username = StringField('Имя', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class SubjectForm(FlaskForm):
    string = StringField('Название предмета', 
                            validators=[DataRequired(), Length(min=2)])
    subject = StringField('Сокращение', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def validate_string(self, string):
        str = Subjects.query.filter_by(string=string.data).first()
        if str:
            raise ValidationError('Такой предмет уже есть!')
        
    def validate_subject(self, subject):
        sub = Subjects.query.filter_by(subject=subject.data).first()
        if sub:
            raise ValidationError('Такое сокращение уже используется!')
        
class StudentForm(FlaskForm):
    student = StringField('Имя', 
                            validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Сохранить')

    def validate_student(self, student):
        stud = Students.query.filter_by(username=student.data).first()
        if stud:
            raise ValidationError('Такой студент уже есть!')

# class ChooseSubjectsForm(FlaskForm):
#     with app.app_context():
#         subjects = Subjects.query.all()
#     finish = ["", "", "", ""]
#     for i in range(0, len(subjects)):
#         finish[i] = f'{subjects[i].string}'
#     submit = SubmitField('Сохранить')



class ExampleForm(FlaskForm):
    # temp = Subjects.query.all()
    # for i in temp:
    #     i = i.string
    subjects = QuerySelectMultipleField(
        'Subjects',
        query_factory= lambda: Subjects.query.all(),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    submit = SubmitField('Подтвердить')

    #lambda: Subjects.query.all()