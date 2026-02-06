============
Introduction
============

Fabric is a python module that makes it easy to read and manipulate
mapped short read sequence data stored in SAM/BAM files.  It is a
lightweight wrapper of the htslib_ C-API.

This page provides a quick introduction in using fabric followed by the
API. See :ref:`usage` for more detailed usage instructions.

To use the module to read a file in BAM format, create a
:class:`~fabric.AlignmentFile` object::

   import fabric
   samfile = fabric.AlignmentFile("ex1.bam", "rb")

Once a file is opened you can iterate over all of the reads mapping to
a specified region using :meth:`~fabric.AlignmentFile.fetch`.  Each
iteration returns a :class:`~fabric.AlignedSegment` object which
represents a single read along with its fields and optional tags::

   for read in samfile.fetch('chr1', 100, 120):
       print(read)

   samfile.close()

To give::

    EAS56_57:6:190:289:82	0	99	<<<7<<<;<<<<<<<<8;;<7;4<;<;;;;;94<;	69	CTCAAGGTTGTTGCAAGGGGGTCTATGTGAACAAA	0	192	1
    EAS56_57:6:190:289:82	0	99	<<<<<<;<<<<<<<<<<;<<;<<<<;8<6;9;;2;	137	AGGGGTGCAGAGCCGAGTCACGGGGTTGCCAGCAC	73	64	1
    EAS51_64:3:190:727:308	0	102	<<<<<<<<<<<<<<<<<<<<<<<<<<<::<<<844	99	GGTGCAGAGCCGAGTCACGGGGTTGCCAGCACAGG	99	18	1
    ...

You can also write to a :class:`~fabric.AlignmentFile`::

   import fabric
   samfile = fabric.AlignmentFile("ex1.bam", "rb")
   pairedreads = fabric.AlignmentFile("allpaired.bam", "wb", template=samfile)
   for read in samfile.fetch():
       if read.is_paired:
           pairedreads.write(read)

   pairedreads.close()
   samfile.close()

An alternative way of accessing the data in a SAM file is by iterating
over each base of a specified region using the
:meth:`~fabric.AlignmentFile.pileup` method. Each iteration returns a
:class:`~fabric.PileupColumn` which represents all the reads in the SAM
file that map to a single base in the reference sequence. The list of
reads are represented as :class:`~fabric.PileupRead` objects in the
:attr:`PileupColumn.pileups <fabric.PileupColumn.pileups>` property::

    import fabric
    samfile = fabric.AlignmentFile("ex1.bam", "rb" )
    for pileupcolumn in samfile.pileup("chr1", 100, 120):
        print("\ncoverage at base %s = %s" % (pileupcolumn.pos, pileupcolumn.n))
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                # query position is None if is_del or is_refskip is set.
                print('\tbase in read %s = %s' %
                      (pileupread.alignment.query_name,
                       pileupread.alignment.query_sequence[pileupread.query_position]))

    samfile.close()

The above code outputs::

    coverage at base 99 = 1
        base in read EAS56_57:6:190:289:82 = A

    coverage at base 100 = 1
        base in read EAS56_57:6:190:289:82 = G

    coverage at base 101 = 1
        base in read EAS56_57:6:190:289:82 = G

    coverage at base 102 = 2
        base in read EAS56_57:6:190:289:82 = G
        base in read EAS51_64:3:190:727:308 = G
    ...

Commands available in `samtools`_ are available as simple
function calls. For example::

   fabric.sort("-o", "output.bam", "ex1.bam")

corresponds to the command line::

   samtools sort -o output.bam ex1.bam 

Analogous to :class:`~fabric.AlignmentFile`, a
:class:`~fabric.TabixFile` allows fast random access to compressed and
tabix indexed tab-separated file formats with genomic data::

   import fabric
   tabixfile = fabric.TabixFile("example.gtf.gz")

   for gtf in tabixfile.fetch("chr1", 1000, 2000):
       print(gtf.contig, gtf.start, gtf.end, gtf.gene_id)

:class:`~fabric.TabixFile` implements lazy parsing in order to iterate
over large tables efficiently.

More detailed usage instructions are available at :ref:`usage`.

.. note::

   Coordinates in fabric are always 0-based (following the python
   convention). SAM text files use 1-based coordinates.

.. note::

   The above examples can be run in the :file:`tests` directory of the
    installation directory. Type 'make' before running them.

.. seealso::

   https://github.com/fabric-developers/fabric

       The fabric code repository, containing source code and download
       instructions

   http://fabric.readthedocs.org/en/latest/

       The fabric website containing documentation

===
API
===

SAM/BAM/CRAM files
==================

Objects of type :class:`~fabric.AlignmentFile` allow working with
BAM/SAM formatted files.

.. autoclass:: fabric.AlignmentFile
   :members:

.. autoclass:: fabric.AlignmentHeader
   :members:

An :class:`~fabric.AlignedSegment` represents an aligned segment within
a SAM/BAM file.

.. autoclass:: fabric.AlignedSegment
   :members:

.. autoclass:: fabric.PileupColumn
   :members:

.. autoclass:: fabric.PileupRead
   :members:

.. autoclass:: fabric.IndexedReads
   :members:


Tabix files
===========

:class:`~fabric.TabixFile` opens tabular files that have been
indexed with tabix_.

.. autoclass:: fabric.TabixFile
   :members:

To iterate over tabix files, use :func:`~fabric.tabix_iterator`:

.. autofunction:: fabric.tabix_iterator

.. autofunction:: fabric.tabix_compress

.. autofunction:: fabric.tabix_index

.. autoclass:: fabric.asTuple
   :members:

.. autoclass:: fabric.asVCF
   :members:

.. autoclass:: fabric.asBed
   :members:

.. autoclass:: fabric.asGTF
   :members:


FASTA files
===========

.. autoclass:: fabric.FastaFile
   :members:

FASTQ files
===========

.. autoclass:: fabric.FastxFile
   :members:

.. autoclass:: fabric.FastqProxy
   :members:


VCF/BCF files
=============

.. autoclass:: fabric.VariantFile
   :members:

.. autoclass:: fabric.VariantHeader
   :members:

.. autoclass:: fabric.VariantHeaderRecord
   :members:

.. autoclass:: fabric.VariantRecord
   :members:

HTSFile
=======

HTSFile is the base class for :class:`fabric.AlignmentFile` and
:class:`fabric.VariantFile`.

.. autoclass:: fabric.HTSFile
   :members:
