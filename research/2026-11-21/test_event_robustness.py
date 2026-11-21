import unittest
import numpy as np
from event_robustness import event_depth_heterogeneity,time_averaging_beta

class RobustnessTests(unittest.TestCase):
    def test_equal_depths(self):
        mu,se,q,qr=event_depth_heterogeneity([.02]*4,[.001]*4)
        self.assertAlmostEqual(mu,.02)
        self.assertAlmostEqual(se,.0005)
        self.assertAlmostEqual(q,0)
    def test_heterogeneity(self):
        self.assertGreater(event_depth_heterogeneity([.02,.03,.01],[.001]*3)[2],100)
    def test_beta_unit(self):
        r=np.random.default_rng(5).normal(size=12000)
        b=time_averaging_beta(r,[1,2,5,10])
        self.assertAlmostEqual(b[0],np.sqrt((len(r)-1)/len(r)),places=5)
        self.assertTrue(np.all(np.abs(b[1:]-1)<.2))
    def test_bad_bins(self):
        with self.assertRaises(ValueError):
            time_averaging_beta(np.arange(10.),[5])
if __name__=="__main__": unittest.main()
