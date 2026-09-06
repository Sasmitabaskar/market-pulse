from app.core.config import settings

def test_settings():
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.debug is True
    assert settings.postgres_host == "localhost"
    assert settings.postgres_port == 5433
    assert settings.postgres_db == "marketpulse"
    assert settings.postgres_user == "postgres"
    assert settings.postgres_password == "postgres"