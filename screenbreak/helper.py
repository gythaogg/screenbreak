import os


def notify(message):
    os.system('notify-send "{}"'.format(message))
    return
