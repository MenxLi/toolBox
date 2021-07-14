from typing import Union
import numpy as np
from numpy.lib.arraysetops import isin
import pandas as pd
import matplotlib.pyplot as plt


class StatBasic:
    def __init__(self):
        pass
    @staticmethod
    def meanStd(data: np.ndarray):
        mean = np.mean(data)
        std = np.std(data)
        count = len(data)
        return {
                "mean": mean,
                "std": std,
                "count": count
                }
    @staticmethod
    def getFormattedMeanStd(data: np.ndarray, tag = "Mean and Std"):
        statistic = StatBasic.meanStd(data)
        mean_std = "Mean: {mean} | Std: {std} - count: {count}".format(statistic["mean"], statistic["std"], statistic["count"])
        string = "{}: \n\t{}".format(tag, mean_std)
        return string

class Stat1D(StatBasic):
    @staticmethod
    def washNone(data: Union[np.ndarray, list]):
        """
        Delete (wash out) all None items in the list and return residual items and None count
        data - 1D or array of number or None
        return data_washed, none_count
        """
        if isinstance(data, list):
            data = np.array(data)
        none_mask = data == None
        none_count = none_mask.sum()
        data_ = np.ma.masked_array(data, none_mask).compressed()
        return data_, none_count
