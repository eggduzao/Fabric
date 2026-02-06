# cython: language_level=3
from fabric.libcalignmentfile cimport AlignedSegment, AlignmentFile

#################################################
# Compatibility Layer for fabric < 0.8

# import all declarations from htslib
from fabric.libchtslib cimport *

cdef class AlignedRead(AlignedSegment):
    pass

cdef class Samfile(AlignmentFile):
    pass

# import the conversion functions
cdef extern from "htslib_util.h":

    # add *nbytes* into the variable length data of *src* at *pos*
    bam1_t * fabric_bam_update(bam1_t * b,
                              size_t nbytes_old,
                              size_t nbytes_new,
                              uint8_t * pos)

    # now: static
    int aux_type2size(int)

    char * fabric_bam_get_qname(bam1_t * b)
    uint32_t * fabric_bam_get_cigar(bam1_t * b)
    uint8_t * fabric_bam_get_seq(bam1_t * b)
    uint8_t * fabric_bam_get_qual(bam1_t * b)
    uint8_t * fabric_bam_get_aux(bam1_t * b)
    int fabric_bam_get_l_aux(bam1_t * b)
    char fabric_bam_seqi(uint8_t * s, int i)

    uint16_t fabric_get_bin(bam1_t * b)
    uint8_t fabric_get_qual(bam1_t * b)
    uint8_t fabric_get_l_qname(bam1_t * b)
    uint16_t fabric_get_flag(bam1_t * b)
    uint32_t fabric_get_n_cigar(bam1_t * b)
    void fabric_set_bin(bam1_t * b, uint16_t v)
    void fabric_set_qual(bam1_t * b, uint8_t v)
    void fabric_set_l_qname(bam1_t * b, uint8_t v)
    void fabric_set_flag(bam1_t * b, uint16_t v)
    void fabric_set_n_cigar(bam1_t * b, uint32_t v)
    void fabric_update_flag(bam1_t * b, uint16_t v, uint16_t flag)
