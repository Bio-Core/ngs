import ngs.tools.gatk as ngs

gatk = ngs.Gatk()
gatk_cov = gatk.depth_of_coverage(bam="input.bam", output="depth")
print(gatk_cov)

