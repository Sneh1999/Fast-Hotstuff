from dataclasses import dataclass


@dataclass
class QC:
    """Class for keeping track of a quorum certificate"""
    type: str
    view_number: int
    block_hash: str
    sig: str

    def as_dict(self):
        return {
            "type": self.type,
            "view_number": self.view_number,
            "block_hash": self.block_hash,
            "sig": self.sig
        }


# view number + index + block hash - byte array and then sign it - vote for a block
# every node generates a vote - only difference is index
# qc will contain array of indexes
#
