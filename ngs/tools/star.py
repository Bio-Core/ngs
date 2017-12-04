"""
A Python3 wrapper for the STAR and STAR-Fusion programs.
"""

import yaml

def align_rnaseq(
        read1=None,
        read2=None,
        prefix=None,
        genome_dir=None,
        star="STAR",
        mode="alignReads",
        num_threads=4,
        segment_min=20,
        read_files_command="zcat",
        two_pass_mode='Basic',
        sam_primary_flag='AllBestScore',
        filter_intron_motifs='RemoveNoncanonical',
        sam_type='BAM SortedByCoordinate',
        quant_mode='TranscriptomeSAM GeneCounts',
        sam_unmapped='Within',
        suffix_array_sparsity=2,
        bam_sort_ram=35000000000):
    """
    Produce the command for aligning FASTQ reads to a reference using the
    STAR aligner.

    Usage:
        align_rnaseq(config, star)

    Input:
          * config: dictionary containing STAR options to use in alignment (required)
          * read1: full path to the read 1 FASTQ file (required)
          * read2: full path to the read 2 FASTQ file (required)
          * prefix: the prefix to use for output files (required)
          * genome_dir: full path to the directory containing STAR genome index files (required)
          * star: full path to the STAR-Fusion program (default: STAR-Fusion) (default: STAR)
          * num_threads: number of threads to use (default: 4)
          * segment_min: minimum segment length (default: 20)
          * read_files_command: uncompress program to run on FASTQ files (default: zcat)
          * two_pass_mode: 2-pass mapping mode (default: Basic)
          * sam_primary_flag: definition for primary alignment (default: AllBestScore)
          * filter_intron_motifs: filter alignments based on intron motifs
            (default: RemoveNoncanonical)
          * sam_type: output SAM file type (default: BAM SortedByCoordinate)
          * quant_mode: types of quantification requested (default: TranscriptomeSAM GeneCounts)
          * sam_unmapped: output unmapped reads in SAM (default: Within)
          * suffix_array_sparsity: distance between indices (default: 2)
          * bam_sort_ram: max available RAM for sorting BAM file (default: 35000000000)

    Output:
        Returns a dictionary containing:
          * cmd: command to execute for alignment
          * output: name of output file alignment is written to

    """
    program = star
    options = ' '.join([
        '--runMode', mode,
        '--readFilesIn', read1, read2,
        '--outFileNamePrefix', prefix,
        '--genomeDir', genome_dir,
        '--runThreadN', str(num_threads),
        '--chimSegmentMin', str(segment_min),
        '--readFilesCommand', read_files_command,
        '--twopassMode', two_pass_mode,
        '--outSAMprimaryFlag', sam_primary_flag,
        '--outFilterIntronMotifs', filter_intron_motifs,
        '--outSAMtype', sam_type,
        '--quantMode', quant_mode,
        '--outSAMunmapped', sam_unmapped,
        '--genomeSAsparseD', str(suffix_array_sparsity),
        '--limitBAMsortRAM', str(bam_sort_ram)
        ])
    cmd = " ".join([program, options])
    junction_file = '.'.join([prefix, 'Chimeric.out.junction'])
    sam_file = '.'.join([prefix, 'Chimeric.out.sam'])
    trans_bam_file = '.'.join([prefix, 'Aligned.toTranscriptome.out.bam'])
    sorted_bam_file = '.'.join([prefix, 'sortedByCoord.out.bam'])
    return {"command": cmd,
            "junction": junction_file,
            "bam": trans_bam_file,
            "sorted_bam": sorted_bam_file,
            "sam": sam_file}


def get_default_config(file):
    """
    Get the default configuration for the STAR aligner as a dictionary.  Note
    that the values can be overwritten for custom configurations.

    Usage:
        get_default_config(file)

    Input:
        * file: default configuration file in YAML format containing all STAR
                options (required)

    Output:
        Returns a dictionary containing standard STAR options
    """
    with open(file, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


def get_fusions(
        junction,
        prefix,
        out_sam,
        gtf,
        star="STAR-Fusion"):
    """
    Create the command to get fusion transcripts from the STAR fusion
    subprogram.

    Usage:
        get_fusions()

    Input:
        junction: junction file from the STAR alignment
        prefix: output prefix
        out_sam: full path to the STAR output file containing .Chimeric.out.sam
        junction: full path to the STAR output file containing .Chimeric.out.junction
        gtf: full path to the GTF file
        star: the full path to the STAR-Fusion program
    """
    program = star
    options = " ".join([
        "--chimeric_junction", junction,
        "--chimeric_out_sam", out_sam,
        "--ref_GTF", gtf,
        "--out_prefix", prefix
        ])
    cmd = " ".join([program, options])
    return {"command": cmd}
