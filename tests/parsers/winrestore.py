#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the Windows Restore Point (rp.log) file parser."""

import unittest

from plaso.lib import definitions
from plaso.parsers import winrestore

from tests.parsers import test_lib


class RestorePointLogParserTest(test_lib.ParserTestCase):
  """Tests for the Windows Restore Point (rp.log) file parser."""

  def testParse(self):
    """Tests the Parse function."""
    parser = winrestore.RestorePointLogParser()
    storage_writer = self._ParseFile(['rp.log'], parser)

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 1)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    events = list(storage_writer.GetEvents())

    expected_event_values = {
        'data_type': 'windows:restore_point:info',
        'date_time': '2015-03-23T18:38:14.2469544+00:00',
        'description': 'Software Distribution Service 3.0',
        'restore_point_event_type': 102,
        'restore_point_type': 0,
        'timestamp_desc': definitions.TIME_DESCRIPTION_CREATION}

    self.CheckEventValues(storage_writer, events[0], expected_event_values)


if __name__ == '__main__':
  unittest.main()
