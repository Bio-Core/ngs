"""
A module for handling sequence alignment using BWA.
"""

class Bwa(object):
    """
    NAME
        Bwa -- A Python class wrapper for the Burrows-Wheeler Aligner
    SYNOPSIS
        object = Bwa()
    DESCRIPTION
        A class for handling alignment tasks using BWA.
    """

    def __init__(
        self,
        bwa="bwa",
        index="ref.fa",
        fastq1="",
        fastq2="",
        prefix="out"):
        """
        object constructor
        """
        self.bwa = bwa
        self.index = index
        self.fastq1 = fastq1
        self.fastq2 = fastq2
        self.prefix = prefix
        return None

    def mem(self):
        """
        Method wrapper for the bwa mem program.
        USAGE:
            object.mem(
                bwa,
                index,
                fastq1,
                fastq2,
                prefix)
        """
        cmd = " ".join([
            self.bwa,
            self.index,
            self.fastq1,
            self.fastq2
            ])
        return {"command": cmd}

    def index(self):
        """
        Index the reference FASTA file for use with BWA.
        USAGE:
            object.index(
                bwa,
                index,
                fasta)
        """
        cmd = " ".join([
            self.bwa,
            ])
        return {"command": cmd}

    def create_read_group(self):
        """
        Create the read group string (in accordance to the SAM specification)
        for use with BWA.
        USAGE:
            object.create_read_group(

            )
        """
        cmd = '@RG\tread_group_string'
        return {"command": cmd}
