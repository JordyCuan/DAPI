from utils.schemas.docs import FastAPIRouteParameters


def test_fast_api_route_parameters_defaults():
    params = FastAPIRouteParameters()

    assert params.tags is None
    assert params.summary is None
    assert params.description is None
    assert params.response_description == "Successful Response"
    assert params.status_code == 200
    assert not params.deprecated
    assert params.include_in_schema
    assert params.operation_id is None
    assert params.responses == {}
    assert params.name is None
    assert params.openapi_extra is None


def test_fast_api_route_parameters_custom_values():
    custom_values = {
        "tags": ["sample"],
        "summary": "Sample summary",
        "status_code": 404,
        "deprecated": True,
        "responses": {404: {"description": "Not found"}},
        "name": "sample_name",
        "openapi_extra": {"extra": "value"},
    }

    params = FastAPIRouteParameters(**custom_values)

    for key, value in custom_values.items():
        assert getattr(params, key) == value
