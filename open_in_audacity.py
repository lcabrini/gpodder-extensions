import logging
import shutil
import os
import subprocess
import gpodder
from gpodder import util

logger = logging.getLogger(__name__)
_ = gpodder.gettext
__title__ = _('Open With Audacity')
__description__ = _('Adds a context menu to open episode with Audacity')
__authors__ = 'Lorenzo Cabrini <lorenzo.cabrini@gmail.com>'
__category__ = 'post-download'

class gPodderExtension:
    def __init__(self, container):
        self.container = container
        if shutil.which('audacity') is None:
            raise Exception("Audacity not found")

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def on_ui_object_available(self, name, ui_object):
        if name == 'gpodder-gtk':
            self.gpodder = ui_object

    def on_episodes_context_menu(self, episodes):
        if len(episodes) != 1:
            return None
        episode = episodes[0]
        if not episode.was_downloaded():
            return None
        return [('Open in Audacity', self.on_open_in_audacity)]

    def on_open_in_audacity(self, episodes):
        episode = episodes[0]
        filename = episode.local_filename(create=False)
        pid = os.fork()
        if pid == 0:
            os.system("audacity '{}'".format(filename))
            exit()
