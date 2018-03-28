from keras.models import model_from_json
import keras.backend as K
import os
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def


class ModelExporter(object):
    """
    Save model as:
        - json
        - Weights: .h5 files;
        - Protobuf: for loading into TensorFlow Serving
        - Checkpoints: also for TF Serving

    The models will live in the directory `stored_models/i/` where i is an integer which is assigned automatically.
    Within that directory, there will be a `tf` and a `keras` directory, where each of the versions of the serialized
    model will be stored.
    """

    def __init__(self, model):
        """
        Args:
            model (keras.Model): compiled keras model
        """
        self.model = model
        self.models_dir = 'stored_models'

    def store(self, name):
        self._store_keras(name)
        self._store_tf(name)

    @property
    def path_id(self):
        existing_models = sorted([int(i) for i in os.listdir(self.models_dir)])
        return existing_models[-1] + 1

    @property
    def keras_model_path(self):
        return os.path.join(self.models_dir, str(self.path_id), 'keras')

    @property
    def tf_model_path(self):
        return os.path.join(self.models_dir, str(self.path_id), 'tf')

    def _store_keras(self, name):
        K.set_learning_phase(0)  # necessary to prevent model from modifying weights

        os.makedirs(self.keras_model_path)
        model_json = self.model.to_json()
        with open(os.path.join(self.keras_model_path, name + '.json'), 'w') as json_file:
            json_file.write(model_json)
        self.model.save_weights(os.path.join(self.keras_model_path, name + '.h5'))
        print("Saved Keras model to disk")

    def _store_tf(self, name):

        json_model_file = open(os.path.join(self.keras_model_path, name + '.json'), "r").read()
        loaded_model = model_from_json(json_model_file)
        loaded_model.load_weights(os.path.join(self.keras_model_path, name + '.h5'))

        builder = saved_model_builder.SavedModelBuilder(self.tf_model_path)
        signature = predict_signature_def(inputs={'states': loaded_model.input},
                                          outputs={'price': loaded_model.output})

        with K.get_session() as sess:
            builder.add_meta_graph_and_variables(sess=sess,
                                                 tags=[tag_constants.SERVING],
                                                 signature_def_map={'predict': signature})
            builder.save()