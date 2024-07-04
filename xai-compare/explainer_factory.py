# ----------------------------------------------------------------------------------------------------
# Class ExplainerFactory
# This class is used to create Explainer objects based on what word is entered into the create() function
#
# ------------------------------------------------------------------------------------------------------

import string
from typing import Any

import pandas as pd

# Local application imports
from explainer import Explainer
from lime_wrapper import LIME
from shap_wrapper import SHAP
from ebm_wrapper import EBM
from mimic_expl_wrapper import MimicExpl
from config import MODE


class ExplainerFactory:
    # If user wants to use XGBoost explanation, model, X, and y must be filled in as parameters for init
    # all possible parameters are set to None as default.
    '''def __init__(self,
                 model: Any = None,
                 X: pd.DataFrame = None,
                 y: pd.DataFrame = None,
                 val_X: pd.DataFrame = None,
                 train_X: pd.DataFrame = None,
                 val_y: pd.DataFrame = None,
                 train_y: pd.DataFrame = None):
        self.model = model
        self.X = X
        self.y = y
        self.val_X = val_X
        self.val_y = val_y
        self.train_X = train_X
        self.train_y = train_y'''

    def __init__(self,
                 model: Any = None,
                 X_train: pd.DataFrame = None,
                 X_test: pd.DataFrame = None,
                 y_train: pd.DataFrame = None,
                 y_test: pd.DataFrame = None,
                 mode: str = MODE.REGRESSION):
        self.model = model
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.mode = mode


    def create_explainer(self, explainer_type: string) -> Explainer:
        if explainer_type == "shap":
            shapEx = SHAP(self.model, self.X_train, self.y_train)
            return shapEx
        elif explainer_type == "lime":
            limeEx = LIME(self.model, self.X_train, self.y_train)
            return limeEx
        if explainer_type == "ebm":
            ebmEx = EBM(self.model, self.X_train, self.y_train)
            return ebmEx
        elif explainer_type == "mimic":
            mimicEx = MimicExpl(self.model, self.X_train, self.y_train)
            return mimicEx

        # If there are more explainers you want to account for, the code can be added here:

        else:
            # throw exception
            print("invalid Explainer")