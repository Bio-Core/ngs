"""
A Python 3 wrapper for the Genome Analysis Toolkit (GATK v3.7).
"""
###############################################################################
### Class definition
###############################################################################
class Gatk(object):
    """
    NAME
        gatk -- A Python class wrapper for the Genome Analysis Toolkit
    SYNOPSIS
        object = Gatk()
    DESCRIPTION
        A class that wraps the methods and attributes of the Genome Analysis
        toolkit.
    """

    def __init__(self,
                 gatk="GenomeAnalysisTK.jar",
                 reference="ref.fa",
                 java='/usr/bin/java',
                 tmpdir='./tmp',
                 logginglevel='INFO',
                 output_dir='.'):
        """
        This is the standard object initialization method that is automatically
        executed when an object is instantiated with this class.

        NOTE:
            Do not call this method directly.  It will automatically be called
            when the class is instantiated.

        USAGE:
            object = Gatk(gatk='/usr/bin/GenomeAnalysisTk.jar', reference='hg19.fa')

        INPUT:
             * gatk: full path to the GATK JAR file (required)
             * reference: full path to the reference genome used (required)
             * java: full path to the java program (default: /usr/bin/java)
             * tmpdir: full path to the temporary directory (default: ./tmp)
             * logginglevel: the level of logging to be used (default: INFO)
             * output_dir: the output directory to output files to (default: .)
        """
        self.java = java
        self.gatk = gatk
        self.reference = reference
        self.tmpdir = tmpdir
        self.logginglevel = logginglevel
        self.output_dir = output_dir
        return None

    def split_n_cigar_reads(self,
                            bams,
                            output,
                            readfilters=('ReassignOneMappingQuality', 'UnmappedRead'),
                            memory=20,
                            original_mapq=255,
                            reassigned_mapq=60):
        """
        Method wrapper for the GATK's SplitNCigarReads subprogram.
        USAGE:
            object.split_n_cigar_reads(
                bams,
                output,
                readfilters,
                memory,
                original_mapq,
                reassigned_mapq
                )

        INPUT:
            * bams:             list of input BAM files (required)
            * output:           output filename
            * readfilters:      list of read filters to apply (default: None)
            * memory:           amount of memory to allocate to the Java engine (default: 20)
            * original_mapq:    mapping quality to change from (default: 255)
            * reassigned_mapq:  mapping quality to change to (default: 60)

        OUTPUT:
            Returns a dictionary containing the command and output filename.
        """
        gatk_memory = ''.join(['-Xmx', str(memory), 'g'])
        gatk_tmp = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        output_filename = ''
        program = ' '.join([
            self.java,
            gatk_memory,
            gatk_tmp,
            '-jar', str(self.gatk)
            ])

        # create input BAM file string
        input_option = " ".join(['-I ' + input_bam for input_bam in bams])

        # build the option for read filter files
        read_filter_option = " ".join(['-rf ' + readfilter for readfilter in readfilters])

        output_filename = '/'.join([self.output_dir, output])
        options = ' '.join([
            '-T SplitNCigarReads',
            input_option,
            '-R', self.reference,
            '-o', output_filename,
            read_filter_option,
            '--reassign_mapping_quality_from', str(original_mapq),
            '--reassign_mapping_quality_to', str(reassigned_mapq),
            '-U ALLOW_N_CIGAR_READS'
            ])
        cmd = ' '.join([program, options])
        return {"command":cmd, "output":output_filename}
    def realigner_target_creator(self,
                                 bams,
                                 output,
                                 memory=20,
                                 threads=8,
                                 knownsites=None):
        """
        Method wrapper for GATK's RealignerTargetCreator subprogram.

        USAGE:
            object.realigner_target_creator(
                bams = [input1, input2, input3],
                output = <output realigner target file>,
                memory = <memory allocated to Java>,
                threads = <number of threads to use>,
                knownsites = [knownsite1, knownsite2, knownsite3],
                output_dir = <output directory>
                )
        INPUT:
            * bams:         array of input files (required)
            * output:       output realigner target filename (required)
            * memory:       amount of memory to allocate to the Java engine (default: 20)
            * threads:      number of threads to use (default: '8')
            * knownsites:   a list of known indel sites (default: [])
            * output_dir:   path to the output directory to write the output to (default: .)

        OUTPUT:
            Returns a dictionary containing the command and output filename
        """
        gatk_memory = ''.join(['-Xmx', str(memory), 'g'])
        gatk_tmp = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        program = ' '.join([
            self.java,
            gatk_memory,
            gatk_tmp,
            '-jar', str(self.gatk)
            ])
        output_filename = '/'.join([self.output_dir, output])

        # build the option for input BAM files
        input_option = " ".join(['-I ' + input_bam for input_bam in bams])
        options = ' '.join([
            '-T RealignerTargetCreator',
            input_option,
            '-o', output_filename,
            '-R', self.reference,
            '-nt', str(threads),
            '-l', self.logginglevel
            ])

        # build the option for known indel sites
        if knownsites:
            knownsites_option = " ".join(['--known ' + site for site in knownsites])
            options = " ".join([options, knownsites_option])
        cmd = ' '.join([program, options])
        return {"command": cmd, "output":output_filename}

    def indel_realigner(self,
                        bams,
                        output,
                        intervals,
                        memory=20):
        """
        Python wrapper for handling GATK's IndelRealigner sub-program.

        USAGE:
            object.indel_realigner(
                bams = [input1, input2, input3],
                output = <output BAM file>,
                intervals = <output from realigner target creator>,
                memory = <memory allocated to Java>
                )

        INPUT:
            * bams:         array of input BAM files (required)
            * output:       indel realigned output BAM file (required)
            * intervals:    output from the realigner target creator (required)
            * memory:       amount of memory to allocate to the Java engine (default: 20)

        OUTPUT:
             Returns a dictionary containing the command and output filename
        """
        java_memory = ''.join(['-Xmx', str(memory), 'g'])
        gatk_tmp = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        program = ' '.join([
            self.java,
            java_memory,
            gatk_tmp,
            '-jar', str(self.gatk)
            ])
        input_option = " ".join(['-I ' + input_bam for input_bam in bams])
        output_filename = '/'.join([self.output_dir, output])
        options = ' '.join([
            '-T IndelRealigner',
            input_option,
            '-o', '/'.join([self.output_dir, output]),
            '-targetIntervals', intervals,
            '-R', self.reference
            ])
        cmd = ' '.join([program, options])
        return {'command':cmd, 'output':output_filename}

    def base_quality_recalibration(self,
                                   bams,
                                   output,
                                   memory=20,
                                   knownsites=None):
        """
        A method that wraps GATK's base quality recalibration suprogram.
        USAGE:
            object.base_quality_recalibration(bams, output, memory):

        INPUT:
            * bams: BAM file to process
            * output: name of file to write output to
            * memory: memory (in GB) to allocate to the Java engine (default: 26)

        OUTPUT:
             list of return values
        """
        java_memory = ''.join(['-Xmx', str(memory), 'g'])
        java_tmp = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        output_filename = '/'.join([self.output_dir, output])
        input_option = " ".join(['-I ' + input_bam for input_bam in bams])
        program = ' '.join([
            self.java,
            java_memory,
            java_tmp,
            "-jar", str(self.gatk)
            ])
        options = ' '.join([
            '-T', 'BaseRecalibrator',
            '-I', input_option,
            '-o', output_filename,
            '-R', self.reference,
            '-U ALLOW_N_CIGAR_READS'
            ])
        if knownsites:
            knownsites_option = " ".join(['--knownSites ' + site for site in knownsites])
            options = " ".join([options, knownsites_option])
        cmd = ' '.join([program, options])
        return {'command':cmd, 'output':output_filename}

    def print_reads(self,
                    bam,
                    output,
                    recaldata,
                    memory=20,
                    threads=4):
        """
        A method that wraps GATK's PrintReads subprogram.

        USAGE:
            object.print_reads(bam, output, recaldata, memory,
                threads)
        INPUT:
            * bam: BAM file to process
            * output: output BAM file to write data to
            * recaldata: base quality recalibration table
            * memory: memory to allocate to the Java engine
            * threads: number of threads to execute across
        OUTPUT:
            A BAM file containing base quality recalibrated BAM files.
        """
        java_memory = ''.join(['-Xmx', str(memory), 'g'])
        java_tmp = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        output_filename = '/'.join([self.output_dir, output])
        program = ' '.join([
            self.java,
            java_memory,
            java_tmp,
            '-jar', str(self.gatk)
            ])
        options = ' '.join([
            '-T PrintReads',
            '-I', bam,
            '-o', output_filename,
            '-R', self.reference,
            '-BQSR', recaldata,
            '-nct', str(threads),
            '-rf BadCigar'
            ])
        cmd = ' '.join([program, options])
        return {"command": cmd, "output": output_filename}

    def haplotype_caller(self,
                         bams,
                         dbsnp,
                         output,
                         stand_call_conf=20,
                         stand_emit_conf=20,
                         memory=8):
        """
        A method wrapper for the HaplotypeCaller from GATK.

        USAGE:
            object.haplotype_caller(
                bams,
                dbsnp,
                output,
                stand_call_conf=20,
                stand_emit_conf=20,
                memory=8)

        INPUT:
            * bams:             list of BAM files to process (required)
            * dbsnp:            VCF of dbSNP (required)
            * output:           name of output file (required)
            * stand_call_conf:  min Phred scale confidence for call (default: 20)
            * stand_emit_conf:  min Phred scale confidence to show (default: 20)
            * memory:           amount of memory to allocate to Java heap (default: 8)

        OUTPUT:
             list of return values
        """
        java_memory = ''.join(['-Xmx', str(memory), 'g'])
        java_tmpdir = ''.join(['-Djava.io.tmpdir=', self.tmpdir])
        program = ' '.join([
            self.java,
            java_memory,
            java_tmpdir,
            '-jar', str(self.gatk)
            ])
        input_option = ' '.join(['-I ' + bam for bam in bams])
        output_filename = '/'.join([self.output_dir, str(output)])
        options = ' '.join([
            '-T HaplotypeCaller',
            input_option,
            '--dbsnp', dbsnp,
            '-R', self.reference,
            '-o', output_filename,
            '-stand_call_confg', str(stand_call_conf),
            '-stand_emit_conf', str(stand_emit_conf),
            '-dontUseSoftClippedBases'
            ])
        cmd = ' '.join([program, options])
        self.variant_output = output_filename
        return {"command": cmd, "output": self.variant_output}

    def variant_filtration(self,
                           variant,
                           output,
                           filters,
                           window=35,
                           cluster=3,
                           memory=8):
        """
        A Python method that wraps the GATK VariantFiltration subprogram.

        USAGE:
            object.variant_filtration(
                variantoutput.vcf,
                output=output.filtered.vcf,
                filters="QD:QD<2.0","FS:FS>30.0",
                window=35,
                cluster=3,
                memory=8)
        INPUT:
            * variant:      VCF file from HaplotypeCaller (required)
            * output:       name of output file to write filtered data to
                            (required)
            * filters:      a comma separates string of f filters to apply in
                            "name:filter,name:filter" format (default: "")
            * window:       window size to evaluate clustered SNPs (default: 35)
            * cluster:      number of SNPs making up a cluster (default: 3)
            * memory:       amount of memory to allocate to the Java heap in GB
                            (default: 8)

        OUTPUT:
            Returns a dictionary containing the command to execute and path to
            the output file.
        """
        program = ' '.join([
            self.java,
            ''.join(['-Xmx', str(memory), 'g']),
            ''.join(['-Djava.io.tmpdir=', self.tmpdir]),
            '-jar', str(self.gatk)
            ])
        output_filename = '/'.join([self.output_dir, output])
        filter_list = []
        filter_option = ""
        if filters != "":
            # the filters will be a string comprised:
            #   <name1>:<filter1>,<name2>:<filter2>...
            filter_dict = dict(item.split(":") for item in filters.split(","))
            for key, value in filter_dict.items():
                filter_list.extend([
                    '--filterName',
                    key,
                    '--filterExpression',
                    ''.join(["\"", value, "\""])
                    ])
            filter_option = ' '.join(filter_list)
        options = ' '.join([
            '-T VariantFiltration',
            '-R', self.reference,
            '--variant', output,
            '-o', output_filename,
            '-window', str(window),
            '-cluster', str(cluster)])
        if filter_option != "":
            options = ' '.join([options, filter_option])
        cmd = ' '.join([program, options])
        return {"command":cmd, "output":output_filename}

    def depth_of_coverage(self,
                          bam=None,
                          output=None,
                          ref=None,
                          java=None,
                          gatk=None,
                          memory=8,
                          intervals=None):
        """
        A Python method that wraps the GATK DepthOfCoverage subprogram.
        USAGE:
            object.depth_of_coverage(
                bam,
                output,
                memory,
                intervals)
        INPUT:
            * bam:          BAM file to calculate depth of coverage
            * output:       name of output file
            * ref:          reference (FASTA) file
            * java:         Java program to use (default: /usr/bin/java)
            * gatk:         full path to the GATK jar file (default: GenomeAnalysisTK.jar)
            * memory:       memory to allocate to the Java heap in GB (default: 8)
            * intervals:    a GATK compatible interval file (default: None)
        """
        # validate the method arguments
        if java is None:
            java = self.java
        if gatk is None:
            gatk = self.gatk
        if ref is None:
            ref = self.reference
        program = ' '.join([
            self.java,
            ''.join(['-Xmx', str(memory), 'g']),
            ''.join(['-Djava.io.tmpdir=', self.tmpdir]),
            '-jar', str(gatk)
            ])
        output_filename = '/'.join([self.output_dir, output])
        options = ' '.join([
            '-T DepthOfCoverage',
            '-I', bam,
            '-R', ref,
            '-o', output_filename,
            '--omitDepthOutputAtEachBase'
            ])
        # limit coverage calculations to intervals, this is useful when calculating
        # coverage for a panel or exomes
        if intervals is not None:
            options = ' '.join([
                options,
                '-L',
                intervals
                ])
        cmd = ' '.join([program, options])
        return {"command":cmd, "output":output_filename}
