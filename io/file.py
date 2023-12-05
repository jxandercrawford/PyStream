from stream import Stream, Pipe


def yield_lines(path: str):
    """
    Will open a file and read the lines as a generator.
    :param str path: The path to the file to open.
    :return: A generator of the file lines.
    """
    with open(path, "r") as fp:
        for line in fp:
            yield line


def file_writer(path: str, mode: str = "w"):
    """
    Opens a file and operates as a generator for writing files.
    :param str path: The path of the file to write to.
    :param str mode: The mode to open the file in. Defaults to "w".
    :return: A generator for writing files.
    """
    with open(path, mode) as fp:
        while True:
            content = yield
            fp.write(content)
            yield content


def stream_file(path: str):
    """
    Open a file as a Stream reading each line of the file.
    :param str path: The path to the file to open.
    :return: A Stream of the file lines.
    """
    return Stream(yield_lines(path))


def pipe_file(path: str, mode: str = "w"):
    """
    Opens a pipe to write a file.
    :param str path: The path of the file to write to.
    :param str mode: The mode to open the file in. Defaults to "w".
    :return: A Pipe for writing to a file.
    """
    writer = file_writer(path, mode)
    next(writer)

    def run_writer(content: str):
        """
        Helper function to properly run the file_write() generator.
        :param str content: The content to pass to the writer.
        :return: The content writen by the file_write() generator.
        """
        writer.send(content)
        return next(writer)

    return Pipe().through(run_writer)
