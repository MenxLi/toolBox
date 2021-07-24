import numpy as np
from typing import Union, List

class ArrayBase:
	def __init__(self) -> None:
		pass
	@staticmethod
	def stretchArr(arr: np.ndarray, min_val: Union[int, float] = 0, max_val: Union[int, float] = 255)-> np.ndarray:
		if not isinstance(arr, np.ndarray):
			raise Exception("Input should be an ndarray")
		arr = arr.astype(float)
		a = (arr-arr.min())/(arr.max()-arr.min())
		a = a*(max_val-min_val)+min_val
		return a
	@staticmethod
	def mapMatUint8(arr: np.ndarray)->np.ndarray:
		return ArrayBase.stretchArr(arr, 0, 255).astype(np.uint8)

ArrayNd = ArrayBase

class Array2D(ArrayNd):
	@staticmethod
	def gray2rgb(img: np.ndarray)->np.ndarray:
		new_img = np.concatenate((img[:,:,np.newaxis], img[:,:,np.newaxis], img[:,:,np.newaxis]), axis=2)
		return new_img