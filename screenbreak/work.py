import argparse
import logging
import os
import time

from .helper import notify
from .state import QuitNow, TimedState


class Work(TimedState):
    def __init__(self, interval_mins=25, message='Work away!'):
        super().__init__(interval_mins, message, 'break')
        return


class Relax(TimedState):
    def __init__(self, interval_mins=5, message='Take a break!'):
        super().__init__(interval_mins, message, 'back to work!')
        return


class ScreenBreak(Relax):
    def __init__(self, interval_mins=5, message=''):
        super().__init__(interval_mins, message)
        return

    def run(self):
        os.system('xset dpms force off')
        super().run()
        os.system('xset dpms force on')
        return


def main():
    parser = argparse.ArgumentParser(description='Screenbreak.')
    parser.add_argument(
        '--work', '-w', help='work interval in minutes', type=int, default=55)
    parser.add_argument(
        '--break-interval',
        '-b',
        help='break interval in minutes',
        type=int,
        default=5)
    parser.add_argument(
        '--turnoff',
        action='store_true',
        default=False,
        help='turn off screen during break')

    args = parser.parse_args()
    try:
        work_interval = args.work
        next_interval = None
        relax_interval = args.break_interval
        while True:
            Work(interval_mins=work_interval).run()
            logging.info('Returned from work')
            if args.turnoff:
                ScreenBreak(interval_mins=relax_interval).run()
            else:
                Relax(interval_mins=relax_interval).run()

            logging.info('Returned from break')
    except QuitNow:
        return

    return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
    main()
