from abc import ABCMeta, abstractmethod

import numpy as np
import random

from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score

# ------------------------------------------------------------------ CLASSIFIERS
class WeakClassifier(BaseEstimator):

    def __init__(self):
        pass

    @abstractmethod
    def predict(self, x):
        pass

    def score(self, x, y, sample_weight=None):

        y_pred = self.predict(x)
        return accuracy_score(y, y_pred, sample_weight=sample_weight)

class LinearClassifier(WeakClassifier):

    def __init__(self, d, h=None):

        if h is None:
            self.h = np.zeros((1, d))
        else:
            self.h = h

    def predict(self, x):
        return np.sign(np.inner(x, self.h))[:, None]

class RandomClassifier(WeakClassifier):

    def predict(self, x):
        r = np.random.randint(2, size=x.shape[0])
        r[r==0] = -1
        return r

class StumpClassifier(WeakClassifier):

    def __init__(self, index, threshold, sign):

        self.id = index
        self.thr = threshold
        self.sign = sign

    def predict(self, x):
        return self.sign * (1 - 2*(x[:, self.id] > self.thr))[:, None]


# ---------------------------------------------------------------- BASE CLFS GENERATION

def get_basis(n, d, *args):

    vectors = np.eye(n, d)
    base_clfs = [LinearClassifier(d, v) for v in vectors]

    return base_clfs

def get_double_basis(n, d, *args):
    assert n % 2 == 0

    vectors = np.append(np.eye(n // 2, d), -np.eye(n // 2, d), axis=0) 
    base_clfs = [LinearClassifier(d, v) for v in vectors]

    return base_clfs

def get_stumps(n, d, min_v, max_v):

    # get nb_clfs/dimensions regular thresholds
    interval = 2 * (max_v - min_v) * d / (n + 1)
    thresholds = [min_v + (i+1)*interval for i in range(n//(2*d) + 1)]

    base_clfs = []

    for j in range(d): 
        base_clfs += [StumpClassifier(j, t, 1) for t in thresholds]
        base_clfs += [StumpClassifier(j, t, -1) for t in thresholds]

    return random.sample(base_clfs, n)

def get_rnd_linear_clfs(n, d, rnd_seed, *args):
    assert n % 2 == 0

    np.random.seed(rnd_seed)
    vectors = np.random.random((n // 2, d))
    base_clfs = [LinearClassifier(d, v) for v in vectors]
    base_clfs += [LinearClassifier(d, -v) for v in vectors]

    return base_clfs