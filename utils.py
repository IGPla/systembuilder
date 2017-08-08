# -*- coding: utf-8 -*-
"""
Utils module
"""
import os

def get_base_dir(_file):
    """
    Return base dir
    """
    return os.path.abspath(os.path.dirname(_file))
