import unittest as U
import foo as F


class TestHoge(U.TestCase):

    def test_hello(self):
        name = "unittest"
        greeter = F.Foo(name)
        self.assertEqual(greeter.hello(6), "good morning, {}.".format(name))
        self.assertEqual(greeter.hello(13), "good afternoon, {}.".format(name))
        self.assertEqual(greeter.hello(20), "good evening, {}.".format(name))
        self.assertEqual(greeter.hello(24), "hi, {}.".format(name))

    def test_bye(self):
        name = "unittest"
        greeter = F.Foo(name)
        self.assertEqual(greeter.bye(), "bye, {}.".format(name))


if __name__ == '__main__':
    unittest.main()
