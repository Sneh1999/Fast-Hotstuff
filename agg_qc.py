from dataclasses import dataclass
from qc import QC


@dataclass
class AggQC:
    """Class for keeping track of an aggregated quorum certificate"""
    qc_set: list[QC]
    sig: str
