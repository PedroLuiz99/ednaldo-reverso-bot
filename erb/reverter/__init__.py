# -*- coding: utf-8 -*-

import os
import ffmpeg

from PIL import Image, ImageOps

from erb import config
from erb.logger import Logger


def revert_video(file, internal_media_id):
    Logger.info("Reverting video...")
    try:
        final_file_name = "{}_reversed.mp4".format(internal_media_id)
        final_file = os.path.join(config.config['paths']['download_path'], final_file_name)

        _input = ffmpeg.input(file)
        audio = _input.audio.filter('areverse')
        video = _input.video.filter('reverse')
        out = ffmpeg.output(audio, video, final_file)
        ffmpeg.run(out, quiet=bool(config.config['logging']['log_level'] != 'debug'))

        Logger.debug("Saved to: {}".format(final_file))
        return final_file
    except WindowsError:
        Logger.error("\tFFMPEG not found! Check your installation and $PATH")
        raise FileNotFoundError
    except ffmpeg.Error as e:
        Logger.error("\tError reverting video!")
        Logger.debug(str(e))
        raise ChildProcessError


def revert_photo(file, internal_media_id):
    Logger.info("Mirroring photo...")
    try:
        final_file_name = "{}_reversed.png".format(internal_media_id)
        final_file = os.path.join(config.config['paths']['download_path'], final_file_name)

        img = Image.open(file)
        mirror = ImageOps.mirror(img)
        mirror.save(final_file)

        Logger.debug("Saved to: {}".format(file))

        return final_file
    except Exception as e:
        Logger.error("\tError processing image!")
        Logger.debug(str(e))
        raise
