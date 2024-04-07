from enum import Enum

class Status_Enum(str, Enum):
    created = 'created'
    approved = 'approved'
    closed = 'closed'