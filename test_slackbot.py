import unittest
import sys
import starterbot
sys.path.append('..')


class TestStarterbot(unittest.TestCase):
    def test_handle_ping_command(self):
        self.assertEqual(starterbot.handle_command('help', 'CCD7USCR0'), """Here is a list of commands:
        exit
        ping
        help
        do""")

    def test_handle_do_command(self):
        # global start_time
        self.assertEqual(starterbot.handle_command('do something',
                         'CCD7USCR0'), 'something something something')

    def test_handle_exit_command(self):
        self.assertEqual(starterbot.handle_command('exit', 'CCD7USCR0'),
                         'See ya later!')

    # def test_handle_ping_command(self):
    #     self.assertEqual(starterbot.handle_command('ping', 'CCD7USCR0'),
    #                      "ryanbot is active, uptime = {} seconds".format(
    #                       time.time() - start_time))

    # Why does above function not work?  (Error start_time is undefined).


if __name__ == '__main__':
    unittest.main()
