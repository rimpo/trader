from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch

from lib.time import TimeService, TimeRange, india

class TestTimeRange(TestCase):

    def test_range_time(self):
        time_range = TimeRange(15)
        with patch('lib.time.TimeService.get_current_time') as mock_datetime:
            mock_datetime.return_value = india.localize(datetime(2021, 1, 22, 9, 15, 0, 0))

            time = time_range.get_next()
