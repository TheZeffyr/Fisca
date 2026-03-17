import pytest

from app.core.config import Config


def test_config_reads_env(monkeypatch):
	monkeypatch.setenv("DB_URL", "sqlite:///test.db")
	monkeypatch.setenv("DEBUG", "true")

	config = Config()
	
	assert config.DB_URL == "sqlite:///test.db"
	assert config.DEBUG is True

def test_config_missing_env(monkeypatch):
	monkeypatch.delenv("DB_URL", raising=False)

	with pytest.raises(ValueError):
		Config().DB_URL

def test_debug_parsing(monkeypatch):
	monkeypatch.setenv("DEBUG", "False")

	config = Config()
	assert config.DEBUG is False
