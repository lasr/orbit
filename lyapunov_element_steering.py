"""Created on Wed Sep 08 2015 15:10.

@author: Nathan Budd
"""
import numpy as np
import numpy.linalg as npl
from math import sin, cos, atan2
from .model_abstract import ModelAbstract
from .gauss_lagrange_planetary_eqns import GaussLagrangePlanetaryEqns as GLPE


class LyapunovElementSteering(ModelAbstract):
    """
    Lyapunov control for orbital elements, neglecting phase angle.

    Phase angle element must be the last (6th) state listed.

    Members
    -------
    mu : float
        Standard gravitational parameter
    W : ndarray
        Diagonal nxn weight array, where n is the state dimension.
    a_t : float
        Thrust magnitude
    Xref : callable
        Can be called with input T (an mx1 ndarray) to produce a reference
        trajectory, X (mxn ndarray), where n is the state dimension defined by
        the Xref.model attribute.
    model : callable
        Can be called with input T (an mx1 ndarray) and X (mxn ndarray)
        to produce state derivatives for this element set.
    glpe : callable
        Can be called with input X (mxn ndarray) to produce a list of ndarrays
        representing the Gauss's form of Lagrange's Planetary Equations for
        each passed state.
    u : ndarray
        Cartesian control history mx3 where m is the number of samples and 3 is
        the control dimension.
    V : ndarray
        Most recent Lyapunov function trajectory, mx1 where m is the number of
        samples.
    Vdot : ndarray
        Most recent Lyapunov function derivative history, mx1 where m is the
        number of samples.
    """

    def __init__(self, mu, W, a_t, Xref, model, glpe):
        """."""
        self.mu = mu
        self.W = W
        self.a_t = a_t
        self.Xref = Xref
        self.model = model
        self.glpe = glpe
        self.u = np.zeros(())
        self.V = np.zeros(())
        self.Vdot = np.zeros(())
        super().__init__()

    def __call__(self, T, X):
        """Evaluate the control at the given times.

        X = [e1 e2 e3 e4 e5 e_phase]

        See dynamics_abstract.py for more details.
        """
        G = self.glpe(X)
        Xref = self.Xref(T)
        Eta = X - Xref

        Xdot = self.model(T, X)
        Xrefdot = self.model(T, Xref)
        Etadot = np.zeros((X.shape))
        Etadot[0:, -1:] = Xdot[0:, -1:] - Xrefdot[0:, -1:]

        U = np.zeros(X.shape)
        self.u = np.zeros((X.shape[0], 3))
        self.V = np.zeros((X.shape[0], 1))
        self.Vdot = np.zeros((X.shape[0], 1))
        for i, eta in enumerate(Eta):
            # Vdot = c'*u, where u is a unit vector
            c = eta * self.W * G[i]
            try:
                u = - c.T / npl.norm(c)
            except RuntimeWarning:
                u = np.zeros(c.T.shape)

            self.u[i] = u.T
            self.V[i] = eta.dot(self.W).dot(eta.T)
            self.Vdot[i] = eta @ self.W @ (Etadot[i:i+1, 0:].T + self.a_t *
                                           G[i] @ u)
            U[i] = (self.a_t * np.dot(G[i], u)).T

        self.Xdot = U
        return U

        def __repr__(self):
            """Printable represenation of the object."""
            return 'LyapunovElementSteering({}, {}, {}, {}, {})'.format(
                self.mu, self.W, self.a_t, self.Xref, self.glpe)

        def __str__(self):
            """Human readable represenation of the object."""
            output = 'LyapunovElementSteering'
            output += '(mu={}, W={}, a_t={}, Xref={}, glpe={})'.format(
                self.mu, self.W, self.a_t, self.Xref, self.glpe)
            return output
