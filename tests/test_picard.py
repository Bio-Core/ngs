"""
Test package for the Picard suite of tools.
"""
import unittest
import ngs.tools.picard

class TestPicard(unittest.TestCase):
    """
    Test class
    """
    def test_addorreplacereadgroups(self):
        """
        A method for testing the generate_addorreplacereadgroups_command function.
        """
        picard = ngs.tools.picard.Picard(
            java="java",
            picard="picard.jar",
            tmpdir="./tmp")

        picard_run = picard.generate_addorreplacereadgroups_command(
            input="input.bam",
            output="output.bam",
            unique_id="unique_id",
            sample="sample1",
            library="library1",
            unit="PLATFORM_UNIT",
            center="pmgc.uhn.ca")
        expected_command = ' '.join([
            "java",
            "-Xmx20g",
            "-Djava.io.tmpdir=./tmp",
            "-jar picard.jar",
            "AddOrReplaceReadGroups",
            "INPUT=input.bam",
            "OUTPUT=output.bam",
            "SORT_ORDER=coordinate",
            "RGID=unique_id",
            "RGLB=library1",
            "RGPL=ILLUMINA",
            "RGPU=PLATFORM_UNIT",
            "RGSM=sample1"])
        self.assertEqual(picard_run["command"], expected_command)

    def test_markduplicates(self):
        """
        A method for testing the generate_markduplicates_command function.
        """
        picard = ngs.tools.picard.Picard(
            java="java",
            picard="picard.jar",
            tmpdir="./tmp")
        picard_run = picard.generate_markduplicates_command(
            input="input.bam",
            output="output.bam",
            metrics="PROCESSED_BAMS/sample.dedup",
            create_index=True,
            max_records=150000)
        expected_command = ' '.join([
            'java',
            '-Xmx20g',
            '-Djava.io.tmpdir=./tmp',
            '-jar picard.jar',
            'MarkDuplicates',
            'INPUT=input.bam',
            'OUTPUT=output.bam',
            'METRICS_FILE=PROCESSED_BAMS/sample.dedup',
            'CREATE_INDEX=TRUE',
            'MAX_RECORDS_IN_RAM=150000',
            'VALIDATION_STRINGENCY=SILENT'])
        self.assertEqual(picard_run["command"], expected_command)
