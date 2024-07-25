from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL, NumberRange
import csv
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.secret_key
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(label='Location URL', validators=[DataRequired(), URL(message=None)])
    open = StringField(label='Open Time', validators=[DataRequired()])
    close = StringField(label='Closing Time', validators=[DataRequired()])
    coffee = SelectField(label='Coffee Rating',choices=[('✘'),('☕️'),('☕️☕️'),('☕️☕️☕️'),('☕️☕️☕️☕️'),('☕️☕️☕️☕️☕️')],coerce=str, validators=[DataRequired()])
    wifi = SelectField(label='Wifi Rating', choices=[('✘'),('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')], coerce=str, validators=[DataRequired()])
    power = SelectField(label='Power Outlet Rating', choices=[('✘'),('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')],coerce=str, validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.data)
        name_cafe = form.cafe.data
        list = [name_cafe, form.location.data, form.open.data, form.close.data, form.coffee.data, form.wifi.data, form.power.data]
        with open('cafe-data.csv', "a", encoding='utf-8') as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(list)
            csv_file.close()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
