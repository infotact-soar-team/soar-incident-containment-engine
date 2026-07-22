import pytest
from unittest.mock import patch, MagicMock
from app.integrations.geoip import lookup_ip_location


@patch("app.integrations.geoip.geoip2.database.Reader")
def test_lookup_ip_location_success(mock_reader_cls):
    mock_response = MagicMock()
    mock_response.country.name = "Germany"
    mock_response.country.iso_code = "DE"
    mock_response.city.name = "Berlin"
    mock_response.location.latitude = 52.52
    mock_response.location.longitude = 13.405

    mock_reader = MagicMock()
    mock_reader.city.return_value = mock_response
    mock_reader_cls.return_value.__enter__.return_value = mock_reader

    result = lookup_ip_location("185.220.101.1")
    assert result["country"] == "Germany"
    assert result["city"] == "Berlin"


def test_lookup_ip_location_missing_db_file(monkeypatch):
    monkeypatch.setattr("app.integrations.geoip.settings.GEOLITE2_DB_PATH", "/nonexistent/path.mmdb")
    with pytest.raises(FileNotFoundError):
        lookup_ip_location("185.220.101.1")