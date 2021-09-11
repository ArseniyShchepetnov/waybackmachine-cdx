"""CDX query URL constructor."""
import datetime
from typing import Any, Dict, List, Optional

import requests

CDX_DOCS = (
    'https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server'
)

CDX_MATCH_TYPE = 'matchType'
CDX_LIMIT = 'limit'
CDX_RESUME_KEY = 'resumeKey'
CDX_SHOW_RESUME_KEY = 'showResumeKey'
CDX_OFFSET = 'offset'
CDX_FAST_LATEST = 'fastLatest'
CDX_OUTPUT_TYPE = 'output'
CDX_FROM_DATETIME = 'from'
CDX_TO_DATETIME = 'to'
CDX_FIELD_ORDER = 'fl'
CDX_URL = 'url'

CDX_LIST_MATCH_TYPES = ['exact', 'prefix', 'host', 'domain']
CDX_LIST_OUTPUT_FORMATS = ['json']
CDX_LIST_FIELD_ORDERS = ["urlkey", "timestamp", "original",
                         "mimetype", "statuscode", "digest", "length"]


CDX_BASE = 'http://web.archive.org/cdx/search/'


CDX_DATETIME_FORMAT = r'%Y%m%d%H%M%S'


def cdx_construct(url: str,
                  params: Optional[Dict[str, Any]] = None) -> str:
    """Construct request url with parameters."""

    result = CDX_BASE + f"cdx?url={url}"

    if params:
        for param, value in params.items():

            if value is not None:
                result += f"&{param}={value}"

    return result


class WaybackMachineCDX:
    """
    CDX request constructor for Wayback Machine.
    """

    def __init__(self,
                 url: str,
                 match_type: Optional[str] = None,
                 output: Optional[str] = None,
                 field_order: Optional[str] = None,
                 from_dt: Optional[str] = None,
                 to_dt: Optional[str] = None,
                 limits: Optional[int] = None,
                 fast_latest: Optional[bool] = None,
                 offset: Optional[int] = None,
                 resume_key: Optional[str] = None,
                 show_resume_key: Optional[bool] = None):
        """
        Parameters
        ----------
        url : str
            URL to request from WaybackMachine
        match_type : Optional[str], optional
            Match type parameter, by default None
        output : Optional[str], optional
            Output formats, by default None
        field_order : Optional[str], optional
            Field order, by default None
        from_dt : Optional[str], optional
            Datetime start, by default None
        to_dt : Optional[str], optional
            Datetime end, by default None
        limits : Optional[int], optional
            Limit number of tuples in response, by default None
        fast_latest : Optional[bool], optional
            Advanced option for latest results, by default None
        offset : Optional[int], optional
            Number of records to skip, by default None
        resume_key : Optional[str], optional
            Resume key parameter, by default None
        show_resume_key : Optional[bool], optional
            Show the resume key, by default None
        """

        self.url = url

        self.params = {}

        self.set_match_scope(match_type)
        self.set_output_format(output)
        self.set_field_order(field_order)
        self.set_datatime_range(from_dt, to_dt)
        self.set_limits(limits, fast_latest, offset)
        self.set_resume_key(resume_key, show_resume_key)

    @property
    def cdx(self) -> str:
        """Return constructed CDX query."""
        return self.construct(self.params)

    def construct(self, params: Optional[Dict[str, Any]] = None) -> str:
        """Construct with parameters."""
        return cdx_construct(self.url, params)

    def test_cdx_is_valid(self) -> bool:
        """Check that request with limit=1 parameter returns OK code."""

        params = self.params.copy()

        params[CDX_LIMIT] = 1

        cdx = self.construct(params)

        response = requests.get(cdx)

        return response.status_code == requests.codes.ok  # pylint: disable=maybe-no-member

    def set_match_scope(self, scope: Optional[str] = None):
        """Set scope 'matchType' parameter."""

        if scope is not None and scope not in CDX_LIST_MATCH_TYPES:
            raise ValueError(f"Scope is invalid {scope}. "
                             f"Valid scopes: {CDX_LIST_MATCH_TYPES}. "
                             f"See {CDX_DOCS} for details")

        self.params[CDX_MATCH_TYPE] = scope

    def set_field_order(self, field_order: Optional[List[str]] = None):
        """Set field order parameter"""

        if field_order is not None:
            unknown_items = list(set(field_order) - set(CDX_LIST_FIELD_ORDERS))
            if len(unknown_items) > 0:
                raise ValueError(f"Unknown items in 'fl': {unknown_items}. "
                                 f"Valid items: {CDX_LIST_FIELD_ORDERS}. "
                                 f"See {CDX_DOCS} for details")
            field_order = ",".join(field_order)

        self.params[CDX_FIELD_ORDER] = field_order

    def set_output_format(self, output: Optional[str] = None):
        """Set output formats."""

        if output is not None and output not in CDX_LIST_OUTPUT_FORMATS:
            raise ValueError(f"Output format is invalid {output}. "
                             f"Valid formats: {CDX_LIST_OUTPUT_FORMATS}. "
                             f"See {CDX_DOCS} for details")

        self.params[CDX_OUTPUT_TYPE] = output

    def set_datatime_range(self,
                           from_dt: Optional[datetime.datetime] = None,
                           to_dt: Optional[datetime.datetime] = None):
        """Set datetime range."""

        cdx_params = [CDX_FROM_DATETIME, CDX_TO_DATETIME]
        params = [from_dt, to_dt]

        for name, val in zip(cdx_params, params):

            if val is not None:
                val = val.strftime(CDX_DATETIME_FORMAT)
                self.params[name] = val

    def set_limits(self,
                   limit: Optional[int] = None,
                   fast_latest: Optional[bool] = None,
                   offset: Optional[int] = None):
        """Set limits parameters"""

        self.params[CDX_LIMIT] = limit
        self.params[CDX_FAST_LATEST] = fast_latest
        self.params[CDX_OFFSET] = offset

    def set_resume_key(self,
                       show: Optional[bool] = None,
                       key: Optional[str] = None):
        """Set resume key parameters"""

        self.params[CDX_SHOW_RESUME_KEY] = show
        self.params[CDX_RESUME_KEY] = key
