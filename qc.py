from dataclasses import dataclass


@dataclass
class QC:
    """Class for keeping track of a quorum certificate"""
    type: str
    view_number: int
    block_hash: str
    sig: str
