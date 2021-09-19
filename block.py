from qc import QC
from agg_qc import AggQC
from dataclasses import dataclass


@dataclass
class Block:
    """Class for keeping track of a Block in the chain"""
    type: str
    agg_qc: AggQC
    qc: QC
    cmd: str
