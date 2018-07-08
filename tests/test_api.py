from io import BytesIO
import re
import string
import typing
import urllib.request
import urllib.parse

from hypothesis import given
import hypothesis.strategies as st
import pytest

from python_ottawa_transit import api


def is_capital_camel(name: str) -> bool:
    return re.match("^(?:[A-Z][a-z]+)+$", name) is not None


def is_camel(name: str) -> bool:
    return re.match("^(?:[a-z]+)(?:[A-Z][a-z]+)*$", name) is not None


@given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=2), min_size=1))
def test_transform_method_name(strings) -> str:
    name = "_".join(strings)
    transformed = api.transform_method_name(name)
    assert is_capital_camel(transformed)


@given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=2), min_size=1))
def test_transform_argument_name(strings) -> str:
    name = "_".join(strings)
    transformed = api.transform_argument_name(name)
    assert is_camel(transformed)


class TestOCTransportApi:
    @pytest.fixture
    def api(self) -> api.OCTransportApi:
        return api.OCTransportApi("APP_ID", "APP_KEY")

    def test_get_route_summary_for_stop(self, monkeypatch, api) -> None:
        def mock_response(url, payload) -> typing.IO[bytes]:
            response = BytesIO()
            args = urllib.parse.parse_qs(payload.decode("utf-8"))

            # Generated the correct API Endpoint, and passed the arguments along correctly
            if (
                url == "https://api.octranspo1.com/v1.2/GetRouteSummaryForStop"
                and args
                == {
                    "appID": ["APP_ID"],
                    "apiKey": ["APP_KEY"],
                    "format": ["json"],
                    "stopNo": ["8435"],
                }
            ):
                response.write(
                    b'{"GetRouteSummaryForStopResult": {"StopNo": "8435", "StopDescription": "BANK / COLLINS", "Error": "", "Routes": {"Route": {"RouteNo": 6, "DirectionID": 1, "Direction": "Northbound", "RouteHeading": "Rockcliffe"}}}}'
                )
                response.seek(0)
            return response

        monkeypatch.setattr(urllib.request, "urlopen", mock_response)
        assert api.get_route_summary_for_stop(stop_no=8435) == {"GetRouteSummaryForStopResult": {"StopNo": "8435", "StopDescription": "BANK / COLLINS", "Error": "", "Routes": {"Route": {"RouteNo": 6, "DirectionID": 1, "Direction": "Northbound", "RouteHeading": "Rockcliffe"}}}}

        #TODO: Test the other endpoints
