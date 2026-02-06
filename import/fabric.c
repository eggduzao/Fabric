#include <getopt.h>
#include <unistd.h>
#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "@fabric@.fabric.h"

FILE * @fabric@_stderr = NULL;
FILE * @fabric@_stdout = NULL;
const char * @fabric@_stdout_fn = NULL;


FILE * @fabric@_set_stderr(int fd)
{
  if (@fabric@_stderr != NULL)
    fclose(@fabric@_stderr);
  @fabric@_stderr = fdopen(fd, "w");
  return @fabric@_stderr;
}

void @fabric@_close_stderr(void)
{
  fclose(@fabric@_stderr);
  @fabric@_stderr = NULL;
}

FILE * @fabric@_set_stdout(int fd)
{
  if (@fabric@_stdout != NULL)
    fclose(@fabric@_stdout);
  @fabric@_stdout = fdopen(fd, "w");
  if (@fabric@_stdout == NULL)
    {
      fprintf(@fabric@_stderr, "could not set stdout to fd %i", fd);
    }
  return @fabric@_stdout;
}

void @fabric@_set_stdout_fn(const char *fn)
{
  @fabric@_stdout_fn = fn;
}

void @fabric@_close_stdout(void)
{
  fclose(@fabric@_stdout);
  @fabric@_stdout = NULL;
}

int @fabric@_puts(const char *s)
{
  if (fputs(s, @fabric@_stdout) == EOF) return EOF;
  return putc('\n', @fabric@_stdout);
}


static jmp_buf @fabric@_jmpbuf;
static int @fabric@_status = 0;

int @fabric@_dispatch(int argc, char *argv[])
{
  /* Reset getopt()/getopt_long() processing. */
#if defined __GLIBC__
  optind = 0;
#elif defined _OPTRESET || defined _OPTRESET_DECLARED
  optreset = optind = 1;
#else
  optind = 1;
#endif

  if (setjmp(@fabric@_jmpbuf) == 0)
    return @fabric@_main(argc, argv);
  else
    return @fabric@_status;
}

void @fabric@_exit(int status)
{
  @fabric@_status = status;
  longjmp(@fabric@_jmpbuf, 1);
}
