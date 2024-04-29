# Import Dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


# define application and database variables
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app_version = "v1/"


# create the data definition
class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(100), nullable=False)
    exchange_rate = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    worth = db.Column(db.Integer, nullable=False)
    gameID = db.Column(db.Integer, nullable=False)
    salePrice = db.Column(db.Integer, nullable=False)

    # outputs to log/screen to verify data visually
    def __repr__(self):
        return f"DataModel(country = {country}, currency = {currency}, exchange_rate = {exchange_rate}, title = {title}, worth = {worth},  gameID = {gameID}, salePrice = {salePrice})"


# run this statement the first thme to create the database structure
# db.create_all()

# handle the incoming data request with a parser
# arguments for a put request
data_put_args = reqparse.RequestParser()
data_put_args.add_argument(
    "country", type=str, help="Name of the country is required", required=True
)
data_put_args.add_argument("currency", type=str, help="Type of currency", required=True)
data_put_args.add_argument(
    "exchange_rate", type=int, help="Rate of exchange", required=True
)
data_put_args.add_argument(
    "title", type=str, help="Name of the title is required", required=True
)
data_put_args.add_argument(
    "worth", type=int, help="How much it is worth", required=True
)
data_put_args.add_argument("gameID", type=int, help="GameID is required", required=True)
data_put_args.add_argument("salePrice", type=int, help="Price of game", required=True)

# arguments for an update request

data_update_args = reqparse.RequestParser()
data_update_args.add_argument(
    "country", type=str, help="Name of the country is required"
)
data_update_args.add_argument("currency", type=str, help="Type of currency")
data_update_args.add_argument("exchage_rate", type=int, help="Rate of exchange")
data_update_args.add_argument("title", type=str, help="Name of the title is required")
data_update_args.add_argument("worth", type=int, help="How much it is worth")
data_update_args.add_argument("gameID", type=int, help="gameID is required")
data_update_args.add_argument("salePrice", type=int, help="Price of game")

# Map the types to columns extracted from the database object

resource_fields = {
    "id": fields.Integer,
    "country": fields.String,
    "currency": fields.String,
    "exchange_rate": fields.Integer,
    "title": fields.String,
    "worth": fields.Integer,
    "gameID": fields.Integer,
    "salePrice": fields.Integer,
}


# Set up the Resource Functions for CRUD
class Data(Resource):

    # GET (READ in CRUD)
    # @marshal_with serializes output from the DB as a dictionary (json object) so we can work with it in python
    @marshal_with(resource_fields)
    def get(self, data_id):
        result = DataModel.query.filter_by(id=data_id).first()
        if not result:
            abort(404, message="Could not find data with that id")
        return result, 201

    # POST (CREATE in CRUD)
    @marshal_with(resource_fields)
    def put(self, data_id):
        args = data_put_args.parse_args()
        result = DataModel.query.filter_by(id=data_id).first()
        if result:
            abort(409, message="Data id taken...")

        data = DataModel(
            id=data_id,
            country=args["country"],
            currency=args["currency"],
            exchange_rate=args["exchange_rate"],
            title=args["title"],
            worth=args["worth"],
            gameID=args["gameID"],
            salePrice=args["salePrice"],
        )
        db.session.add(data)
        db.session.commit()
        return data, 201

    # PUT (UPDATE in CRUD)
    @marshal_with(resource_fields)
    def patch(self, data_id):
        args = data_update_args.parse_args()
        result = DataModel.query.filter_by(id=data_id).first()
        if not result:
            abort(404, message="Data doesn't exist, cannot update")

        if args["country"]:
            result.country = args["country"]
        if args["currency"]:
            result.currency = args["currency"]
        if args["exchange_rate"]:
            result.exchange_rate = args["exchange_rate"]
        if args["title"]:
            result.title = args["title"]
        if args["worth"]:
            result.worth = args["worth"]
        if args["gameID"]:
            result.gameID = args["gameID"]
        if args["salePrice"]:
            result.salePrice = args["salePrice"]

        db.session.commit()

        return result, 200

    # DELETE (DELETE in CRUD)
    def delete(self, data_id):
        abort_if_data_id_doesnt_exist(data_id)
        del Data[data_id]
        return "", 204


# Register the Resource called data to the API (remember to change versions when making changes for submission)
api.add_resource(Data, "/" + app_version + "data/<int:data_id>")

# Run the API body
if __name__ == "__main__":
    app.run(debug=True)
