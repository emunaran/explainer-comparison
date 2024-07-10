# ----------------------------------------------------------------------------------------------------
# Class Permutations
#
# This class wraps the permutation explainer
#
# ------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error

# Local application imports
from xai_compare.explainer import Explainer


class PermutationFeatureImportance(Explainer):
    def __init__(self, model, X_train, y_train, num_permutations=5, random_state=None, mode='regression'):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.num_permutations = num_permutations
        self.random_state = random_state
        self.mode = mode
 
    def explain_global(self, X_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates permutation feature importance for a given model.
        
        Parameters:
        - X_data: The feature matrix.
        
        Returns:
        - feature_importances_df: A DataFrame containing the feature names and their mean importance.
        """
        np.random.seed(self.random_state)

        if self.mode == 'classification':
            scorer = accuracy_score
        elif self.mode == 'regression':
            scorer = mean_squared_error

        # Initialize a dictionary to store importance scores for each feature
        feature_importances = {feature: [] for feature in X_data.columns}
        
        # Loop over each feature to permute and evaluate its importance
        for feature in X_data.columns:
            for _ in range(self.num_permutations):
                # Permute the current feature
                X_data_permuted = X_data.copy()
                X_data_permuted[feature] = np.random.permutation(X_data[feature])
                # Evaluate the model with the permuted feature and calculate the importance score
                importance_score = scorer(self.model.predict(X_data), self.model.predict(X_data_permuted))
                feature_importances[feature].append(importance_score)

        # Average the importance scores over the number of repeats
        averaged_importances = {feature: np.mean(importances) for feature, importances in feature_importances.items()}
        
        # Normalize the importance scores to sum to 1 (for comparability with other explainers)
        total_importance = sum(averaged_importances.values())
        normalized_importances = {feature: importance / total_importance for feature, importance in averaged_importances.items()}
        
        # Convert to DataFrame 
        feature_importances_df = pd.DataFrame.from_dict(normalized_importances, orient='index', columns=['importance'])
        
        return feature_importances_df
    

    def explain_local(self, X_data: pd.DataFrame) -> pd.DataFrame:
        """
        This function is not applicable for permutation feature importance as it is a global method.
        """
        raise NotImplementedError("The explain_local method is not applicable for permutation feature importance.")