import unittest
import random
import copy
from nose.tools import assert_almost_equal

import bayes


class GaussianConjugatePriorTest(unittest.TestCase):
    def test_update_composability(self):
        gcp1 = bayes.GaussianConjugatePrior()
        gcp2 = bayes.GaussianConjugatePrior()

        xs = [42, 1, 5, 10]
        gcp1.update(*xs)
        for x in xs:
            gcp2.update(x)

        assert_almost_equal(gcp1.alpha, gcp2.alpha)
        assert_almost_equal(gcp1.beta, gcp2.beta)
        assert_almost_equal(gcp1.mu0, gcp2.mu0)
        assert_almost_equal(gcp1.n0, gcp2.n0)

    def test_convergence(self):
        prng = random.Random(42)

        gcp = bayes.GaussianConjugatePrior()
        for _ in range(10000):
            gcp.update(prng.normalvariate(42, 3))

        eps = 0.1
        for _ in range(10):
            mu, sigma = gcp.draw_parameters(prng)
            assert 42 - eps < mu < 42 + eps, mu
            assert 3 - eps < sigma < 3 + eps, sigma

    def test_strong_prior(self):
        gcp = bayes.GaussianConjugatePrior.strong_prior(42, 3, 10000)

        prng = random.Random(42)
        eps = 0.1
        for _ in range(10):
            mu, sigma = gcp.draw_parameters(prng)
            assert 42 - eps < mu < 42 + eps, mu
            assert 3 - eps < sigma < 3 + eps, sigma


if __name__ == '__main__':
    unittest.main()
