#!/usr/bin/env python
# coding: utf-8

import datetime
import logging


class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.delta = duration.strftime("%H:%M:%S")
        return super().format(record)


def get_logger():
    # add custom formatter to root logger
    handler = logging.StreamHandler()
    LOGFORMAT = '+%(delta)s - %(asctime)s - %(levelname)-9s: %(message)s'
    fmt = DeltaTimeFormatter(LOGFORMAT)
    handler.setFormatter(fmt)
    logging.getLogger().addHandler(handler)
    return logging.getLogger()


def to_list(textdata):
    return "".join(textdata.lower().split()).split(',')