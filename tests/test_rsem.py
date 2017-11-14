"""
A Python test module for the rsem module.
"""
import unittest
from ngs.tools.rsem import generate_rsem_command

class TestRsem(unittest.TestCase):
    """
    A simple test class for RSEM
    """
    def test_generate_rsem_command(self):
        """
        Test the generate_rsem_command function.
        """
        rsem = generate_rsem_command( 
            bam="test.bam",
            output_prefix="RSEM/sample",
            rsem_ref="ref/ref_hg38",
            threads=4,
            strand_specific=True,
            program="bin/rsem-calculate-expression")
        expected_command = ' '.join([
            "bin/rsem-calculate-expression",
            "-p 4",
            "--bam",
            "--paired-end test.bam",
            "--strand-specific",
            "ref/ref_hg38",
            "RSEM/sample"
            ])
        self.assertEqual(rsem["command"], expected_command)
