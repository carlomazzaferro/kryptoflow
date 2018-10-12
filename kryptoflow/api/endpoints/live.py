from flask import request
from flask_restplus import Resource, Namespace
from flask_restplus.reqparse import RequestParser


# create dedicated namespace for GAN client
ns = Namespace('historic', description='Operations for retrieving historical data')

parser = RequestParser()
parser.add_argument('offset', type=int, required=True)
parser.add_argument('max_points', type=int, required=False)


@ns.route('/')
class HistoricData(Resource):
    @ns.doc(description='Predict the house number on the image using GAN model. ' +
                        'Return 3 most probable digits with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
            })
    @ns.expect(parser)
    def get(self):
        try:
            payload = get_historic_data(int(request.args['offset']), max_points=int(request.args['max_points']))
        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            results = format_data(payload)
            return results, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
