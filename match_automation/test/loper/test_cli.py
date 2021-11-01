import unittest
from os.path import dirname, abspath, join

from ...loper import cli


class TestCli(unittest.TestCase):

    def test_notes_sociable(self):
        test_resource_dir = join(dirname(dirname(abspath(__file__))), 'resources')
        cli.notes(user_dir_path=join(test_resource_dir, 'person_reports'),
                  output_dir='.',
                  content_file_path=join(test_resource_dir, 'school_content', 'test_school_content.xlsx'))

    def test_reports_sociable(self):
        test_resource_dir = join(dirname(dirname(abspath(__file__))), 'resources')
        cli.reports(user_dir_path=join(test_resource_dir, 'person_reports'),
                    output_dir='.',
                    content_file_path=join(test_resource_dir, 'school_content', 'test_school_content.xlsx'),
                    media_dir='')
