import json
from flask import request
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser
from kryptoflow.serving.backend.api.restplus import api


# create dedicated namespace for GAN client
ns = api.namespace('test', description='Operations for retrieving historical data')


@ns.route('/random')
class HistoricData(Resource):
    @ns.doc(description='Predict the house number on the image using GAN model. ' +
                        'Return 3 most probable digits with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
            })
    def post(self):
        from random import randint
        from flask import jsonify
        response = {
            'randomNumber': randint(1, 100)
        }
        return jsonify(response)

