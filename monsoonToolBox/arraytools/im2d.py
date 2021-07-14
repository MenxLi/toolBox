import numpy as np
from .arrayBase import Array2D

class Img2D(Array2D):
    def imgChannel(img: np.ndarray)->int:
        if len(img.shape)==3:
            return img.shape[2]
        if len(img.shape)==2:
            return 1


class Mask2D(Array2D):
    def getCentroid2d(msk: np.ndarray):
        xs = list(range(msk.shape[1]))*msk.shape[0]
        xs = np.array(xs)[..., np.newaxis]
        ys = list(range(msk.shape[0]))*msk.shape[1]
        ys = np.array(ys).transpose()[..., np.newaxis]
        coords = np.concatenate((xs, ys), axis = -1)
        mask = np.logical_not(msk)[..., np.newaxis]
        mask = np.concatenate((mask, mask), axis = -1)
        msk_coords = np.ma.masked_array(coords, mask = mask)
        return msk_coords.mean(axis = -2).compressed()