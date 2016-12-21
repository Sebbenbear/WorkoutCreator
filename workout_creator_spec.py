import unittest

from workout_creator import Activity
from workout_creator import MovingActivity

class TestMovingActivities(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_moving_activity(self):
        activity = MovingActivity("running")
        activity.set_distance(2)
        self.assertEqual(activity.name, "running")
        self.assertEqual(activity.distance, 2)

if __name__ == '__main__':
    unittest.main()

# class ActualTests(unittest.TestCase):
