from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class CovidModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(100))
    confirmed = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Integer, nullable=True)
    recovered = db.Column(db.Integer, nullable=True)
    deaths = db.Column(db.Integer, nullable=True)
    new_cases = db.Column(db.Integer, nullable=True)

#db.create_all()

covid_put_args = reqparse.RequestParser()
covid_put_args.add_argument("confirmed", type=int, help="1")
covid_put_args.add_argument("active", type=int, help="2")
covid_put_args.add_argument("recovered", type=int, help="2")
covid_put_args.add_argument("deaths", type=int, help="2")
covid_put_args.add_argument("new_cases", type=int, help="2")

covid_update_args = reqparse.RequestParser()
covid_update_args.add_argument("confirmed", type=int, help="1")
covid_update_args.add_argument("active", type=int, help="2")
covid_update_args.add_argument("recovered", type=int, help="2")
covid_update_args.add_argument("deaths", type=int, help="2")
covid_update_args.add_argument("new_cases", type=int, help="2")

resource_fields = {
    'id': fields.Integer,
    'country': fields.String,
    'confirmed': fields.Integer,
    'active': fields.Integer,
    'recovered': fields.Integer,
    'deaths': fields.Integer,
    'new_cases': fields.Integer
}

class Covid(Resource):
    @marshal_with(resource_fields)
    def get(self, country):
        result = CovidModel.query.filter_by(country=country).first()
        if not result:
            abort(404, message="No such country")
        return result

    @marshal_with(resource_fields)
    def post(self, country):
        check_country = CovidModel.query.filter_by(country=country).all()
        print(check_country)
        if check_country:
            abort(404, message='error')
        args = covid_put_args.parse_args()
        case = CovidModel(country=country, confirmed=args['confirmed'], active=args['active'], recovered=args['recovered'], deaths=args['deaths'], new_cases=args['new_cases'])
        db.session.add(case)
        db.session.commit()
        return case

    @marshal_with(resource_fields)
    def patch(self, country):
        args = covid_update_args.parse_args()
        result = CovidModel.query.filter_by(country=country).first()
        if not result:
            abort(404, message='no video')
        if args['confirmed']:
            result.confirmed = args['confirmed']
        if args['active']:
            result.active = args['active']
        if args['recovered']:
            result.recovered = args['recovered']
        if args['deaths']:
            result.deaths = args['deaths']
        if args['new_cases']:
            result.new_cases = args['new_cases']

        db.session.commit()
        return result

    def delete(self, country):
        result = CovidModel.query.filter_by(country=country).delete()
        if not result:
            abort(404, message="No such country")
        db.session.commit()
        return 202

class AllInfo(Resource):
    @marshal_with(resource_fields)
    def get(self, ):
        all_info = CovidModel.query.all()
        return all_info

api.add_resource(Covid, "/countries/<string:country>")
api.add_resource(AllInfo, "/all")

if __name__ == '__main__':
    app.run(debug=True)