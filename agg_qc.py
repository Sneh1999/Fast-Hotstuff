from dataclasses import dataclass
from typing import List
from qc import QC


@dataclass
class AggQC:
    """Class for keeping track of an aggregated quorum certificate"""
    qc_set: List[QC]
    sig: str

    def as_dict(self):
        return {
            "sig": self.sig,
            "qc_set": [qc.as_dict() for qc in self.qc_set]
        }
