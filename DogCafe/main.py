import csv
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired(message="Please write the Cafe's name")])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[URL(message="invalid URL")])
    opening = StringField('Opening Time e.g. 8:00 AM',
                          validators=[DataRequired(message="Please write the Cafe's opening time")])
    closing = StringField('Closing Time e.g. 5:30 PM ',
                          validators=[DataRequired(message="Please write the Cafe's closing time")])
    coffee = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    submit = SubmitField(label='Add')


app = Flask(__name__)
app.secret_key = "DSTV"
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/cafes")
def cafes():
    with open('DataCafes.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows, long=len(list_of_rows))


@app.route("/add", methods=['GET', 'POST'])
def new_cafe():
    new_form = CafeForm()

    if new_form.validate_on_submit():
        with open(file='DataCafes.csv', mode='a', encoding="utf-8") as extra:
            extra.write(f"{new_form.name.data},"
                        f"{new_form.location.data},"
                        f"{new_form.opening.data},"
                        f"{new_form.closing.data},"
                        f"{new_form.coffee.data},"
                        f"{new_form.wifi.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=new_form)


if __name__ == "__main__":
    app.run(debug=True)
