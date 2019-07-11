# import os
from unittest import mock
import inspect
# from tempfile import TemporaryDirectory, NamedTemporaryFile

from terra import settings
from terra.compute.utils import compute, ComputeHandler, Handler
import terra.compute.dummy as dummy
from terra.core.utils import cached_property

from .utils import TestCase


class TestHandler(TestCase):
  def test_handler(self):
    handle = Handler()
    handle.real
    self.assertIsNotNone(handle._connection)

  @mock.patch.object(settings, '_wrapped', None)
  def test_compute_handler(self):
    settings.configure({'compute': {'arch': 'terra.compute.dummy'}})

    test_compute = ComputeHandler()

    self.assertTrue(inspect.ismethod(test_compute.run))
    self.assertIsNotNone(test_compute._connection)
    self.assertIsInstance(test_compute._connection, dummy.Compute)

  # Make sure this can be run twice
  test_compute_handler2 = test_compute_handler
