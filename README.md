# WaybackMachine CDX Python Module

[WaybackMachine](https://archive.org/web/) website
[WaybackMachine CDX](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) code

## Example

```python
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
print(cdx.cdx)
```
Result:
```
http://web.archive.org/cdx/search/cdx?url=google.com&matchType=exact&output=json&fl=original&from=20200911154035&to=20210911154035&limit=1&fastLatest=False&offset=0&resumeKey=False
```
