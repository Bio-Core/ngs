"""
A test module for the STAR fusion library.
"""
import unittest
from ngs.tools.star import get_fusions

class TestFusion(unittest.TestCase):
    """
    A simple test class.
    """
    def test_fusion_command(self):
        """
        Test the fusion command.
        """
        gtf_file = '/'.join([
            '/cluster/projects/carlsgroup/workinprogress/abdel',
            '20170418_INSPIRE_RNA/gencode.v26.annotation.gtf'
            ])
        fusions = get_fusions(
            junction='STAR/LTS-035_T_RNA_GCCAAT_L007Chimeric.out.junction',
            prefix='STAR_fusion/LTS-035_T_RNA_GCCAAT_L007',
            out_sam='STAR/LTS-035_T_RNA_GCCAAT_L007Chimeric.out.sam',
            gtf=gtf_file)
        expected_command = " ".join([
            'STAR-Fusion',
            '--chimeric_junction STAR/LTS-035_T_RNA_GCCAAT_L007Chimeric.out.junction',
            '--chimeric_out_sam STAR/LTS-035_T_RNA_GCCAAT_L007Chimeric.out.sam',
            '--ref_GTF', gtf_file,
            '--out_prefix STAR_fusion/LTS-035_T_RNA_GCCAAT_L007'])
        self.assertEqual(fusions['command'], expected_command)
