def hello_world():
    # This functions returns a message
    return "Hello, World!"


import unittest

class HelloWorldTest(unittest.TestCase):
    def test_check_hello_world_returns_correct_msg(self):
        msg = "Test if hello world is returned"
        self.assertEqual(hello_world(), "Hello, World!", msg=msg)

if __name__ == '__main__':
    unittest.main()