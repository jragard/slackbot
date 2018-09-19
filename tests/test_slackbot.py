import sys
import unittest
sys.path.append('..')
from starterbot import handle_command


class TestStarterbot(unittest.TestCase):

    def test_handle_help_command(self):
        self.assertEqual(handle_command('help', 'CCD7USCR0'), """Here is a list of commands:
        exit - Shut me down
        ping - Check my uptime
        help - Display a list of commands for me
        do - Tell me to do something
        bitcoin - Ask me the bitcoin price""")

    def test_handle_do_command(self):
        # global start_time
        self.assertEqual(handle_command('do something',
                         'CCD7USCR0'), 'something something something')

    def test_handle_exit_command(self):
        self.assertEqual(handle_command('exit', 'CCD7USCR0'),
                         'See ya later!')


if __name__ == '__main__':
    unittest.main()
