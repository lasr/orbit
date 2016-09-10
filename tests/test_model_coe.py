"""Created on Wed Sep 07 2016 12:09.

@author: Nathan Budd
"""
import unittest
import numpy as np
import numpy.matlib as npm
import matplotlib.pyplot as plt
from ..model_coe import ModelCOE
from ..perturb_zero import PerturbZero
from ...mcpi.mcpi import MCPI
from ...mcpi.mcpi_approx import MCPIapprox
from ...orbital_mech.element_sets.orb_coe import OrbCOE


class TestModelCOE(unittest.TestCase):
    """Test class for ModelCOE."""

    def setUp(self):
        """."""
        mu = 1.
        self.mcoe = ModelCOE(mu)

    def test_instantiation(self):
        """."""
        self.assertIsInstance(self.mcoe, ModelCOE)

    def test_getattr(self):
        """."""
        self.assertEqual(self.mcoe.mu, 1)

    def test_setattr(self):
        """."""
        self.mcoe.mu = 2.
        self.assertEqual(self.mcoe.mu, 2)

    def test_dynamics(self):
        x = np.matrix([[2., .5, 1., .1, .1, 0.],
                       [4., .5, 1., .1, .1, 0.],
                       [8., .5, 1., .1, .1, 0.]])
        t = np.matrix([[0.], [1.], [2.]])

        xdot = self.mcoe(t, x)
        print(self.mcoe.Xdot)
        self.assertEqual(xdot.shape, (3, 6))

    def test_dynamics_integration(self):
        def X_guess_func(t):
            return npm.ones((len(t), 6)) * .1

        domains = (0., 6.)
        N = 20,
        X0 = [2., .1, .1, 0., 0., 0.]
        tol = 1e-10

        mcpi = MCPI(self.mcoe, domains, N, X_guess_func, X0, tol)
        X_approx = mcpi.solve_serial()
        print(mcpi.iterations)

        T_step = 0.1
        T = np.arange(domains[0], domains[1]+T_step, T_step).tolist()
        x_approx = X_approx(T)
        plt_p, = plt.plot(T, [row[0] for row in x_approx], label='p')
        plt_e, = plt.plot(T, [row[1] for row in x_approx], label='e')
        plt_i, = plt.plot(T, [row[2] for row in x_approx], label='i')
        plt_W, = plt.plot(T, [row[3] for row in x_approx], label='W')
        plt_w, = plt.plot(T, [row[4] for row in x_approx], label='w')
        plt_f, = plt.plot(T, [row[5] for row in x_approx], label='f')
        plt.legend(handles=[plt_p, plt_e, plt_i, plt_W, plt_w, plt_f])
        plt.show()
        self.assertIsInstance(X_approx, MCPIapprox)

    def test_reference(self):
        T_step = 0.1
        domains = (0., 1.)
        T = np.arange(domains[0], domains[1]+T_step, T_step).tolist()
        X0 = np.matrix([2., .1, .1, 0., 0., 0.])
        X = self.mcoe.reference(np.matrix(T).T, X0).tolist()

        plt_p, = plt.plot(T, [row[0] for row in X], label='p')
        plt_e, = plt.plot(T, [row[1] for row in X], label='e')
        plt_i, = plt.plot(T, [row[2] for row in X], label='i')
        plt_W, = plt.plot(T, [row[3] for row in X], label='W')
        plt_w, = plt.plot(T, [row[4] for row in X], label='w')
        plt_f, = plt.plot(T, [row[5] for row in X], label='f')
        plt.legend(handles=[plt_p, plt_e, plt_i, plt_W, plt_w, plt_f])
        plt.show()
        self.assertEqual(X[-1][0], X0[0,0])
