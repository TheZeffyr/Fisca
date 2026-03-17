import pytest

from app.core.config import Config


def test_config_reads_env(monkeypatch):
	monkeypatch.setenv("DB_URL", "sqlite:///test.db")
	monkeypatch.setenv("LOG_LEVEL", "10")

	config = Config()
	
	assert config.DB_URL == "sqlite:///test.db"
	assert config.LOG_LEVEL == 10

def test_config_missing_env(monkeypatch):
	monkeypatch.delenv("DB_URL", raising=False)

	with pytest.raises(ValueError):
		Config().DB_URL

