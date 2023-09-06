def test_filters_imports():
    from utils import filters

    assert hasattr(filters, "BaseFilterManager")
    assert hasattr(filters, "FilterSchema")
