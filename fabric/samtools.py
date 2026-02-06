import fabric.utils

addreplacerg = fabric.utils.FabricDispatcher('samtools', 'addreplacerg')
ampliconclip = fabric.utils.FabricDispatcher('samtools', 'ampliconclip')
ampliconstats = fabric.utils.FabricDispatcher('samtools', 'ampliconstats')
bam2fq = fabric.utils.FabricDispatcher('samtools', 'bam2fq')
bamshuf = fabric.utils.FabricDispatcher('samtools', 'bamshuf')
bedcov = fabric.utils.FabricDispatcher('samtools', 'bedcov')
calmd = fabric.utils.FabricDispatcher('samtools', 'calmd')
cat = fabric.utils.FabricDispatcher('samtools', 'cat')
checksum = fabric.utils.FabricDispatcher('samtools', 'checksum')
collate = fabric.utils.FabricDispatcher('samtools', 'collate')
consensus = fabric.utils.FabricDispatcher('samtools', 'consensus')
coverage = fabric.utils.FabricDispatcher('samtools', 'coverage')
cram_size = fabric.utils.FabricDispatcher('samtools', 'cram-size')
depad = fabric.utils.FabricDispatcher('samtools', 'depad')
depth = fabric.utils.FabricDispatcher('samtools', 'depth')
dict = fabric.utils.FabricDispatcher('samtools', 'dict')
faidx = fabric.utils.FabricDispatcher('samtools', 'faidx')
fasta = fabric.utils.FabricDispatcher('samtools', 'fasta')
fastq = fabric.utils.FabricDispatcher('samtools', 'fastq')
fixmate = fabric.utils.FabricDispatcher('samtools', 'fixmate')
flags = fabric.utils.FabricDispatcher('samtools', 'flags')
flagstat = fabric.utils.FabricDispatcher('samtools', 'flagstat')
fqidx = fabric.utils.FabricDispatcher('samtools', 'fqidx')
fqimport = fabric.utils.FabricDispatcher('samtools', 'import')
head = fabric.utils.FabricDispatcher('samtools', 'head')
idxstats = fabric.utils.FabricDispatcher('samtools', 'idxstats')
index = fabric.utils.FabricDispatcher('samtools', 'index')
markdup = fabric.utils.FabricDispatcher('samtools', 'markdup')
merge = fabric.utils.FabricDispatcher('samtools', 'merge')
mpileup = fabric.utils.FabricDispatcher('samtools', 'mpileup')
pad2unpad = fabric.utils.FabricDispatcher('samtools', 'pad2unpad')
phase = fabric.utils.FabricDispatcher('samtools', 'phase')
quickcheck = fabric.utils.FabricDispatcher('samtools', 'quickcheck')
reference = fabric.utils.FabricDispatcher('samtools', 'reference')
reheader = fabric.utils.FabricDispatcher('samtools', 'reheader')
reset = fabric.utils.FabricDispatcher('samtools', 'reset')
rmdup = fabric.utils.FabricDispatcher('samtools', 'rmdup')
samples = fabric.utils.FabricDispatcher('samtools', 'samples')
sort = fabric.utils.FabricDispatcher('samtools', 'sort')
split = fabric.utils.FabricDispatcher('samtools', 'split')
stats = fabric.utils.FabricDispatcher('samtools', 'stats')
targetcut = fabric.utils.FabricDispatcher('samtools', 'targetcut')
tview = fabric.utils.FabricDispatcher('samtools', 'tview')
version = fabric.utils.FabricDispatcher('samtools', 'version')
view = fabric.utils.FabricDispatcher('samtools', 'view')

__all__ = [
    'addreplacerg', 'ampliconclip', 'ampliconstats',
    'bam2fq', 'bamshuf', 'bedcov', 'calmd', 'cat', 'checksum',
    'collate', 'consensus', 'coverage', 'cram_size',
    'depad', 'depth', 'dict', 'faidx', 'fasta',
    'fastq', 'fixmate', 'flags', 'flagstat', 'fqidx',
    'fqimport', 'head', 'idxstats', 'index',
    'markdup', 'merge', 'mpileup', 'pad2unpad',
    'phase', 'quickcheck', 'reference', 'reheader',
    'reset', 'rmdup', 'samples', 'sort', 'split',
    'stats', 'targetcut', 'tview', 'version', 'view',
]
