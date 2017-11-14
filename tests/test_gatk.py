"""
A test module for the ngs.gatk package.
"""
import unittest
import ngs.tools.gatk as ngs

class TestGatkMethods(unittest.TestCase):
    """
    Test class used to test the Gath package.
    """
    def test_split_n_cigar_reads(self, bams=None, output="split.bam"):
        """
        Test the split_n_cigar_reads function to ensure command remains consistent
        with expected.
        """
        if bams is None:
            bams = ["input.bam"]
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")
        self.assertTrue(hasattr(gatk, "split_n_cigar_reads"),
                        "split_n_cigar_reads() not found in gatk")
        split_run = gatk.split_n_cigar_reads(bams=bams, output=output)
        expected_split_command = " ".join([
            "/usr/bin/java -Xmx20g -Djava.io.tmpdir=./tmp",
            "-jar GenomeAnalysisTK.jar",
            "-T SplitNCigarReads",
            "-I input.bam",
            "-R ref.fa",
            "-o PROCESSED_BAMS/split.bam",
            "-rf ReassignOneMappingQuality",
            "-rf UnmappedRead",
            "--reassign_mapping_quality_from 255",
            "--reassign_mapping_quality_to 60",
            "-U ALLOW_N_CIGAR_READS"
            ])
        self.assertEqual(
            split_run["command"],
            expected_split_command,
            "command does not match expected")

    def test_realign_target_creator(self, bams=None, output="realign"):
        """
        Test the realign_target_creator method to determine whether the output
        command matches the expected command.
        """
        if bams is None:
            bams = ["input.bam"]
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")
        self.assertTrue(
            hasattr(gatk, "realigner_target_creator"),
            "realigner_target_creator() not found in gatk")
        realign_run = gatk.realigner_target_creator(bams=bams, output=output)
        expected_realigner_command = " ".join([
            "/usr/bin/java -Xmx20g -Djava.io.tmpdir=./tmp",
            "-jar GenomeAnalysisTK.jar",
            "-T RealignerTargetCreator",
            "-I input.bam",
            "-o PROCESSED_BAMS/realign",
            "-R ref.fa",
            "-nt 8",
            "-l INFO"
            ])
        self.assertEqual(
            realign_run["command"],
            expected_realigner_command)

    def test_indel_realigner(self, bams=None, output="realign.bam", intervals="realign"):
        """
        Test the indel_realigner method to determine whether the output
        command matches the expected command.
        """
        if bams is None:
            bams = ["input.bam"]
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")
        self.assertTrue(
            hasattr(gatk, "indel_realigner"),
            "indel_realigner() not found in gatk")
        indel_realign_run = gatk.indel_realigner(bams=bams, output=output, intervals=intervals)
        expected_realign_run_command = " ".join([
            "/usr/bin/java -Xmx20g -Djava.io.tmpdir=./tmp",
            "-jar GenomeAnalysisTK.jar",
            "-T IndelRealigner",
            "-I input.bam",
            "-o PROCESSED_BAMS/realign.bam",
            "-targetIntervals realign",
            "-R ref.fa"
            ])
        self.assertEqual(
            indel_realign_run["command"],
            expected_realign_run_command,
            "command does not match expected indel realignment")

    def test_base_quality_recalibration(self,
                                        bams=None,
                                        output="basequalrecal.table"):
        """
        Test the base_quality_recalibration method to see if command matches
        expected.
        """
        if bams is None:
            bams = ["indel_realign.bam"]
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")
        self.assertTrue(
            hasattr(gatk, "base_quality_recalibration"),
            "base_quality_recalibration() not found in gatk")
        base_qual_recal_run = gatk.base_quality_recalibration(bams=bams, output=output)
        baserecal_command = " ".join([
            "/usr/bin/java -Xmx20g -Djava.io.tmpdir=./tmp",
            "-jar GenomeAnalysisTK.jar",
            "-T BaseRecalibrator",
            "-I indel_realign.bam",
            "-o PROCESSED_BAMS/basequalrecal.table",
            "-R ref.fa",
            "-U ALLOW_N_CIGAR_READS"
            ])
        self.assertEqual(
            base_qual_recal_run["command"],
            baserecal_command,
            "command does not match expected")

    def test_print_reads(self, bam="realign.bam", output="recal.bam", recaldata="recal.table"):
        """
        Test whether the print_reads method provides the expected output.
        """
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")

        # check to see if command exists for object
        self.assertTrue(
            hasattr(gatk, "print_reads"),
            msg="print_reads() not found in gatk")

        printreads_run = gatk.print_reads(
            bam=bam,
            output=output,
            recaldata=recaldata
            )
        expected_printreads_command = " ".join([
            "/usr/bin/java -Xmx20g -Djava.io.tmpdir=./tmp",
            "-jar GenomeAnalysisTK.jar",
            "-T PrintReads",
            "-I realign.bam",
            "-o PROCESSED_BAMS/recal.bam",
            "-R ref.fa",
            "-BQSR recal.table",
            "-nct 4",
            "-rf BadCigar"
            ])
        self.assertEqual(
            printreads_run["command"],
            expected_printreads_command,
            "PrintReads command does not match expected")

    def test_depthofcoverage(self, bam="input.bam", output="depth.txt"):
        """
        Test the depth_of_coverage command outputs the same as expected.
        """
        gatk = ngs.Gatk(output_dir="PROCESSED_BAMS")
        self.assertTrue(
            hasattr(gatk, "depth_of_coverage"),
            "depth_of_coverage() not found in gatk package")
        depth_run = gatk.depth_of_coverage(
            bam=bam,
            output=output,
            )
        print(depth_run)


if __name__ == '__main__':
    unittest.main()
