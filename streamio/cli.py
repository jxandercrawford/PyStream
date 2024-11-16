import sys

from stream import Pipe, Stream


def yield_input():
    """
    Open the stdin and read lines to as a generator. Dies at EOF.
    :return: A generator taking in the stdin.
    """
    while 1:
        try:
            content = input()
        except EOFError:
            break
        except Exception as e:
            raise e

        yield content


def stream_stdin() -> Stream:
    """
    Open the stdin and read lines to a Stream. Dies at EOF.
    :return: A stream taking in the stdin.
    """
    return Stream(yield_input())


def pipe_stdout() -> Pipe:
    """
    Opens a pipe that writes to stdout.
    :return: A pipe to stdout.
    """
    return Pipe().through(lambda x: print(x, file=sys.stdout))


def pipe_stderr() -> Pipe:
    """
    Opens a pipe that writes to stderr.
    :return: A pipe to stderr.
    """
    return Pipe().through(lambda x: print(x, file=sys.stderr))
