"""
A Python3 wrapper for the TopHat2 suite of tools.
"""
def generate_tophat2_command(
        read1,
        read2,
        genome_dir,
        gtf,
        output,
        fusion_ignore_chromosomes=None,
        threads=8,
        inner_mate_distance=10,
        mate_std_dev=35,
        max_intron_length=100000,
        fusion_min_dist=100000,
        fusion_anchor_length=13,
        tophat2="tophat2"):
    """
    A method that wraps the TopHat2 program and generates the command
    to execute for transcript alignment.
    """
    # validate the input arguments
    if fusion_ignore_chromosomes is None:
        fusion_ignore_chromosomes = ["M"]
    program = ' '.join([tophat2])
    options = ' '.join([
        '-p', str(threads),
        "--fusion-search",
        "--bowtie1",
        "--no-coverage-search",
        "--keep-fasta-order",
        "-r", str(inner_mate_distance),
        "--mate-std-dev", str(mate_std_dev),
        "--max-intron-length", str(max_intron_length),
        "--fusion-min-dist", str(fusion_min_dist),
        "--fusion-anchor-length", str(fusion_anchor_length),
        "--fusion-ignore-chromosomes", ','.join(fusion_ignore_chromosomes),
        "-G", gtf,
        "-o", output
        ])
    cmd = ' '.join([program, options, genome_dir, read1, read2])
    return {"command":cmd}
