import unittest
from utils.add_scraped_files import create_path_to_folder, get_timestamp_from_file

rootdir = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/'

class TestUtilsFunctions(unittest.TestCase):
    def test_creating_catalog_path_without_extension(self):
        path = create_path_to_folder('Rainbow', '2024-01-01')
        self.assertEqual(path, '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/Rainbow/2024-01-01')

    def test_creating_catalog_path_with_extension(self):
        path = create_path_to_folder('Rainbow', '2024-01-01','tar')
        self.assertEqual(path, '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/Rainbow/2024-01-01.tar')


class TestGettingTimestampFromFile(unittest.TestCase):
    def test_get_timestamp_from_json_gz_file(self):
        file_name = 'exmaple-tour_2024-04-10T19:24:43.12345.json.gz'
        expected_timestamp = '2024-04-10T19:24:43.12345'
        timestamp = get_timestamp_from_file(file_name)
        self.assertEqual(timestamp, expected_timestamp)

    def test_get_timestamp_from_json_file(self):
        file_name = 'exmaple-tour_2024-04-10T19:24:43.12345.json'
        expected_timestamp = '2024-04-10T19:24:43.12345'
        timestamp = get_timestamp_from_file(file_name)
        self.assertEqual(timestamp, expected_timestamp)