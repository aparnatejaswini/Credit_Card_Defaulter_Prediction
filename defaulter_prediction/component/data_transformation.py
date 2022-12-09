from defaulter_prediction.logger import logging
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.entity.entity_config import DataTransformationConfig
from defaulter_prediction.entity.entity_artifact import DataIngestionArtifact,DataValidationArtifact, DataTransformationArtifact

from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import sys


class ColumnImputer(BaseEstimator,TransformerMixin):
    """
    This is a custom imputer.
    input: column name, values_to_replace, fill_value, 
    output: imputes values_to_replace variable with given fill_value variables
    """

    def __init__(self, col_name, values_to_replace, fill_value):
        self.__col_name = col_name
        self.__fill_value = fill_value
        self.__values_to_replace = values_to_replace

    def fit(self,X):
        self.features_ = self.__col_name
        self.statistic_=self.__fill_value
        self.strategy_='Constant'
        return self
        
    def transform(self, X:pd.DataFrame):
        X[self.__col_name].replace(self.__values_to_replace, self.__fill_value, inplace=True)
        return X[self.__col_name]



class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self,X):
        pay_columns = [col for col in X.columns[X.columns.str.startswith("PAY_")]]
        bill_amt_cols = [col for col in X.columns[X.columns.str.startswith("BILL_AMT")]]
        pay_amt_columns = [col for col in X.columns[X.columns.str.startswith("PAY_AMT")]]
        pay_cat_cols = [col for col in pay_columns if col not in pay_amt_columns ]
        X['avg_bill_amt'] = np.round(X[bill_amt_cols].sum(axis=1)/6, 2)
        X['avg_pay_amt'] = np.round(X[pay_amt_columns].sum(axis=1)/6, 2)
        X['avg_pay_hist'] = np.round(X[pay_cat_cols].sum(axis=1)/6, 2)
        return X
        
    def transform(self,):
        pass


class DataTransformation():
    def __init__(self, config:DataTransformationConfig, 
                        di_artifact: DataIngestionArtifact, 
                            dv_artifact:DataValidationArtifact ):
        try:
            logging.info(f"{'='*20} Data Transformation log started. {'='*20}")
            self.config = config
            self.di_artifact = di_artifact
            self.di_artifact = di_artifact

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def drop_col(df:pd.DataFrame, col:str)->pd.DataFrame:
        """
        This method drops given column col from dataframe df
        Output: pd.DataFrame
        """
        df.drop(columns=col, inplace=True)
        return df


    def __del__(self, ) -> None:
            logging.info(f"{'='*20} Data Transformation log completed successfully. {'='*20}")
