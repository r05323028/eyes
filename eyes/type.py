'''Eyes types module
'''
import enum


class Label(enum.Enum):
    '''Entity label
    '''
    PERSON = enum.auto()


class SourceType(enum.Enum):
    '''Source types enum
    '''
    PTT = enum.auto()
    DCARD = enum.auto()
