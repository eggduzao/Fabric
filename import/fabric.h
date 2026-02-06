#ifndef @fabric@_FABRIC_H
#define @fabric@_FABRIC_H

#include <stdio.h>

#ifndef __has_attribute
#define __has_attribute(attribute) 0
#endif
#ifndef FABRIC_NORETURN
#if __has_attribute(__noreturn__) || __GNUC__ >= 3
#define FABRIC_NORETURN __attribute__((__noreturn__))
#else
#define FABRIC_NORETURN
#endif
#endif

extern FILE * @fabric@_stderr;

extern FILE * @fabric@_stdout;

extern const char * @fabric@_stdout_fn;

/*! set fabric standard error to point to file descriptor

  Setting the stderr will close the previous stderr.
 */
FILE * @fabric@_set_stderr(int fd);

/*! set fabric standard output to point to file descriptor

  Setting the stdout will close the previous stdout.
 */
FILE * @fabric@_set_stdout(int fd);

/*! set fabric standard output to point to filename

 */
void @fabric@_set_stdout_fn(const char * fn);

/*! close fabric standard error and set to NULL
  
 */
void @fabric@_close_stderr(void);

/*! close fabric standard output and set to NULL
  
 */
void @fabric@_close_stdout(void);

int @fabric@_puts(const char *s);

int @fabric@_dispatch(int argc, char *argv[]);

void FABRIC_NORETURN @fabric@_exit(int status);

extern int @fabric@_main(int argc, char *argv[]);

/* Define these only in samtools/bcftools C source, not Cython code. */
#if !(defined CYTHON_ABI || defined CYTHON_HEX_VERSION)

/*! Several non-static function names are used in both samtools and bcftools.
    Both libcsamtools.so and libcbcftools.so are loaded simultaneously, leading
    to collisions and wrong functions being called. #define these names so the
    actual symbol names include distinct prefixes to avoid collisions.
 */
#define main_consensus @fabric@_main_consensus
#define main_reheader @fabric@_main_reheader
#define bam_smpl_init @fabric@_bam_smpl_init
#define bam_smpl_destroy @fabric@_bam_smpl_destroy
#define read_file_list @fabric@_read_file_list

/*! A non-static error() function name is used in bcftools, which collides
    with glibc's error() function and leads to the wrong function being called
    on some platforms. #define this name with a prefix to avoid this collision.
 */
#define error @fabric@_error

#endif

#endif
