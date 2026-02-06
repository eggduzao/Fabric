import fabric.utils

annotate = fabric.utils.FabricDispatcher('bcftools', 'annotate')
call = fabric.utils.FabricDispatcher('bcftools', 'call')
cnv = fabric.utils.FabricDispatcher('bcftools', 'cnv')
concat = fabric.utils.FabricDispatcher('bcftools', 'concat')
consensus = fabric.utils.FabricDispatcher('bcftools', 'consensus')
convert = fabric.utils.FabricDispatcher('bcftools', 'convert')
csq = fabric.utils.FabricDispatcher('bcftools', 'csq')
filter = fabric.utils.FabricDispatcher('bcftools', 'filter')
gtcheck = fabric.utils.FabricDispatcher('bcftools', 'gtcheck')
head = fabric.utils.FabricDispatcher('bcftools', 'head')
index = fabric.utils.FabricDispatcher('bcftools', 'index')
isec = fabric.utils.FabricDispatcher('bcftools', 'isec')
merge = fabric.utils.FabricDispatcher('bcftools', 'merge')
mpileup = fabric.utils.FabricDispatcher('bcftools', 'mpileup')
norm = fabric.utils.FabricDispatcher('bcftools', 'norm')
plugin = fabric.utils.FabricDispatcher('bcftools', 'plugin')
query = fabric.utils.FabricDispatcher('bcftools', 'query')
reheader = fabric.utils.FabricDispatcher('bcftools', 'reheader')
roh = fabric.utils.FabricDispatcher('bcftools', 'roh')
sort = fabric.utils.FabricDispatcher('bcftools', 'sort')
stats = fabric.utils.FabricDispatcher('bcftools', 'stats')
view = fabric.utils.FabricDispatcher('bcftools', 'view')

__all__ = [
    'annotate', 'call', 'cnv', 'concat', 'consensus',
    'convert', 'csq', 'filter', 'gtcheck', 'head',
    'index', 'isec', 'merge', 'mpileup', 'norm',
    'plugin', 'query', 'reheader', 'roh', 'sort',
    'stats', 'view',
]
