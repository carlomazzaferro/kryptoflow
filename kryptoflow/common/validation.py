from kryptoflow.models import conf
from sklearn.base import BaseEstimator


class ModelTypeError(Exception):
    pass


class ModelNameTypeError(Exception):
    pass


class NotInitilizedError(Exception):
    pass


def check_model_type(model_type=None, model=None):
    from kryptoflow.models.model import KerasBaseModel
    if not model:
        if model_type not in conf.ALLOWABLE_MODLES:
            raise ModelNameTypeError('model_type must be either of: %s' % ', '.join(conf.ALLOWABLE_MODLES))
    else:
        if isinstance(model, KerasBaseModel):
            return 'keras'
        elif isinstance(model, BaseEstimator):
            return 'sklearn'
        else:
            raise ModelNameTypeError('Model must be either a Keras complied model or an sklearn model')



