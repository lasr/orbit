"""Created on Wed Sep 07 2015 16:36.

@author: Nathan Budd
"""
import numpy as np
import numpy.linalg as npl
import numpy.matlib as npm
from .model_orbital_elements import ModelOrbitalElements


class ModelMEE(ModelOrbitalElements):
    """MEE two-body model.

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

        X = [p f g h k L]

        See dynamics_abstract.py for more details.
        """
        # Ldot = sqrt(mu p) / r^2
        # r = p / (1. + f*cL + g*sL)
        cL = np.cos(X[:, -1])
        sL = np.sin(X[:, -1])
        p = X[:, 0]
        f = X[:, 1]
        g = X[:, 2]
        r = p / (1. + np.multiply(f, cL) + np.multiply(g, sL))
        Ldot = np.power(self.mu * p, .5) / np.power(r, 2)

        shape = X.shape
        zeros = npm.zeros((shape[0], shape[1]-1))
        self.Xdot = np.concatenate((zeros, Ldot), 1)

        return self.Xdot
