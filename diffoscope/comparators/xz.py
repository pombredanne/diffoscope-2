# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2014-2015 Jérémy Bobbio <lunar@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import os.path
import re
import subprocess
import diffoscope.comparators
from diffoscope import tool_required
from diffoscope.comparators.binary import File, needs_content
from diffoscope.comparators.utils import Archive, get_compressed_content_name
from diffoscope import logger, tool_required


class XzContainer(Archive):
    @property
    def path(self):
        return self._path

    def open_archive(self, path):
        self._path = path
        return self

    def close_archive(self):
        self._path = None

    def get_member_names(self):
        return [get_compressed_content_name(self.path, '.xz')]

    @tool_required('xz')
    def extract(self, member_name, dest_dir):
        dest_path = os.path.join(dest_dir, member_name)
        logger.debug('xz extracting to %s' % dest_path)
        with open(dest_path, 'wb') as fp:
            subprocess.check_call(
                ["xz", "--decompress", "--stdout", self.path],
                shell=False, stdout=fp, stderr=None)
        return dest_path

    def compare(self, other, source=None):
        my_file = self.get_member(self.get_member_names()[0])
        other_file = other.get_member(other.get_member_names()[0])
        source = None
        if my_file.name == other_file.name:
            source = my_file.name
        return [diffoscope.comparators.compare_files(my_file, other_file, source)]


class XzFile(File):
    RE_FILE_TYPE = re.compile(r'^XZ compressed data$')

    @staticmethod
    def recognizes(file):
        return XzFile.RE_FILE_TYPE.match(file.magic_file_type)

    @needs_content
    def compare_details(self, other, source=None):
        with XzContainer(self).open() as my_container, \
             XzContainer(other).open() as other_container:
            return my_container.compare(other_container, source)