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
    # TODO:
    # Integer for block sequence - 64 int
    # Integer for View number maps to Primary ID

    def as_dict(self):
        return {
            "type": self.type,
            "agg_qc": self.agg_qc.as_dict(),
            "qc": self.qc.as_dict(),
            "cmd": self.cmd
        }
