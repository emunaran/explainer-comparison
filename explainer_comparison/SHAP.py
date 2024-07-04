# ----------------------------------------------------------------------------------------------------
# Class SHAP
# This clas wraps SHAP explainer methods.
#
# ------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import shap as sh
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from explainer_comparison.Explainer import Explainer


class SHAP(Explainer):
    # initialize with void values

    def explain_global(self, x_data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates global SHAP values (average) for the features in the dataset.

        :param x_data: DataFrame containing the feature data.
        :return: DataFrame of average SHAP values for each feature.
        """
        shap_values = self.explain_local(x_data)

        #if isinstance(self.model, RandomForestClassifier):
        #    global_exp = pd.DataFrame(explainer.shap_values(x_data).mean(axis=1))
        #    feature_importance = pd.DataFrame(abs(explainer.shap_values(x_data)).mean(axis=1))
        #    print("Global Explanation:\n")
        #    print(global_exp)
        #    print("Feature Importance:\n")
        #    print(feature_importance)
        #elif isinstance(self.model, RandomForestRegressor):

        shap_mean = np.mean(shap_values, axis=0)

        return pd.DataFrame(shap_mean, index=x_data.columns, columns=['SHAP Value'])


    def chooseExplainer(self, model_type: str) -> sh.Explainer:
        """
        Selects an appropriate SHAP explainer based on the model type.

        :param model_type: A string describing the type of the model
        :return: A SHAP Explainer class or None if no appropriate explainer is found
        """
        model_type = model_type.lower()

        if "tree" in model_type or "forest" in model_type:
            return sh.TreeExplainer
        elif "linear" in model_type:
            return sh.LinearExplainer
        else:
            return sh.KernelExplainer

    def explain_local(self, x_data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates local SHAP values for the given data points.

        :param x_data: DataFrame containing the feature data.
        :return: DataFrame of SHAP values for each feature and data point.
        """
        explainer_class = self.chooseExplainer(type(self.model).__name__)

        # background = pd.DataFrame(np.median(x_data, axis=0), index=x_data.columns).T
        background = sh.kmeans(x_data, 5).data if explainer_class.__name__ != "LinearExplainer" else x_data

        explainer = explainer_class(self.model, background)
        shap_values = explainer.shap_values(x_data, check_additivity=False)
        
        if not isinstance(shap_values, list):
            # Regression task or classification with linear model
            shap_df = pd.DataFrame(shap_values, columns=x_data.columns)

        elif len(shap_values)==2:
            # Binary classification task
            # In binary classification tasks, SHAP returns two items in the shap_values array.
            # The item at index 0 represents the SHAP values for the negative class (label 0),
            # and the item at index 1 represents the SHAP values for the positive class (label 1).
            # Here, we are taking only the SHAP values for the negative class.
            shap_df = pd.DataFrame(shap_values[0], columns=x_data.columns) 

        else:       # Multiclass
            # Stack the arrays and average over classes (axis=-1)
            stacked_shap_values = np.stack(np.abs(shap_values), axis=-1)
            mean_abs_shap_values = np.mean(stacked_shap_values, axis=-1)
            shap_df = pd.DataFrame(mean_abs_shap_values, columns=x_data.columns)

        return shap_df
