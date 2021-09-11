# WaybackMachine CDX Python Module

[WaybackMachine](https://archive.org/web/) website

[WaybackMachine CDX](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) code

## Example

```python

from datetime import datetime
from waybackmachine_cdx import WaybackMachineCDX

from_datetime = datetime.datetime(2020, 9, 11, 15, 45, 5)
to_datetime = datetime.datetime(2021, 9, 11, 15, 45, 5)

cdx = WaybackMachineCDX(url='google.com',
                        match_type='exact',
                        output='json',
                        field_order=['original'],
                        from_dt=from_datetime,
                        to_dt=to_datetime,
                        limits=1,
                        fast_latest=False,
                        offset=0,
                        resume_key=None,
                        show_resume_key=False)
print(cdx.cdx)
```
Result:
```
http://web.archive.org/cdx/search/cdx?url=google.com&matchType=exact&output=json&fl=original&from=20200911154505&to=20210911154505&limit=1&fastLatest=False&offset=0&resumeKey=False
```
