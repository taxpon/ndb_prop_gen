import unittest
from ndb_prop_gen.arg import Arg


sample_property = """\
    @property
    def sample_name(self):
        return self._sample_name
"""


class TestArg(unittest.TestCase):

    def setUp(self):
        self.sample = Arg("sample_name", "Float", 0.0)
        pass

    def tearDown(self):
        pass

    def test_class_arg(self):
        self.assertEqual(self.sample.class_arg, "sample_name=0.0")

    def test_class_init(self):
        self.assertEqual(self.sample.class_init, "self._sample_name = sample_name")

    def test_class_property(self):
        self.assertEqual(self.sample.class_property, sample_property)

    def test_model_init(self):
        self.assertEqual(self.sample.model_init, "sample_name = ndb.FloatProperty(default=0.0)")

if __name__ == "__main__":
    unittest.main()