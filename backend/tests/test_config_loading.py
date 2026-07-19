from app.core.config import settings


def test_settings_load_with_defaults():
    assert settings.APP_NAME == "SOAR Incident Containment Engine"
    assert settings.DATABASE_URL.startswith("postgresql://")


def test_settings_has_ti_api_key_fields():
    assert hasattr(settings, "ABUSEIPDB_API_KEY")
    assert hasattr(settings, "VIRUSTOTAL_API_KEY")