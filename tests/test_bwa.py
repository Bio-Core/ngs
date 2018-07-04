"""
A test module for the ngs.tools.bwa module
"""

import unittest
import ngs.tools.bwa

class TestBwaMethods(unittest.TestCase):
    """
    Test class used to test the Bwa package.
    """
    def test_bwa_mem(self, bams=None, output="split.bam"):
        """
        Test the bwa mem subprogram
        """
        if bams is None:
            bams = ["input.bam"]
        bwa = ngs.tools.bwa.Bwa()
        self.assertTrue(hasattr(bwa, "mem"),
                        "mem() not found in bwa")
        mem_run = bwa.mem()
        expected_mem_command = " ".join([
            "bwa mem",
            "-M -t4",
            "-R '@RG\tID:1\tSM:TM01-1\tPL:Illumina\tPU:AATGTTGC.L001\tLB:aliciapreposttreat'",
            "/mnt/work1/data/genomes/human/hg19/iGenomes/Sequence/BWAIndex/genome.fa",
            "./fastq/Sample_TM01-1/TM01-1_AATGTTGC_L001_R1.fastq.gz",
            "./fastq/Sample_TM01-1/TM01-1_AATGTTGC_L001_R2.fastq.gz >",
    "./result/bwa_out/TM01-1.sam"])
        self.assertEqual(
            mem_run["command"],
            expected_mem_command,
            "command does not match expected")
        # print(bwa.mem())

    def test_create_read_group(self):
        """
        Test the construction of the creat_read_group method for creating the
        SAM specification read group string used in BWA.
        """
        pass