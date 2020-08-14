from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, BooleanField

from search_entrants import collection_and_analysis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it_is_my_very_big-big_secret_my_dear'


class EntrantsForm(FlaskForm):
    list_entrants = TextAreaField('Введите ФИО абитурентов, каждого с новой строки')
    file_entrants = FileField('Загрузите файл с ФИО абитуриентов')
    is_analysis = BooleanField('Добавить аналитику')
    submit = SubmitField('Поиск')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EntrantsForm()
    result = ['Вы пока ничего не искали']
    if form.submit.data:
        if form.list_entrants.data:
            data = form.list_entrants.data.split('\r\n')
            result = collection_and_analysis(data, form.is_analysis.data)
        elif form.file_entrants.data:
            data = request.FILES[form.image.name].readlines()
            result = collection_and_analysis(data, form.is_analysis.data)
        else:
            result = ['Вы ничего не ввели']
    return render_template('index.html', form=form, result=result)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
