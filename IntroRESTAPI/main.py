from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record


@app.route("/random")
def get_random_cafe():
    group = db.session.execute(db.select(Cafe))
    all_cafes = group.scalars().all()
    selection = random.choice(all_cafes)
    return jsonify(cafe=selection.to_dict())


@app.route("/all")
def get_all():
    group = db.session.execute(db.select(Cafe))
    group_list = group.scalars().all()
    all_cafes = [item.to_dict() for item in group_list]
    return jsonify(cafes=all_cafes)


@app.route("/search")
def get_location():
    loc = request.args.get('loc')
    all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalars().all()
    if all_cafes:
        return jsonify(cafes=[item.to_dict() for item in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we dont have a cafe at that location"})


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update(cafe_id):
    new_price = request.args.get('new_price')
    selected = db.session.get(Cafe, cafe_id)  # when using get_or_404 to look for an item, if it's not on the database,
    # it will give a standard 404 message, bypassing the later else statement, that why we use just db.session.get
    if selected:
        selected.coffee_price = new_price
        db.session.commit()
        return jsonify(success="Successfully updates the price") , 200
    else:
        return jsonify(error={"not found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    key = request.args.get('api_key')
    if cafe:
        if key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success="The cafe was successfully deleted from the Database"), 202
        else:
            return jsonify(error="Sorry, That's not allowed. Make sure you have the correct api_key."),403
    else:
        return jsonify(error={"not found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
