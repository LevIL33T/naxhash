from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from unittest import main, TestCase

import naxhash.settings
import tests


class TestUserData(TestCase):

    def setUp(self):
        self.testdir = Path(mkdtemp())
        self.settings = naxhash.settings.DEFAULT_SETTINGS
        self.devices = tests.get_test_devices()
        self.benchmarks = tests.get_test_benchmarks()

    def tearDown(self):
        rmtree(self.testdir)

    def test_settings(self):
        testfile = self.testdir/'settings.conf'
        with open(testfile, 'w') as fd:
            naxhash.settings.write_settings_to_file(fd, self.settings)
        with open(testfile, 'r') as fd:
            read_settings = naxhash.settings.read_settings_from_file(fd)
        self.assertEqual(self.settings, read_settings)

    def test_benchmarks(self):
        testfile = self.testdir/'benchmarks.json'
        with open(testfile, 'w') as fd:
            naxhash.settings.write_benchmarks_to_file(fd, self.benchmarks)
        with open(testfile, 'r') as fd:
            read_benchmarks = naxhash.settings.read_benchmarks_from_file(
                fd, self.devices)
        device = self.devices[0]
        self.assertEqual(self.benchmarks, read_benchmarks)

    def test_persistent_settings(self):
        naxhash.settings.save_settings(self.testdir, self.settings)
        read_settings = naxhash.settings.load_settings(self.testdir)
        self.assertEqual(self.settings, read_settings)

    def test_persistent_benchmarks(self):
        naxhash.settings.save_benchmarks(self.testdir, self.benchmarks)
        read_benchmarks = naxhash.settings.load_benchmarks(
            self.testdir, self.devices)
        self.assertEqual(self.benchmarks, read_benchmarks)


if __name__ == '__main__':
    main()

