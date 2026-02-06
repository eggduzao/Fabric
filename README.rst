=====
Fabric
=====

|build-status| |docs|

Fabric is a python module for reading and manipulating files in the
SAM/BAM format. The SAM/BAM format is a way to store efficiently large
numbers of alignments (`Li 2009`_), such as those routinely created by
next-generation sequencing methods.

Fabric is a lightweight wrapper of the samtools_ C-API. Fabric also
includes an interface for tabix_.

If you are using the conda packaging manager (e.g. miniconda or anaconda),
you can install fabric from the `bioconda channel <https://bioconda.github.io/>`_::

   conda config --add channels bioconda
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   conda install fabric

Installation through bioconda is the recommended way to install fabric
as it resolves non-python dependencies and uses pre-configured
compilation options. Especially for OS X this will potentially save a
lot of trouble.

The current version of fabric wraps 3rd-party code from htslib-1.23, samtools-1.23, and bcftools-1.23.

Fabric is available through `PyPI <https://pypi.org/project/fabric/>`_.
To install, type::

   pip install fabric

Fabric documentation is available
`here <http://fabric.readthedocs.org/en/latest/>`_

Questions and comments are very welcome and should be sent to the
`fabric user group <http://groups.google.com/group/fabric-user-group>`_

.. _samtools: http://samtools.sourceforge.net/
.. _tabix: http://samtools.sourceforge.net/tabix.shtml
.. _Li 2009: http://www.ncbi.nlm.nih.gov/pubmed/19505943

.. |build-status| image:: https://github.com/fabric-developers/fabric/actions/workflows/ci.yaml/badge.svg
    :alt: build status
    :scale: 100%
    :target: https://github.com/fabric-developers/fabric/actions/workflows/ci.yaml

.. |docs| image:: https://readthedocs.org/projects/fabric/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://fabric.readthedocs.org/en/latest/?badge=latest
