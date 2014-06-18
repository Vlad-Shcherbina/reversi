from __future__ import division
import random
import math


class GaussianConjugatePrior(object):
    def __init__(self):
        self.alpha = 0.0
        self.beta = 0.0
        self.n0 = 0.0
        self.mu0 = 0.0

    @staticmethod
    def strong_prior(mu, sigma, strength=0.1):
        # Roughly corresponds to observing `strength` samples drawn
        # from N(mu, sigma).
        assert strength > 0
        gcp = GaussianConjugatePrior()
        gcp.alpha = 0.5 * strength
        gcp.beta = 0.5 * strength * sigma**2
        gcp.mu0 = float(mu)
        gcp.n0 = float(strength)
        return gcp

    def draw_parameters(self, prng=random):
        assert self.n0 > 0 and self.beta > 0, \
            "can't draw from improper distribution (strong prior can help)"
        precision = prng.gammavariate(self.alpha, 1 / self.beta)
        sigma = 1.0 / math.sqrt(precision)
        mu = prng.normalvariate(self.mu0, sigma / math.sqrt(self.n0))
        return mu, sigma

    def draw_sample(self, prng=random):
        return prng.normalvariate(*self.draw_parameters(prng=prng))

    def update(self, *xs):
        # see http://www.cs.berkeley.edu/~jordan/courses/260-spring10/lectures/lecture5.pdf
        xs = list(xs)
        if not xs:
            return
        n = len(xs)
        self.alpha += 0.5 * n
        mean = sum(xs) / n
        self.beta += 0.5 * sum((x - mean)**2 for x in xs)
        self.beta += 0.5 * self.n0 * n / (self.n0 + n) * (mean - self.mu0)**2

        self.mu0 = (self.n0 * self.mu0 + mean * n) / (self.n0 + n)
        self.n0 += n


if __name__ == '__main__':
    gcp = GaussianConjugatePrior.strong_prior(40, 5, strength=0.001)

    xs = [random.normalvariate(42, 3) for _ in range(10)]
    for x in xs:
        gcp.update(x)

    print gcp.alpha, gcp.beta

    for i in range(10):
        print gcp.draw_parameters(), gcp.draw_sample()
