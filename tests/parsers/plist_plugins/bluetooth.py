#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the MacOS Bluetooth plist plugin."""

import unittest

from plaso.parsers.plist_plugins import bluetooth

from tests.parsers.plist_plugins import test_lib


class MacOSBluetoothPlistPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the MacOS Bluetooth plist plugin."""

  def testProcess(self):
    """Tests the Process function."""
    plugin = bluetooth.MacOSBluetoothPlistPlugin()
    storage_writer = self._ParsePlistFileWithPlugin(
        plugin, ['plist_binary'], 'com.apple.bluetooth.plist')

    number_of_events = storage_writer.GetNumberOfAttributeContainers('event')
    self.assertEqual(number_of_events, 12)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    # The order in which PlistParser generates events is nondeterministic
    # hence we sort the events.
    events = list(storage_writer.GetSortedEvents())

    expected_event_values = {
        'data_type': 'macos:bluetooth:entry',
        'date_time': '2012-11-02T01:13:17.324095+00:00',
        'device_identifier': '44-00-00-00-00-04',
        'device_name': 'Apple Magic Trackpad 2',
        'is_paired': True,
        'timestamp_desc': 'Last Inquiry Update Time'}

    self.CheckEventValues(storage_writer, events[8], expected_event_values)


if __name__ == '__main__':
  unittest.main()
