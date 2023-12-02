import sys
from stream import Stream, Pipe


def stream_stdin():
    """
    Open the stdin and read lines to a Stream.
    :return: A stream taking in the stdin.
    """

    def get_input():
        while 1:
            try:
                content = input()
            except EOFError:
                break
            except Exception as e:
                raise e

            yield content

    return Stream(get_input())


def pipe_stdout():
    """
    Opens a pipe that writes to stdout.
    :return: A pipe to stdout.
    """
    return Pipe().through(lambda x: print(x, file=sys.stdout))


def pipe_stderr():
    """
    Opens a pipe that writes to stderr.
    :return: A pipe to stderr.
    """
    return Pipe().through(lambda x: print(x, file=sys.stderr))


if __name__ == "__main__":
    source = stream_stdin()
    print("Enter 2 for STDERR: ", end="")
    if next(source) == "2":
        sink = Pipe().through(lambda x: "STDERR> " + x).through(pipe_stderr())
    else:
        sink = Pipe().through(lambda x: "STDOUT> " + x).through(pipe_stdout())
    source.through(sink).drain()

