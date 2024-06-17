from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegistrationForm

"""
Создать форму для регистрации пользователей на сайте. 
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
"""

app = Flask(__name__)

app.config['SECRET_KEY'] = '32b2c9982dab56275242e90ba6b200a7fa8e7a3dca17dc77e394985f17df1bba'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def main():
    return 'Добро пожаловать!'

@app.route('/reg/', methods=['GET','POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate:
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        return f'Залогинился {last_name}'
    return render_template('reg.html')


if __name__ =='__main__':
    app.run(debug=True)