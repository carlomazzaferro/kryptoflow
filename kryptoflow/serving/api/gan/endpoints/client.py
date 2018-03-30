import json
from flask_restplus import Resource
from kryptoflow.serving.api.restplus import api
from kryptoflow.serving.api.gan.logic.tf_serving_client import make_prediction, _load_and_transform_data


# create dedicated namespace for GAN client
ns = api.namespace('prediction_client', description='Operations for client predictions')


# Flask-RestPlus specific parser for image uploading
UPLOAD_KEY = 'image'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()


@ns.route('/prediction')
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
        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            results = make_prediction(payload)
            return json.loads(results['val']), 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
