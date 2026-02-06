.. _Usage: 

=========================================
Working with BAM/CRAM/SAM-formatted files
=========================================

Opening a file
==============

To begin with, import the fabric module and open a
:class:`fabric.AlignmentFile`::

   import fabric
   samfile = fabric.AlignmentFile("ex1.bam", "rb")

The above command opens the file :file:`ex1.bam` for reading.
The ``b`` qualifier indicates that this is a :term:`BAM` file. 
To open a :term:`SAM` file, type::

   import fabric
   samfile = fabric.AlignmentFile("ex1.sam", "r")

:term:`CRAM` files are identified by a ``c`` qualifier::

   import fabric
   samfile = fabric.AlignmentFile("ex1.cram", "rc")

Fetching reads mapped to a :term:`region`
=========================================

Reads are obtained through a call to the
:meth:`fabric.AlignmentFile.fetch` method which returns an iterator.
Each call to the iterator will returns a :class:`fabric.AlignedSegment`
object::

   iter = samfile.fetch("seq1", 10, 20)
   for x in iter:
       print(str(x))

:meth:`fabric.AlignmentFile.fetch` returns all reads overlapping a
region sorted by the first aligned base in the :term:`reference`
sequence.  Note that it will also return reads that are only partially
overlapping with the :term:`region`. Thus the reads returned might
span a region that is larger than the one queried.

Using the pileup-engine
=======================

In contrast to :term:`fetching`, the :term:`pileup` engine returns for
each base in the :term:`reference` sequence the reads that map to that
particular position. In the typical view of reads stacking vertically
on top of the reference sequence similar to a multiple alignment,
:term:`fetching` iterates over the rows of this implied multiple
alignment while a :term:`pileup` iterates over the :term:`columns<column>`.

Calling :meth:`~fabric.AlignmentFile.pileup` will return an iterator
over each :term:`column` (reference base) of a specified
:term:`region`. Each call to the iterator returns an object of the
type :class:`fabric.PileupColumn` that provides access to all the
reads aligned to that particular reference position as well as
some additional information::

   iter = samfile.pileup('seq1', 10, 20)
   for x in iter:
      print(str(x))
 

Creating BAM/CRAM/SAM files from scratch
========================================

The following example shows how a new :term:`BAM` file is constructed
from scratch.  The important part here is that the
:class:`fabric.AlignmentFile` class needs to receive the sequence
identifiers. These can be given either as a dictionary in a header
structure, as lists of names and sizes, or from a template file.
Here, we use a header dictionary::

   header = { 'HD': {'VN': '1.0'},
               'SQ': [{'LN': 1575, 'SN': 'chr1'}, 
                      {'LN': 1584, 'SN': 'chr2'}] }

   with fabric.AlignmentFile(tmpfilename, "wb", header=header) as outf:
       a = fabric.AlignedSegment()
       a.query_name = "read_28833_29006_6945"
       a.query_sequence="AGCTTAGCTAGCTACCTATATCTTGGTCTTGGCCG"
       a.flag = 99
       a.reference_id = 0
       a.reference_start = 32
       a.mapping_quality = 20
       a.cigar = ((0,10), (2,1), (0,25))
       a.next_reference_id = 0
       a.next_reference_start=199
       a.template_length=167
       a.query_qualities = fabric.qualitystring_to_array("<<<<<<<<<<<<<<<<<<<<<:<9/,&,22;;<<<")
       a.tags = (("NM", 1),
		 ("RG", "L1"))
       outf.write(a)

Using streams
=============

Fabric does not support reading and writing from true python file
objects, but it does support reading and writing from stdin and
stdout. The following example reads from stdin and writes to stdout::

   infile = fabric.AlignmentFile("-", "r")
   outfile = fabric.AlignmentFile("-", "w", template=infile)
   for s in infile:
       outfile.write(s)

It will also work with :term:`BAM` files. The following script
converts a :term:`BAM` formatted file on stdin to a :term:`SAM`
formatted file on stdout::

   infile = fabric.AlignmentFile("-", "rb")
   outfile = fabric.AlignmentFile("-", "w", template=infile)
   for s in infile:
       outfile.write(s)

Note that the file open mode needs to changed from ``r`` to ``rb``.

==================================================
Using samtools and bcftools commands within Python
==================================================

Commands available in `samtools`_ and `bcftools`_ are available as simple
function calls, with command line options provided as arguments. For
example::

   import fabric.samtools
   fabric.samtools.sort("-o", "output.bam", "ex1.bam", catch_stdout=False)

   import fabric.bcftools
   fabric.bcftools.index("--csi", "ex2.vcf.gz")

corresponds to the command lines::

   samtools sort -o output.bam ex1.bam
   bcftools index --csi ex2.vcf.gz

Samtools commands are also imported into the main ``fabric`` namespace.
For example::

   fabric.sort("-m", "1000000", "-o", "output.bam", "ex1.bam", catch_stdout=False)

To make them valid Python identifiers, the functions :func:`!cram_size`
and :func:`!fqimport` are spelt thus, differently from their
corresponding commands.

In order to get usage information, try::

   print(fabric.sort.usage())

Argument errors raise a :class:`fabric.SamtoolsError`::

   fabric.sort()

   Traceback (most recent call last):
   File "x.py", line 12, in <module>
     fabric.sort()
   File "/build/lib.linux-x86_64-2.6/fabric/__init__.py", line 37, in __call__
     if retval: raise SamtoolsError( "\n".join( stderr ) )
   fabric.SamtoolsError: 'Usage: samtools sort [-n] [-m <maxMem>] <in.bam> <out.prefix>\n'

Messages from `samtools`_ on stderr are captured and are
available using the :meth:`~FabricDispatcher.get_messages` method::

   fabric.sort.get_messages()

By default, fabric captures the samtools command's standard output and returns it
as the function's return value. To redirect stdout to a file instead, either use
the ``save_stdout`` keyword argument, or use ``"-o", "filename"`` in the arguments
and also use ``catch_stdout=False`` to prevent fabric's capturing from overriding
your redirection. Finally, ``catch_stdout=False`` by itself discards standard output,
which may help resolve problems in environments such as IPython notebooks::

   # Return value
   pileup_text = fabric.samtools.mpileup("in.bam")

   # Save to file
   fabric.samtools.mpileup("in.bam", save_stdout=pileup_filename)
   fabric.samtools.mpileup("-o", pileup_filename, "in.bam", catch_stdout=False)

   # Discard standard output
   fabric.samtools.mpileup("in.bam", catch_stdout=False)  # Returns None

For each :obj:`!command` available as a `samtools`_ subcommand,
the following functions are provided:

.. py:function:: fabric.samtools.command(args, *, catch_stdout=True, save_stdout=None, split_lines=False)

   :param args: Arguments to be passed to the samtools subcommand.
   :param bool catch_stdout: Whether to return stdout as the function's value.
   :param str save_stdout: Filename to which stdout should be written.
   :param bool split_lines: Whether to split the return value into a list of lines.
   :returns: Standard output if it was caught, otherwise None.

   If `save_stdout` is not None, the command's standard ouput is written to the
   file specified and the function returns None.

   Otherwise, if `catch_stdout` is true, the command's standard output is captured
   and used as the function's return value --- either as a single :obj:`str` or as
   :obj:`list[str] <list>` according to `split_lines`. If `catch_stdout` is false,
   the command's standard output is discarded and the function returns None.

   The command's standard error is always captured and made available via
   :func:`~fabric.samtools.command.get_messages`.

.. py:function:: fabric.samtools.command.get_messages()

   Returns the standard error from the most recent invocation of the particular
   :obj:`!command`, either as a single :obj:`str` or as :obj:`list[str] <list>`
   according to `split_lines` as specified in that invocation.

.. py:function:: fabric.samtools.command.usage()

   Returns the command's usage/help message, as a single :obj:`str`.

For each :obj:`!command` available as a `bcftools`_ subcommand, the
:func:`!fabric.bcftools.command`, :func:`!fabric.bcftools.command.get_messages`,
and :func:`!fabric.bcftools.command.usage` functions operate similarly.


================================
Working with tabix-indexed files
================================

To open a tabular file that has been indexed with tabix_, use
:class:`~fabric.TabixFile`::

    import fabric
    tbx = fabric.TabixFile("example.bed.gz")

Similar to :class:`~fabric.AlignmentFile.fetch`, intervals within a
region can be retrieved by calling :meth:`~fabric.TabixFile.fetch()`::

    for row in tbx.fetch("chr1", 1000, 2000):
         print(str(row))

This will return a tuple-like data structure in which columns can
be retrieved by numeric index::

    for row in tbx.fetch("chr1", 1000, 2000):
         print("chromosome is", row[0])

By providing a parser to :class:`~fabric.AlignmentFile.fetch`
or :class:`~fabric.TabixFile`, the data will we presented in parsed
form::

    for row in tbx.fetch("chr1", 1000, 2000, parser=fabric.asTuple()):
         print("chromosome is", row.contig)
         print("first field (chrom)=", row[0])

Pre-built parsers are available for :term:`bed`
(:class:`~fabric.asBed`) formatted files and :term:`gtf`
(:class:`~fabric.asGTF`) formatted files. Thus, additional fields
become available through named access, for example::

    for row in tbx.fetch("chr1", 1000, 2000, parser=fabric.asBed()):
         print("name is", row.name)


.. Currently inactivated as pileup deprecated
.. Using the samtools SNP caller
.. -----------------------------

.. There are two ways to access the samtools SNP caller. The :class:`fabric.IteratorSNPCalls`
.. is appropriate when calling many consecutive SNPs, while :class:`fabric.SNPCaller` is
.. best when calling SNPs at non-consecutive genomic positions. Each snp caller returns objects of
.. type :class:`fabric.SNPCall`.

.. To use :class:`fabric.IteratorSNPCalls`, associate it with a :class:`fabric.IteratorColumn`::

..     samfile = fabric.AlignmentFile( "ex1.bam", "rb")  
..     fastafile = fabric.Fastafile( "ex1.fa" )
..     pileup_iter = samfile.pileup( stepper = "samtools", fastafile = fastafile )
..     sncpall_iter = fabric.IteratorSNPCalls(pileup_iter)
..     for call in snpcall_iter:
..         print(str(call))

.. Usage of :class:`fabric.SNPCaller` is similar::

..     samfile = fabric.AlignmentFile( "ex1.bam", "rb")  
..     fastafile = fabric.Fastafile( "ex1.fa" )
..     pileup_iter = samfile.pileup( stepper = "samtools", fastafile = fastafile )
..     snpcaller = fabric.SNPCaller.call(pileup_iter)
..     print(snpcaller( "chr1", 100 ))

.. Note the use of the option *stepper* to control which reads are included in the 
.. in the :term:`pileup`. The ``samtools`` stepper implements the same read selection
.. and processing as in the samtools pileup command.

.. Calling indels works along the same lines, using the :class:`fabric.IteratorIndelCalls`
.. and :class:`fabric.IteratorIndelCaller`.


====================================
Working with VCF/BCF formatted files
====================================

To iterate through a VCF/BCF formatted file use
:class:`~fabric.VariantFile`::

   from fabric import VariantFile

   bcf_in = VariantFile("test.bcf")  # auto-detect input format
   bcf_out = VariantFile('-', 'w', header=bcf_in.header)
   
   for rec in bcf_in.fetch('chr1', 100000, 200000):
       bcf_out.write(rec)

:meth:`_fabric.VariantFile.fetch()` iterates over
:class:`~fabric.VariantRecord` objects which provides access to
simple variant attributes such as :class:`~fabric.VariantRecord.contig`,
:class:`~fabric.VariantRecord.pos`, :class:`~fabric.VariantRecord.ref`::

   for rec in bcf_in.fetch():
       print(rec.pos)

but also to complex attributes such as the contents to the
:class:`~fabric.VariantRecord.info`, :class:`~fabric.VariantRecord.format`
and :term:`genotype` columns. These
complex attributes are views on the underlying htslib data structures
and provide dictionary-like access to the data::

   for rec in bcf_in.fetch():
       print(rec.info)
       print(rec.info.keys())
       print(rec.info["DP"])

The :py:attr:`~fabric.VariantFile.header` attribute
(:class:`~fabric.VariantHeader`) provides access information
stored in the :term:`vcf` header. The complete header can be printed::

   >>> print(bcf_in.header)
   ##fileformat=VCFv4.2
   ##FILTER=<ID=PASS,Description="All filters passed">
   ##fileDate=20090805
   ##source=myImputationProgramV3.1
   ##reference=1000GenomesPilot-NCBI36
   ##phasing=partial
   ##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples
   With Data">
   ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
   ##INFO=<ID=AF,Number=.,Type=Float,Description="Allele Frequency">
   ##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
   ##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build
   129">
   ##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
   ##FILTER=<ID=q10,Description="Quality below 10">
   ##FILTER=<ID=s50,Description="Less than 50% of samples have data">
   ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
   ##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
   ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
   ##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
   ##contig=<ID=M>
   ##contig=<ID=17>
   ##contig=<ID=20>
   ##bcftools_viewVersion=1.3+htslib-1.3
   ##bcftools_viewCommand=view -O b -o example_vcf42.bcf
   example_vcf42.vcf.gz
   #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO   FORMAT    NA00001 NA00002 NA0000
  
Individual contents such as contigs, info fields, samples, formats can
be retrieved as attributes from :py:attr:`~fabric.VariantFile.header`::

   >>> print(bcf_in.header.contigs)
   <fabric.cbcf.VariantHeaderContigs object at 0xf250f8>

To convert these views to native python types, iterate through the views::

   >>> print(list((bcf_in.header.contigs)))
   ['M', '17', '20']
   >>> print(list((bcf_in.header.filters)))
   ['PASS', 'q10', 's50']
   >>> print(list((bcf_in.header.info)))
   ['NS', 'DP', 'AF', 'AA', 'DB', 'H2']
   >>> print(list((bcf_in.header.samples)))
   ['NA00001', 'NA00002', 'NA00003']

Alternatively, it is possible to iterate through all records in the
header returning objects of type :py:class:`~fabric.VariantHeaderRecord`:: ::

   >>> for x in bcf_in.header.records:
   >>>    print(x)
   >>>    print(x.type, x.key)
   GENERIC fileformat
   FILTER FILTER
   GENERIC fileDate
   GENERIC source
   GENERIC reference
   GENERIC phasing
   INFO INFO
   INFO INFO
   INFO INFO
   INFO INFO
   INFO INFO
   INFO INFO
   FILTER FILTER
   FILTER FILTER
   FORMAT FORMAT
   FORMAT FORMAT
   FORMAT FORMAT
   FORMAT FORMAT
   CONTIG contig
   CONTIG contig
   CONTIG contig
   GENERIC bcftools_viewVersion
   GENERIC bcftools_viewCommand

===============
Extending fabric
===============

Using pyximport_, it is (relatively) straight-forward to access fabric
internals and the underlying `samtools`_ library. An example is provided
in the :file:`tests` directory. The example emulates the samtools
flagstat command and consists of three files:

1. The main script :file:`fabric_flagstat.py`. The important lines in
   this script are::

      import pyximport
      pyximport.install()
      import _fabric_flagstat

      ...
   
      flag_counts = _fabric_flagstat.count(fabric_in)

   The first part imports, sets up pyximport_ and imports the cython
   module :file:`_fabric_flagstat`.  The second part calls the
   ``count`` method in :file:`_fabric_flagstat`.
 
2. The cython implementation :file:`_fabric_flagstat.pyx`. This script
   imports the fabric API via::

      from fabric.libcalignmentfile cimport AlignmentFile, AlignedSegment

   This statement imports, amongst others, :class:`AlignedSegment`
   into the namespace. Speed can be gained from declaring
   variables. For example, to efficiently iterate over a file, an
   :class:`AlignedSegment` object is declared::

      # loop over samfile
      cdef AlignedSegment read
      for read in samfile:
          ...

3. A :file:`pyxbld` providing pyximport_ with build information.
   Required are the locations of the samtools and fabric header
   libraries of a source installation of fabric plus the
   :file:`csamtools.so` shared library. For example::

     def make_ext(modname, pyxfilename):
	 from distutils.extension import Extension
	 import fabric
	 return Extension(name=modname,
               sources=[pyxfilename],
               extra_link_args=fabric.get_libraries(),
	       include_dirs=fabric.get_include(),
	       define_macros=fabric.get_defines())

If the script :file:`fabric_flagstat.py` is called the first time,
pyximport_ will compile the cython_ extension
:file:`_fabric_flagstat.pyx` and make it available to the
script. Compilation requires a working compiler and cython_
installation.  Each time :file:`_fabric_flagstat.pyx` is modified, a
new compilation will take place.

pyximport_ comes with cython_.

