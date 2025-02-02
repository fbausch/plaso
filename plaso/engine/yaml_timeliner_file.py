# -*- coding: utf-8 -*-
"""YAML-based timeliner configuration file."""

import yaml

from plaso.lib import errors


class TimelinerDefinition(object):
  """Timeliner definition.

  Attributes:
    attribute_mappings (dict[str, str]): data and time description
        (timestamp_desc) per attribute name.
    data_type (str): event data type indicator.
  """

  def __init__(self, data_type):
    """Initializes a timeliner definition.

    Args:
      data_type (str): event data type indicator.
    """
    super(TimelinerDefinition, self).__init__()
    self.attribute_mappings = {}
    self.data_type = data_type


class YAMLTimelinerConfigurationFile(object):
  """YAML-based timeliner configuration file.

  A YAML-based timeliner configuration file contains one or more timeliner
  definitions. A timeliner definitions consists of:

  data_type: 'fs:stat'
  attribute_mappings:
  - name: 'access_time'
    description: 'Last Access Time'

  Where:
  * data_type, defines the corresponding event data type;
  * attribute_mappings, defines attribute mappings.
  """

  _SUPPORTED_KEYS = frozenset([
      'attribute_mappings',
      'data_type'])

  def _ReadTimelinerDefinition(self, timeliner_definition_values):
    """Reads a timeliner definition from a dictionary.

    Args:
      timeliner_definition_values (dict[str, object]): timeliner definition
           values.

    Returns:
      TimelinerDefinition: a timeliner definition.

    Raises:
      ParseError: if the format of the timeliner definition is not set
          or incorrect.
    """
    if not timeliner_definition_values:
      raise errors.ParseError('Missing timeliner definition values.')

    different_keys = set(timeliner_definition_values) - self._SUPPORTED_KEYS
    if different_keys:
      different_keys = ', '.join(different_keys)
      raise errors.ParseError('Undefined keys: {0:s}'.format(different_keys))

    data_type = timeliner_definition_values.get('data_type', None)
    if not data_type:
      raise errors.ParseError(
          'Invalid event timeliner definition missing data type.')

    attribute_mappings = timeliner_definition_values.get(
        'attribute_mappings', None)
    if not attribute_mappings:
      raise errors.ParseError(
          'Invalid event timeliner definition: {0:s} missing source.'.format(
              data_type))

    timeliner_definition = TimelinerDefinition(data_type)
    timeliner_definition.attribute_mappings = {
        attribute_mapping['name']: attribute_mapping['description']
        for attribute_mapping in attribute_mappings}

    return timeliner_definition

  def _ReadFromFileObject(self, file_object):
    """Reads the timeliner definitions from a file-like object.

    Args:
      file_object (file): timeliner definitions file-like object.

    Yields:
      TimelinerDefinition: a timeliner definition.
    """
    yaml_generator = yaml.safe_load_all(file_object)

    for yaml_definition in yaml_generator:
      yield self._ReadTimelinerDefinition(yaml_definition)

  def ReadFromFile(self, path):
    """Reads the timeliner definitions from a YAML file.

    Args:
      path (str): path to a timeliner configuration file.

    Yields:
      TimelinerDefinition: a timeliner definition.
    """
    with open(path, 'r', encoding='utf-8') as file_object:
      for yaml_definition in self._ReadFromFileObject(file_object):
        yield yaml_definition
