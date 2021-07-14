from os import EX_PROTOCOL
import numpy as np 
import numba as nb
from typing import Union, List
from .arrayBase import ArrayBase

class EvalBase(ArrayBase):
	def __init__(self) -> None:
		pass
	
	@staticmethod
	def iou(mask1: np.ndarray, mask2: np.ndarray) -> float:
		"""
		mask1 and mask2: n dimensional np array of 0 or 1
		"""
		epsilon = 1e-7
		intersection = np.logical_and(mask1, mask2)
		intersection = intersection.sum()
		union = np.logical_or(mask1, mask2)
		union = union.sum() + epsilon
		return intersection/union

	@staticmethod
	def dice(mask1: np.ndarray, mask2: np.ndarray) -> float:
		"""
		mask1 and mask2: n dimensional np array of 0 or 1
		"""
		epsilon = 1e-7
		intersection = np.logical_and(mask1, mask2)
		intersection = intersection.sum()
		denominator = mask1.sum() + mask2.sum() + epsilon
		return 2*intersection/denominator

	@staticmethod
	def batchIou(mask1s: np.ndarray, mask2s: np.ndarray) -> np.ndarray:
		"""
		calculate ious of a batch of images
		returns 1D array
		"""
		assert mask1s.shape == mask2s.shape, "The masks should have same shape"
		epsilon = 1e-7
		dim = len(mask1s.shape)
		intersection = np.logical_and(mask1s, mask2s)
		union = np.logical_or(mask1s, mask2s)
		for i in range(dim-1):
			intersection = intersection.sum(axis = -1)
			union = union.sum(axis = -1)
		union = union + epsilon
		return intersection/union

	@staticmethod
	def batchDice(mask1s: np.ndarray, mask2s: np.ndarray) -> np.ndarray:
		"""
		calculate dices of a batch of images
		returns 1D array
		"""
		assert mask1s.shape == mask2s.shape, "The masks should have same shape"
		epsilon = 1e-7
		dim = len(mask1s.shape)
		intersection = np.logical_and(mask1s, mask2s)
		_mask1s = mask1s.copy()
		_mask2s = mask2s.copy()
		for i in range(dim-1):
			intersection = intersection.sum(axis = -1)
			_mask1s = _mask1s.sum(axis = -1)
			_mask2s = _mask2s.sum(axis = -1)
		denominator = _mask1s + _mask2s + epsilon
		return 2*intersection/denominator

	@staticmethod
	def batchIouLoop(mask1s: np.ndarray, mask2s: np.ndarray) -> np.ndarray:
		"""
		####### For testing propose, use batchIou instead ##########
		calculate ious of a batch of images
		returns 1D array
		"""
		assert mask1s.shape == mask2s.shape, "The masks should have same shape"
		epsilon = 1e-7
		output = np.array([], dtype=float)
		for m1, m2 in zip(mask1s, mask2s):
			intersection_bool = np.logical_and(m1, m2)
			intersection = intersection_bool.sum()
			union_bool = np.logical_or(m1, m2)
			union = union_bool.sum() + epsilon
			_iou = intersection/union
			output = np.concatenate((output, [_iou]))
		return output
