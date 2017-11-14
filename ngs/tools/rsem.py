"""
A Python3 wrapper for the RSEM software package.
"""
def generate_rsem_command(
        bam,
        output_prefix,
        rsem_ref,
        threads=8,
        strand_specific=True,
        program='rsem-calculate-expression'
        ):
    """
    USAGE:
        generate_rsem_command(
            bam=test.bam,
            output_prefix=RSEM/sample
            rsem_ref=genome/ref
            threads=16,
            strand_specific=True,
            program=rsem-calculate-expression)
    INPUT:
        * bam: BAM file to process (required)
        * output_prefix: directory and name to prepend to output files (required)
        * rsem_ref: full path to the rsem program (required)
        * threads: number of threads to use (default: 8)
        * strand_specific: boolean to determine whether to calculate expression
            based on strandedness (default: True)
        * program: full path to the rsem-calculate-expression program
    OUTPUT:
        Output files will be located in the directory defined by the output-
        prefix argument.
    """
    # validate the input arguments
    if rsem_ref is None:
        rsem_ref = '/'.join([
            '/cluster/projects/carlsgroup/workinprogress/abdel',
            '20170418_INSPIRE_RNA/RSEM_REF_hg38_gencode/hg38'])
    if output_prefix is None:
        print("output_prefix is a required argument")
        exit()
    program = ' '.join([
        program
        ])
    options = ' '.join([
        '-p', str(threads),
        '--bam',
        '--paired-end', bam,
        ])
    # append strand-specific flag if that option is set to true (default)
    if strand_specific is True:
        options = ' '.join([options, '--strand-specific'])
    options = ' '.join([options, rsem_ref, output_prefix])
    cmd = ' '.join([program, options])
    return {"command":cmd}
