# -*- coding: utf-8 -*-

# noqa - Proudly chupinhed from https://gist.github.com/techtonik/2151727

import inspect
import sys


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    def stack_(frame):
        frame_list = []
        while frame:
            frame_list.append(frame)
            frame = frame.f_back
        return frame_list

    stack = stack_(sys._getframe(1)) # noqa 'protected attribute'
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parent_frame = stack[start]

    name = []
    module = inspect.getmodule(parent_frame)
    # `modname` can be None when frame is executed directly in console
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parent_frame.f_locals:
        name.append(parent_frame.f_locals['self'].__class__.__name__)
    codename = parent_frame.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parent_frame
    return ".".join(name)
