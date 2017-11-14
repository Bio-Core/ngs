"""
A Python test module for align_rnaseq.
"""
import unittest
from ngs.tools.star import align_rnaseq

class TestAlign(unittest.TestCase):
    """
    A simple test class for STAR.
    """
    def test_align_command(self):
        """
        Test the alignment command.
        """
        genome_dir = "/".join([
            '/cluster/projects/carlsgroup/workinprogress',
            'abdel/20170418_INSPIRE_RNA',
            'STARIndex_hg38_gencode_genomeSAsparseD2',
            ])
        command = align_rnaseq(
            read1='./FCRL4_neg_Day_0_CGGCTATG-TAAGATTA_R1.fastq.gz',
            read2='./FCRL4_neg_Day_0_CGGCTATG-TAAGATTA_R2.fastq.gz',
            prefix='STAR/FCRL4_neg_Day_0_CGGCTATG-TAAGATTA',
            genome_dir=genome_dir)
        fastq_files = " ".join([
            './FCRL4_neg_Day_0_CGGCTATG-TAAGATTA_R1.fastq.gz',
            './FCRL4_neg_Day_0_CGGCTATG-TAAGATTA_R2.fastq.gz'])
        expected_command = " ".join([
            'STAR',
            '--runMode alignReads',
            '--readFilesIn', fastq_files,
            " ".join([
                '--outFileNamePrefix',
                'STAR/FCRL4_neg_Day_0_CGGCTATG-TAAGATTA']),
            '--genomeDir', genome_dir,
            '--runThreadN 4',
            '--chimSegmentMin 20',
            '--readFilesCommand zcat',
            '--twopassMode Basic',
            '--outSAMprimaryFlag AllBestScore',
            '--outFilterIntronMotifs RemoveNoncanonical',
            '--outSAMtype BAM SortedByCoordinate',
            '--quantMode TranscriptomeSAM GeneCounts',
            '--outSAMunmapped Within',
            '--genomeSAsparseD 2',
            '--limitBAMsortRAM 35000000000'])
        self.assertEqual(command, expected_command)
