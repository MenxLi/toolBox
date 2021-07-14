import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .basic import StatBasic

"""Methods for 1D bool array"""

class Bool1D(StatBasic):
    """Methods for 1d bool array"""
    @staticmethod
    def _getFormattedPercentage(data: np.ndarray, tag: str = "Percentage"):
        percentage = Bool1D._calcPercentage(data)
        string = "{}: \n\t{}".format(tag, percentage)
        return string
    
    @staticmethod
    def _calcPercentage(data: np.ndarray):
        """data: 1D bool|int array of 0|1"""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        data = data.astype(np.int)
        percentage = data.sum()/len(data)
        return percentage
    
    @staticmethod
    def calcConfusion(y_true: np.ndarray, y_pred:np.ndarray):
        """
        Calculate confusion matrix, 
        - y_true and y_pred: 1D array of T/F | 1/0
        """
        if not isinstance(y_true, np.ndarray):
            y_true = np.array(y_true)
        if not isinstance(y_pred, np.ndarray):
            y_pred = np.array(y_pred)
        y_true = y_true.astype(np.bool)
        y_pred = y_pred.astype(np.bool)
        d_size = len(y_true)
        TP = np.logical_and(y_true, y_pred).astype(np.int).sum()/d_size
        TN = np.logical_and(np.logical_not(y_true), np.logical_not(y_pred)).astype(np.int).sum()/d_size
        FN = np.logical_and(y_true, np.logical_not(y_pred)).astype(np.int).sum()/d_size
        FP = np.logical_and(np.logical_not(y_true), y_pred).astype(np.int).sum()/d_size
        confusion = {
            "TP": TP,
            "TN": TN,
            "FN": FN,
            "FP":FP
        }
        return confusion

    @staticmethod
    def plotConfusion(y_true, y_pred):
        # https://datatofish.com/confusion-matrix-python/
        import seaborn as sn
        if not isinstance(y_true, np.ndarray):
            y_true = np.array(y_true).astype(np.int)
        if not isinstance(y_pred, np.ndarray):
            y_pred = np.array(y_pred).astype(np.int)
        data = {'y_Actual': y_true,
        'y_Predicted': y_pred }
        df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
        confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'], margins = True)

        sn.heatmap(confusion_matrix, annot=True)
        plt.show()

    @staticmethod
    def _getFormattedConfusionMatrix(self, confusion, tag = "Confusion matrix"):
        data = {"pred_0": pd.Series([confusion["TN"], confusion["FN"]], index = ["true_0", "true_1"]),
                "pred_1": pd.Series([confusion["FP"], confusion["TP"]], index = ["true_0", "true_1"])}
        df = pd.DataFrame(data)
        string = "{}: \n{}".format(tag, df.to_string())
        return string
