# cython: language_level=3

from fabric.libcalignmentfile cimport AlignmentFile, AlignedSegment
from fabric.libcalignmentfile cimport BAM_FPROPER_PAIR, BAM_FPAIRED
from fabric.libcalignedsegment cimport fabric_get_flag

def count(AlignmentFile samfile):
    cdef int is_proper = 0
    cdef int is_paired = 0
    cdef AlignedSegment read
    cdef int f

    for read in samfile:
        f = fabric_get_flag(read._delegate)
        if f & BAM_FPAIRED:
            is_paired += 1
        if f & BAM_FPROPER_PAIR:
            is_proper += 1

    return is_paired, is_proper
