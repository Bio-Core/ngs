"""
A Python3 wrapper for the RNASeQC software package.
"""
import logging

def generate_rnaseqc_command(
        output,
        gtf,
        reference,
        sample_list,
        java,
        rnaseqc,
        tmpdir,
        bwa='bwa',
        single_end='NO',
        memory='8'):
    """
    NAME
        generate_rnseqc_commands -- A Python3 function that generates the
        RNASeQC executable command.
    SYNOPSIS
        generate_rnaseqc_command()
    INPUT
        * output: full path to the output directory (required)
        * gtf: full path to the annotated transcript file in GTF format (required)
        * reference: full path to the reference genome in FASTA format (required)
        * sample_list: tab separated sample text file (required)
        * java: full path to the Java program (default: java)
        * rnaseqc: full path to the RNASeQC JAR file (required)
        * tmpdir: full path to a temporary directory (default: auto-creates a temporary directory)
        * bwa: full path to the BWA executable (default: bwa)
        * single_end: full path to the sample list file (default: NO)
        * memory: amount of memory to allocate to the heap (default: 8)
    OUTPUT
        Returns an executable command for RNASeQC as a dictionary:
        * command: executable command to run RNASeQC
    """
    if java is None:
        java = "java"
    if rnaseqc is None:
        exit(logging.critical("Please provide full path to the RNASeQC program"))
    program = " ".join([
        java,
        ''.join(['-Xmx', str(memory), 'g']),
        ''.join(['-Djava.io.tmpdir=', tmpdir]),
        '-jar', rnaseqc
        ])
    options = " ".join([
        "-bwa", bwa,
        "-o", output,
        "-t", gtf,
        "-r", reference,
        "-singleEnd", single_end,
        "-s", sample_list
        ])
    cmd = ' '.join([program, options])
    return {"command":cmd}
