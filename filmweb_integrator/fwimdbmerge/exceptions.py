#!/usr/bin/env python
# coding: utf-8


class Error(Exception):
    """Base class for other exceptions"""
    pass


class MalformedDataError(Error):
    """Raised when the input value is too small"""
    pass


class DataProcessingError(Error):
    """Raised when the input value is too large"""
    pass