import unittest
from hello_world import hello_world

class HelloWorldTest(unittest.TestCase):
    def test_hello(self):
        msg = "Test if hello world is returned"
        self.assertEqual(hello_world(), "Hello, World!", msg=msg)

if __name__ == '__main__':
    unittest.main()