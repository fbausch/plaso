#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the vsftpd text parser plugin."""

import unittest

from plaso.parsers.text_plugins import vsftpd

from tests.parsers.text_plugins import test_lib


class VsftpdLogTextPluginText(test_lib.TextPluginTestCase):
  """Tests for the vsftpd text parser plugin."""

  def testProcess(self):
    """Tests the Process function."""
    plugin = vsftpd.VsftpdLogTextPlugin()
    storage_writer = self._ParseTextFileWithPlugin(['vsftpd.log'], plugin)

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 25)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    # TODO: sort events.
    # events = list(storage_writer.GetSortedEvents())

    events = list(storage_writer.GetEvents())

    expected_event_values = {
        'data_type': 'vsftpd:log',
        'date_time': '2016-06-10T14:24:19',
        'text': (
            '[pid 3] [jean] OK DOWNLOAD: Client "192.168.1.7", '
            '"/home/jean/trains/how-thomas-the-tank-engine-works-1.jpg", '
            '49283 bytes, 931.38Kbyte/sec'),
        'timestamp': '2016-06-10 14:24:19.000000'}

    self.CheckEventValues(storage_writer, events[12], expected_event_values)

  def testProcessWithTimeZone(self):
    """Tests the Process function with a time zone."""
    plugin = vsftpd.VsftpdLogTextPlugin()
    storage_writer = self._ParseTextFileWithPlugin(
        ['vsftpd.log'], plugin, time_zone_string='CET')

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 25)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    # TODO: sort events.
    # events = list(storage_writer.GetSortedEvents())

    events = list(storage_writer.GetEvents())

    expected_event_values = {
        'data_type': 'vsftpd:log',
        'date_time': '2016-06-10T14:24:19',
        'text': (
            '[pid 3] [jean] OK DOWNLOAD: Client "192.168.1.7", '
            '"/home/jean/trains/how-thomas-the-tank-engine-works-1.jpg", '
            '49283 bytes, 931.38Kbyte/sec'),
        'timestamp': '2016-06-10 12:24:19.000000'}

    self.CheckEventValues(storage_writer, events[12], expected_event_values)


if __name__ == '__main__':
  unittest.main()
