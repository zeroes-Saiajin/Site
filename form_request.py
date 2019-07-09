from wtforms import *
from wtforms.validators import *
from model import *

def login_taken(form, field):
    l1 = field.data
    t = User.get(login=l1)
    if t is not None:
        raise ValidationError('Too late')


def mail_taken(form, field):
    ma = field.data
    t = User.get(mail=ma)
    if t is not None:
        raise ValidationError('Too late')

def slug_check(form, field):
    s = field.data
    s = s.strip()
    if len(s) < 2:
        raise ValidationError('Сокращение должно быть не короче двух символов')
    from string import ascii_lowercase
    if s[0] not in ascii_lowercase:
        raise ValidationError('Сокращение должно начинаться с символа английского языка нижней раскладки')

    for x in s:
        if x not in (ascii_lowercase + '_'):
            raise ValidationError('Сокращение должно состоять только из символов английского языка нижнего регистра и символа "_"')

def password_check(form, field):
    pwd2 = field.data
    pwd1 = form.pwd.data
    if pwd1 != pwd2:
        raise ValidationError('Nope')

def title_check(form, field):
    g = field.data
    if TvSeries.get(title=g):
        raise ValidationError('Такой тайтл уже существует')

class RegistrationForm(Form):
    login = StringField('Логин', [InputRequired(message='Укажите логин'), login_taken])
    mail = StringField('Почта', [InputRequired(message='Укажите почту'), mail_taken])
    pwd = PasswordField('Пароль', [InputRequired(message='Введите пароль')])
    pwd2 = PasswordField('Пароль еще раз', [InputRequired(message='Введите пароль'), password_check])


class LoginForm(Form):
    login = StringField('Логин', [InputRequired()])
    pwd = PasswordField('Пароль', [InputRequired()])


class NameForm(Form):
    first_name = StringField('Имя', [InputRequired()])
    last_name = StringField('Вамилия', [InputRequired()])


class TitleForm(Form):
    title = StringField('Название сериала', [InputRequired(), title_check])
    description = StringField('Описание', [InputRequired()])
    image = StringField('Ссылка на картинку', [InputRequired()])
    start = DateField('Выберите дату', format="%Y/%m/%d")


class EpisodeForm(Form):
    name = StringField('Название эпизода', [InputRequired(), title_check])
    episode = StringField('Номер эпизода', [InputRequired()])
    season = StringField('Номер сезона', [InputRequired()])
    prod = SelectField('Продюсер')
    title = SelectField('Сериал')



