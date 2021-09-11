"""Test `WaybackMachineCDX` class."""
import unittest
from datetime import datetime

from waybackmachine_cdx import WaybackMachineCDX


class TestWaybackMachineCDX(unittest.TestCase):
    """Test `WaybackMachineCDX` class."""

    def test_constructor(self):
        """Test cdx is valid."""

        today = datetime.today()

        cdx = WaybackMachineCDX(url='google.com',
                                match_type='exact',
                                output='json',
                                field_order=['original'],
                                from_dt=today.replace(year=today.year - 1),
                                to_dt=today,
                                limits=1,
                                fast_latest=False,
                                offset=0,
                                resume_key=None,
                                show_resume_key=False)

        cdx.test_cdx_is_valid()
