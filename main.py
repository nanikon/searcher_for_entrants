import os
from flask import Flask, render_template, request

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, BooleanField

from search_entrants import collection_and_analysis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it_is_my_very_big-big_secret_my_dear'


class EntrantsForm(FlaskForm):
    list_entrants = TextAreaField('Введите ФИО абитурентов, каждого с новой строки')
    file_entrants = FileField('Загрузите файл .txt с ФИО абитуриентов')
    is_analysis = BooleanField('Добавить аналитику')
    submit = SubmitField('Поиск')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'txt'


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
            file = request.files['file_entrants']
            if file and allowed_file(file.filename):
                data = file.read().decode('utf-8').split('\r\n')
                result = collection_and_analysis(data, form.is_analysis.data)
            else:
                result = ['Файл не найден или у него неправильное расширение']
        else:
            result = ['Вы ничего не ввели']
    return render_template('index.html', form=form, result=result)


if __name__ == '__main__':
    # app.run(port=8080, host='127.0.0.1')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
