"""
A test module for the TopHat2 API.
"""
import unittest
from ngs.tools.tophat2 import generate_tophat2_command

class TestTophat2(unittest.TestCase):
    """

    """
    def test_generate_tophat2_command(self):
        """
        Method for testing the generate_tophat2_command function in
        the API.
        """
        tophat2_run = generate_tophat2_command(
            read1="read1.fastq.gz",
            read2="read2.fastq.gz",
            genome_dir="genome_dir",
            gtf="gencode.v26.annotation.gtf",
            output="TOPHAT_fusion/sample",
            fusion_ignore_chromosomes=["M", "MT"],
            threads=4,
            inner_mate_distance=5,
            mate_std_dev=30,
            max_intron_length=200000,
            fusion_min_dist=10000,
            fusion_anchor_length=10,
            tophat2="tophat2"
            )
        expected_command = ' '.join([
            "tophat2",
            "-p 4",
            "--fusion-search",
            "--bowtie1",
            "--no-coverage-search",
            "--keep-fasta-order",
            "-r 5",
            "--mate-std-dev 30",
            "--max-intron-length 200000",
            "--fusion-min-dist 10000",
            "--fusion-anchor-length 10",
            "--fusion-ignore-chromosomes M,MT",
            "-G gencode.v26.annotation.gtf",
            "-o TOPHAT_fusion/sample",
            "genome_dir",
            "read1.fastq.gz",
            "read2.fastq.gz"])
        self.maxDiff = None
        self.assertEqual(tophat2_run["command"], expected_command)
