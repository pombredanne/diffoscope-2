# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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

from io import StringIO
import pytest
from diffoscope.config import Config
from diffoscope.difference import Difference

def test_too_much_input_for_diff(monkeypatch):
    monkeypatch.setattr(Config, 'max_diff_input_lines', 20)
    too_long_text_a = StringIO("a\n" * 21)
    too_long_text_b = StringIO("b\n" * 21)
    difference = Difference.from_text_readers(too_long_text_a, too_long_text_b, 'a', 'b')
    assert '[ Too much input for diff ]' in difference.unified_diff 

def test_too_long_diff_block_lines(monkeypatch):
    monkeypatch.setattr(Config, 'max_diff_block_lines', 10)
    too_long_text_a = StringIO("a\n" * 21)
    too_long_text_b = StringIO("b\n" * 21)
    difference = Difference.from_text_readers(too_long_text_a, too_long_text_b, 'a', 'b')
    assert '[ 11 lines removed ]' in difference.unified_diff
