from __future__ import absolute_import

from fabric.libchtslib         cimport bam1_t, bam_endpos
from fabric.libcsamfile        cimport aux_type2size
from fabric.libcalignedsegment cimport AlignedSegment

import fabric


cpdef build_read():
    cdef AlignedSegment read = fabric.AlignedSegment()
    read.query_name = "hello"
    read.query_sequence = "ACGT"
    read.reference_start = 10
    read.cigarstring = "4M"

    # Test calling htslib function
    cdef bam1_t *calign = read._delegate
    print(bam_endpos(calign))

    # Test calling fabric htslib_util function
    print(aux_type2size(12))

    return read
