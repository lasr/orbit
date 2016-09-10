"""Created on Wed Sep 07 2015 16:36.

@author: Nathan Budd
"""
import numpy as np
import numpy.linalg as npl
import numpy.matlib as npm
from .model_orbital_elements import ModelOrbitalElements


class ModelCOE(ModelOrbitalElements):
    """COE two-body model.

    Instance Members
    ----------------
    mu : float
    Standard gravitational parameter
    """

    def __init__(self, mu):
        """."""
        self.mu = mu
        super().__init__()

    def __call__(self, T, X):
        """Evaluate the dynamics at the given times.

        X = [p e i W w f]

        See dynamics_abstract.py for more details.
        """
        p = X[:, 0]
        e = X[:, 1]
        f = X[:, 5]
        r = p / (1. + np.multiply(e, np.cos(f)))
        h = np.power(self.mu * p, .5)
        f_dot = h / np.power(r, 2)

        shape = X.shape
        zeros = npm.zeros((shape[0], shape[1]-1))
        self.Xdot = np.concatenate((zeros, f_dot), 1)

        return self.Xdot
