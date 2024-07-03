from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DSTV'
bootstrap = Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Anime-Top.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class TopAnime(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)


class AnimeForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired(message='Please Type Your Rating')])
    review = StringField('Your Review', validators=[DataRequired(message='Please Write Your Review')])
    submit = SubmitField(label='Done')


class SearchForm(FlaskForm):
    title = StringField('Anime Name', validators=[DataRequired(message='Please Write the Anime name')])
    submit = SubmitField(label='Add')


with app.app_context():
    db.create_all()


def api_anime(name):
    header = {"X-MAL-CLIENT-ID": "687f086ab6df7e0f3a4ff5c6162c3ca0"}
    first_parameter = {'q': name}
    second_parameter = {'fields': ['start_season, synopsis']}

    response = requests.get(url="https://api.myanimelist.net/v2/anime", headers=header, params=first_parameter)
    anime_data = response.json()['data']
    identity = 0
    for item in anime_data:
        if item['node']['title'] == name:
            identity = item['node']['id']

    second_response = requests.get(url=f"https://api.myanimelist.net/v2/anime/{identity}", headers=header,
                                   params=second_parameter)
    img_url = second_response.json()['main_picture']['medium']
    year = second_response.json()['start_season']['year']
    synopsis = second_response.json()['synopsis']
    extract = [img_url, year, synopsis]
    return extract


@app.route("/")
def home():
    anime = db.session.execute(db.select(TopAnime).order_by(TopAnime.rating))
    all_anime = anime.scalars().all()  # Convert ScalarResult to Python List
    for n in range(len(all_anime)):
        all_anime[n].ranking = len(all_anime) - n
        db.session.commit()
    return render_template("index.html", data=all_anime)


@app.route("/edit", methods=['GET', 'POST'])
def update():
    first_form = AnimeForm()
    if first_form.validate_on_submit():
        new_rating = first_form.rating.data
        new_review = first_form.review.data
        anime_id = request.args.get('id')
        selection = db.get_or_404(TopAnime, anime_id)
        selection.rating = new_rating
        selection.review = new_review
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', fir_form=first_form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    second_form = SearchForm()
    if second_form.validate_on_submit():
        main_data = api_anime(name=second_form.title.data)
        new_anime = TopAnime(
            title=second_form.title.data,
            year=main_data[1],
            description=main_data[2],
            rating=0,
            ranking=0,
            review="",
            img_url=main_data[0]
        )
        db.session.add(new_anime)
        db.session.commit()
        return redirect(url_for('update', id=new_anime.id))
    return render_template("add.html", sec_form=second_form)


@app.route("/delete")
def delete():
    anime_id = request.args.get('id')
    selection = db.get_or_404(TopAnime, anime_id)
    db.session.delete(selection)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
