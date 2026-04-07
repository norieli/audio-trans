"""
Configuration Manager - Handles app configuration and API key storage
配置管理 - 处理应用配置和API密钥存储
"""
import os
import json
import base64
from pathlib import Path


class ConfigManager:
    """Manages application configuration"""

    CONFIG_DIR = Path.home() / ".audiotrans"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file"""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._default_config()

    def _default_config(self) -> dict:
        """Default configuration"""
        return {
            "source_dir": "",
            "output_dir": "",
            "match_rule": "",  # keyword, prefix, suffix
            "match_value": "",
            "filename_rule": "preserve",  # preserve, sequential
            "filename_prefix": "",
            "seq_digits": 3,
            "organize_mode": "copy",  # copy, move
            "translate_mode": "local",  # local, ai
            "api_key": "",
            "step_status": {},  # Track completed steps
        }

    def save(self):
        """Save configuration to file"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save()

    def encode_api_key(self, api_key: str) -> str:
        """Encode API key with base64"""
        return base64.b64encode(api_key.encode()).decode()

    def decode_api_key(self, encoded: str) -> str:
        """Decode API key from base64"""
        return base64.b64decode(encoded.encode()).decode()

    def get_api_key(self) -> str:
        """Get decoded API key"""
        encoded = self.config.get("api_key", "")
        if encoded:
            return self.decode_api_key(encoded)
        return ""

    def set_api_key(self, api_key: str):
        """Set and encode API key"""
        if api_key:
            self.config["api_key"] = self.encode_api_key(api_key)
            self.save()

    def reset(self):
        """Reset all configuration"""
        self.config = self._default_config()
        self.save()