#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the McAfee AV Log parser."""

import unittest

from plaso.parsers import mcafeeav

from tests.parsers import test_lib


class McafeeAccessProtectionUnitTest(test_lib.ParserTestCase):
  """Tests for the McAfee AV Log parser."""

  def testParse(self):
    """Tests the Parse function."""
    parser = mcafeeav.McafeeAccessProtectionParser()
    storage_writer = self._ParseFile(['AccessProtectionLog.txt'], parser)

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 14)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    # The order in which DSVParser generates events is nondeterministic
    # hence we sort the events.
    events = list(storage_writer.GetSortedEvents())

    expected_event_values = {
        'data_type': 'av:mcafee:accessprotectionlog',
        'date_time': '2013-09-27T14:42:26'}

    self.CheckEventValues(storage_writer, events[10], expected_event_values)

    # TODO: Test that the UTF-8 byte order mark gets removed from
    # the first line.

    # Test this entry:
    # 9/27/2013 2:42:26 PM  Blocked by Access Protection rule
    #   SOMEDOMAIN\someUser C:\Windows\System32\procexp64.exe C:\Program Files
    # (x86)\McAfee\Common Framework\UdaterUI.exe  Common Standard
    # Protection:Prevent termination of McAfee processes  Action blocked :
    # Terminate

    expected_event_values = {
        'action': 'Action blocked : Terminate',
        'data_type': 'av:mcafee:accessprotectionlog',
        'date_time': '2013-09-27T14:42:39',
        'filename': 'C:\\Windows\\System32\\procexp64.exe',
        'rule': (
            'Common Standard Protection:Prevent termination of McAfee '
            'processes'),
        'status': 'Blocked by Access Protection rule',
        'timestamp': '2013-09-27 14:42:39.000000',
        'trigger_location': (
            'C:\\Program Files (x86)\\McAfee\\Common Framework\\Frame'
            'workService.exe'),
        'username': 'SOMEDOMAIN\\someUser'}

    self.CheckEventValues(storage_writer, events[11], expected_event_values)

  def testParseWithTimeZone(self):
    """Tests the Parse function with a time zone."""
    parser = mcafeeav.McafeeAccessProtectionParser()
    storage_writer = self._ParseFile(
        ['AccessProtectionLog.txt'], parser, time_zone_string='CET')

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 14)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    # The order in which DSVParser generates events is nondeterministic
    # hence we sort the events.
    events = list(storage_writer.GetSortedEvents())

    # Test this entry:
    # 9/27/2013 2:42:26 PM  Blocked by Access Protection rule
    #   SOMEDOMAIN\someUser C:\Windows\System32\procexp64.exe C:\Program Files
    # (x86)\McAfee\Common Framework\UdaterUI.exe  Common Standard
    # Protection:Prevent termination of McAfee processes  Action blocked :
    # Terminate

    expected_event_values = {
        'action': 'Action blocked : Terminate',
        'data_type': 'av:mcafee:accessprotectionlog',
        'date_time': '2013-09-27T14:42:39',
        'filename': 'C:\\Windows\\System32\\procexp64.exe',
        'rule': (
            'Common Standard Protection:Prevent termination of McAfee '
            'processes'),
        'status': 'Blocked by Access Protection rule',
        'timestamp': '2013-09-27 12:42:39.000000',
        'trigger_location': (
            'C:\\Program Files (x86)\\McAfee\\Common Framework\\Frame'
            'workService.exe'),
        'username': 'SOMEDOMAIN\\someUser'}

    self.CheckEventValues(storage_writer, events[11], expected_event_values)


if __name__ == '__main__':
  unittest.main()
