import re
import os
from typing import List, Iterable, Union, TextIO

from reader.file_reader import FileReader

class TextReader(FileReader):
    def __init__(self,
                 line_delim: str = os.linesep,
                 word_delim: str = " ",
                 lazy: bool = True,
                 keep_blank: bool = False,
                 strip: bool = True,
                 squeeze: int = 1) -> None:
        self.reset(line_delim=line_delim,
                   word_delim=word_delim,
                   lazy=lazy,
                   keep_blank=keep_blank,
                   strip=strip,
                   squeeze=squeeze)

    def reset(self,
              line_delim: str = os.linesep,
              word_delim: str = " ",
              lazy: bool = True,
              keep_blank: bool = False,
              strip: bool = True,
              squeeze: int = 1) -> None:
        self._line_delim = line_delim
        self._word_delim = word_delim
        self._lazy = lazy
        self._keep_blank = keep_blank

        self._strip = strip
        if self._strip:
            self._strip_target = self._word_delim + "|" + self._line_delim

        self._squeeze = squeeze
        if self._squeeze > -1:
            self._squeeze_target = re.compile(self._word_delim + "+")
            self._squeeze_goal = self._word_delim * self._squeeze

    def read(self, path: str) -> str:
        file = open(path)
        text = file.read()
        file.close()
        return self.format(text)

    def read_lines(self, path: str) -> Union[Iterable, List]:
        file = open(path, newline=self._line_delim)
        if self._lazy:
            return self._read_lines_lazy(file)
        else:
            return self._read_lines_std(file)

    def _read_lines_lazy(self, file: TextIO) -> Iterable:
        line = file.readline()
        while line:
            if line != self._line_delim or self._keep_blank:
                yield self.format(line)
            line = file.readline()
        file.close()

    def _read_lines_std(self, file: TextIO) -> List:
        lines = []
        line = file.readline()
        while line:
            if line != self._line_delim or self._keep_blank:
                lines.append(self.format(line))
            line = file.readline()
        file.close()
        return lines

    def read_words(self, path: str) -> Union[Iterable, List]:
        file = open(path, newline=self._line_delim)
        if self._lazy:
            return self._read_words_lazy(file)
        else:
            return self._read_words_std(file)

    def _read_words_lazy(self, file: TextIO) -> Iterable:
        line = file.readline()
        while line:
            if line != self._line_delim or self._keep_blank:
                for word in line.split(self._word_delim):
                    if word != "":
                        yield self.format(word)
            line = file.readline()
        file.close()

    def _read_words_std(self, file: TextIO) -> List:
        words = []
        line = file.readline()
        while line:
            if line != self._line_delim or self._keep_blank:
                for word in line.split(self._word_delim):
                    if word != "":
                        words.append(self.format(word))
            line = file.readline()
        file.close()
        return words

    def format(self, text: str) -> str:
        if self._squeeze:
            text = re.sub(self._squeeze_target, self._squeeze_goal, text)
        if self._strip:
            text = text.strip(self._strip_target)
        return text
