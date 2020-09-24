import logging
import os
import select
import sys
import time
from datetime import datetime, timedelta

from tqdm import tqdm


def notify(message):
    if message:
        os.system('notify-send "{}"'.format(message))
    return


class QuitNow(Exception):
    pass


class State:
    def __init__(self):
        return

    def __str__(self):
        return self.__class__.__name__


class TimedState(State):
    def __init__(self, interval_mins, message='', next_state=''):
        super().__init__()
        self.interval = interval_mins * 60
        self.message = message
        self.next_state = next_state
        return

    def run(self):
        logging.info('%s for %3.1f minutes', self, self.interval / 60)
        self.start_time = datetime.now()
        if self.message: notify(self.message)
        JUMP_SECONDS = 60
        for i in tqdm(range(0, self.interval, JUMP_SECONDS)):
            try:
                time.sleep(JUMP_SECONDS)
            except KeyboardInterrupt:
                self.elapsed_time = datetime.now() - self.start_time
                self.await_input()
                return
            except EOFError:
                pass

        return

    def resume(self):
        logging.info('Continue %sing', self)
        self.interval = self.interval - self.elapsed_time.seconds
        self.run()
        return

    def abort(self):
        raise QuitNow()

    def await_input(self):
        logging.info('Interrupted after %2.2f minutes',
                     self.elapsed_time.seconds / 60)
        response_continue = ''
        try:
            while not response_continue:
                print("Continue {}ing (c) | {} (b) | Quit (q) ".format(
                    self, self.next_state))
                i, o, e = select.select([sys.stdin], [], [], 20)

                response_continue = sys.stdin.readline().strip() if i else ''
                if response_continue.startswith('b'):
                    return
                elif response_continue.startswith('q'):
                    self.abort()
                elif response_continue.startswith('c'):
                    self.resume()
                else:
                    response_continue = ''
                    self.resume()
        except KeyboardInterrupt:
            self.abort()

        return
