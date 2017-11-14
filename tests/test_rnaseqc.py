"""
A Python test module for generate_rnaseqc_command().
"""
import unittest
from ngs.tools.rnaseqc import generate_rnaseqc_command

class TestAlign(unittest.TestCase):
    """
    A simple test class for RNASeQC.
    """
    def test_rnaseqc_command(self):
        """
        Test the RNASeQC command.
        """
        reference = '/'.join([
            '/cluster/tools/data/genomes/human/hg38',
            'iGenomes/Sequence/WholeGenomeFasta/genome.fa'])
        gtf_file = '/'.join([
            '/cluster/projects/carlsgroup/workinprogress/abdel',
            '20170418_INSPIRE_RNA/rnaseqc_gencode.v26.annotation.gtf'])
        run = generate_rnaseqc_command(
            output="RNASeQC/LTS-035_T_RNA_GCCAAT_L007",
            gtf=gtf_file,
            reference=reference,
            sample_list="RNASeQC/LTS-035_T_RNA_GCCAAT_L007.sampleFile.list",
            java="java",
            rnaseqc='$rnaseqc_dir/RNA-SeQC.jar',
            tmpdir='RNASeQC/tmp7JESc1Ll',
            bwa='bwa',
            single_end='NO',
            memory='8')
        expected_program = " ".join([
            'java -Xmx8g',
            '-Djava.io.tmpdir=RNASeQC/tmp7JESc1Ll',
            '-jar $rnaseqc_dir/RNA-SeQC.jar'])
        expected_options = " ".join([
            '-bwa bwa',
            '-o RNASeQC/LTS-035_T_RNA_GCCAAT_L007',
            '-t /cluster/projects/carlsgroup/workinprogress/abdel/20170418_INSPIRE_RNA/rnaseqc_gencode.v26.annotation.gtf',
            '-r /cluster/tools/data/genomes/human/hg38/iGenomes/Sequence/WholeGenomeFasta/genome.fa',
            '-singleEnd NO',
            '-s RNASeQC/LTS-035_T_RNA_GCCAAT_L007.sampleFile.list'
            ])
        expected_command = " ".join([expected_program, expected_options])
        self.assertEqual(run["command"], expected_command)
