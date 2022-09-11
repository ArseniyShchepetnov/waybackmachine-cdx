"""Iterator over Wayback Machine sites using CDX."""
import json
import logging
from collections.abc import Iterator
from typing import List, Optional

import pandas as pd
import requests

from waybackmachine_cdx.cdx import WaybackMachineCDX

logger = logging.getLogger(__name__)


class WaybackMachineIteratorCDX(Iterator):
    """
    Iterator over WaybackMachine CDX results.
    """

    def __init__(self,
                 url: str,
                 n_cached: int = 100,
                 timeout: int = 10,
                 **kwargs):
        """
        Parameters
        ----------
        url : str
            URL parameter for WaybackMachine CDX.
        n_cached : int, optional
            Number of tuples for one request, by default 100.
        **kwargs :
            Other parameters passed to `WaybackMachineCDX` constructor.
        """

        self._cdx = WaybackMachineCDX(url, **kwargs)

        self._cdx.set_limits(n_cached, None, None)
        self._cdx.set_output_format('json')

        self._cached_data = None
        self._current_item = 0

        self.timeout = timeout

    def __iter__(self) -> Iterator:
        return self

    def __next__(self):

        if (self._cached_data is None
                or self._current_item == self._cached_data.n_rows - 1):

            if self._cached_data is None:
                self._cdx.set_resume_key(show=True, key=None)
            else:

                if self._cached_data.resume_key is not None:
                    self._cdx.set_resume_key(show=True,
                                             key=self._cached_data.resume_key)
                else:
                    logger.info("StopIteration")
                    raise StopIteration

            response = requests.get(self._cdx.cdx, timeout=self.timeout)
            logger.info("Response status code %d", response.status_code)

            content = response.content
            logger.info("Response content length %d", len(content))

            json_data = json.loads(content)
            logger.info("Response content: %d rows", len(json_data))

            self._cached_data = WaybackMachineResponseCDX(json_data)
            self._current_item = 0

        else:

            self._current_item += 1

        item = self._cached_data.data.iloc[self._current_item]

        return item


class WaybackMachineResponseCDX:
    """
    Response from WaybackMachine using CDX.

    Stores result in the pandas dataframe and the resume key.
    """

    def __init__(self, data: List[List[str]]):
        """
        Parameters
        ----------
        data : List[List[str]]
            Response result from the WaybackMachine
            as list of lists of strings.
        """
        self._resume_key: Optional[str]

        if len(data[-2]) == 0:

            self._resume_key = data[-1][0]
            self._data = pd.DataFrame(data=data[1:-2], columns=data[0])

        else:

            self._resume_key = None
            self._data = pd.DataFrame(data=data[1:], columns=data[0])

    @property
    def resume_key(self) -> Optional[str]:
        """WaybackMachine resume key property."""
        return self._resume_key

    @property
    def data(self) -> pd.DataFrame:
        """Tuples from the WaybackMachine"""
        return self._data

    @property
    def n_rows(self):
        """Number of tuples."""
        return len(self.data.index)
