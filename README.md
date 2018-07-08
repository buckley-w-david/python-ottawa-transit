[![CircleCI](https://circleci.com/gh/buckley-w-david/python-ottawa-transit.svg?style=svg)](https://circleci.com/gh/buckley-w-david/python-ottawa-transit)
# python-ottawa-transit

Python interface to the [OC Transpo](http://www.octranspo.com/developers/documentation) API and utilities for working with the returned data.

## Installation

The package is available on [PyPi](https://pypi.org/project/python-ottawa-transit)
```bash
pip install python-ottawa-transit
```

Alternativly it can be installed from source using [Poetry](https://github.com/sdispater/poetry)
```bash
git clone https://github.com/buckley-w-david/python-ottawa-transit.git
cd python-ottawa-transit
poetry install
```

## Usage

```python3
>>> from python_ottawa_transit import OCTransportApi
>>> api = OCTransportApi(app_id = 'APPLICATION_ID', app_key = 'APPLICATION_KEY')
>>> api.get_route_summary_for_stop(stop_no=8435)
{"GetRouteSummaryForStopResult":{"StopNo":"8435","StopDescription":"BANK \\/ COLLINS","Error":"","Routes":{"Route":{"RouteNo":6,"DirectionID":1,"Direction":"Northbound","RouteHeading":"Rockcliffe"}}}}
```
