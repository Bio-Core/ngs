"""
A Python 3 wrapper for the Picard suite of tools.
"""
from uuid import uuid4

class Picard(object):
    """

    """
    def __init__(
        self,
        picard="picard.jar",
        java="/usr/bin/java",
        tmpdir='tmp',
        validation_stringency='SILENT'):
        """
        Object initialization, auto-executed during class instantiation.
        """
        self.picard = picard
        self.java = java
        self.tmpdir = tmpdir
        self.validation_stringency="SILENT"
        return None

    def generate_addorreplacereadgroups_command(
        self,
        input,
        output,
        sample,
        library,
        unit,
        center,
        unique_id=str(uuid4()),
        memory=20,
        sort_order='coordinate',
        platform='ILLUMINA'):
        """
        Method for generating the command to execute the
        AddOrReplaceReadGroups Picard program.
        USAGE:
            generate_addorreplacereadgroups_command(
            input="input.bam",
            output="output.bam",
            sample="testsample",
            library="testlibrary",
            )
        INPUT:
            * input:        full path to the input BAM file (required)
            * output:       name of output BAM file (required)
            * unique_id:    unique identifier for the read group ID (optional)
            * sample:       name of sample to be used in the read group (required)
            * library:      name of library to be used in the read group (required)
            * unit:         platform unit containing flowcell barcode (required)
            * center:       the center where sequencing was performed (default: ca.uhn.pmgc)
            * sort_order:   the sort order for the reads (default: coordinate)
            * platform:     name of sequencing platform used (default: ILLUMINA)
            * memory:       memory allocation as integer (default: self.memory)
        OUTPUT:
            Returns a dictionary containing the command to be executed.
        """
        program =  ' '.join([
            self.java,
            ''.join(["-Xmx", str(memory), 'g']),
            '='.join(['-Djava.io.tmpdir', self.tmpdir]),
            "-jar", self.picard])
        options = ' '.join([
            "AddOrReplaceReadGroups",
            '='.join(["INPUT", input]),
            '='.join(["OUTPUT", output]),
            '='.join(["SORT_ORDER", sort_order]),
            '='.join(["RGID", unique_id]),
            '='.join(["RGLB", library]),
            '='.join(["RGPL", platform]),
            '='.join(["RGPU", unit]),
            '='.join(["RGSM", sample])
            ])
        cmd = ' '.join([program, options])
        return {"command":cmd}

    def generate_markduplicates_command(
        self,
        input,
        output,
        metrics,
        create_index=True,
        max_records=150000,
        memory=20):
        """
        Method for generating the command to execute the MarkDuplicates Picard
        program.
        
        USAGE:
            generate_markduplicates_command(input="input.bam", output="PROCESSED_BAMS/output",
                metric="PROCESSED_BAMS/sample", create_index=True, max_records=10000,
                memory=20)
        INPUT:
            * input: input BAM file for duplicate marking (required)
            * output: name of output to write data to (required)
            * metrics: metrics prefix (required)
            * create_index: create the BAM file index (default: True)
            * max_records: maximum number of records in memory (default: 150000)
            * memory: ammount of memory in GB to allocate to the Java heap (default: 20)
        OUTPUT:
            Returns a dictionary containing:
            * command: the command to be exected
        """
        if create_index:
            create_index_option = "TRUE"
        else:
            create_index_option = "FALSE"
        program = ' '.join([
            self.java,
            ''.join(["-Xmx", str(memory), 'g']),
            '='.join(['-Djava.io.tmpdir', self.tmpdir]),
            "-jar", self.picard])
        options = ' '.join([
            'MarkDuplicates',
            '='.join(["INPUT", input]),
            '='.join(["OUTPUT", output]),
            '='.join(["METRICS_FILE", metrics]),
            '='.join(["CREATE_INDEX", create_index_option]),
            '='.join(["MAX_RECORDS_IN_RAM", str(max_records)]),
            '='.join(["VALIDATION_STRINGENCY", self.validation_stringency])
            ])
        cmd = ' '.join([program, options])
        return {"command":cmd}

