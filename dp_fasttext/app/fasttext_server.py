"""
Defines a custom Sanic app with ML model(s) attached
"""
import logging
from dp4py_sanic.app.server import Server

from dp_fasttext.config import CONFIG
from dp_fasttext.ml.supervised import SupervisedModel
from dp_fasttext.ml.unsupervised import UnsupervisedModel
from dp_fasttext.api.request.fasttext_request import FasttextRequest
from dp_fasttext.app.ml.supervised_models_cache import get_supervised_model
from dp_fasttext.app.ml.unsupervised_models_cache import get_unsupervised_model


class FasttextServer(Server):

    def __init__(self, log_namespace: str, name=None, router=None, error_handler=None,
                 load_env=True,
                 strict_slashes=False,
                 configure_logging=True):
        super(FasttextServer, self).__init__(log_namespace, name=name, router=router, error_handler=error_handler,
                                             load_env=load_env, request_class=FasttextRequest,
                                             strict_slashes=strict_slashes,
                                             configure_logging=configure_logging)

        self.supervised_filename = CONFIG.ML.supervised_model_filename
        self.unsupervised_filename = CONFIG.ML.unsupervised_model_filename

        # Initialise model
        logging.info("Initialising fastText model", extra={
            "params": {
                "filename": self.supervised_filename
            }
        })
        model: SupervisedModel = self.get_supervised_model()
        logging.info("Successfully initialised fastText model", extra={
            "params": {
                "filename": self.supervised_filename,
                "matrix_dimensions": "(%d, %d)" % (len(model.get_words()), model.get_dimension())
            }
        })

    def get_supervised_model(self) -> SupervisedModel:
        """
        Returns the ONS supervised fasttext model
        :return:
        """
        logging.debug("Fetching cached supervised model", extra={
            "params": {
                "filename": self.supervised_filename
            }
        })

        return get_supervised_model(self.supervised_filename)

    def get_unsupervised_model(self) -> UnsupervisedModel:
        """
        Returns the ONS supervised fasttext model
        :return:
        """
        logging.debug("Fetching cached unsupervised model", extra={
            "params": {
                "filename": self.unsupervised_filename
            }
        })

        return get_unsupervised_model(self.unsupervised_filename)