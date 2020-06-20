# -*- coding: utf-8 -*-

import os
import ffmpeg

from erb import config
from erb.logger import Logger


def revert_video(file, internal_media_id):
    try:
        final_file = "{}_reversed.mp4".format(internal_media_id)

        _input = ffmpeg.input(file)
        audio = _input.audio.filter('areverse')
        video = _input.video.filter('reverse')
        out = ffmpeg.output(audio, video, os.path.join(config.config['paths']['download_path'], final_file))
        ffmpeg.run(out, quiet=bool(config.config['logging']['log_level'] != 'debug'))

    except WindowsError:
        Logger.error("\tFFMPEG not found! Check your installation and $PATH")
        raise FileNotFoundError
    except ffmpeg.Error as e:
        Logger.error("\tError reverting video using FFMPEG!")
        Logger.debug(str(e))
        raise ChildProcessError


