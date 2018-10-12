import json
from flask_restplus import Resource, Namespace
from kryptoflow.api.helpers.tf_serving_client import make_prediction, _load_and_transform_data


# create dedicated namespace for GAN client
ns = Namespace('predict', description='Operations for client predictions')


@ns.route('/')
class Prediction(Resource):
    @ns.doc(description='Predict the house number on the image using GAN model. ' +
            'Return 3 most probable digits with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    def post(self):
        try:
            payload = _load_and_transform_data()
            print(payload)
        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            results = make_prediction(payload)
            return json.loads(results['val']), 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
