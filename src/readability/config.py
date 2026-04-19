"""Configuration loader - supports config.yaml and environment variables"""

import os
from pathlib import Path
from typing import Optional
import yaml


def get_hermes_config_path() -> Optional[Path]:
    """Get Hermes config path if it exists"""
    hermes_home = Path.home() / ".hermes"
    config_path = hermes_home / "config.yaml"
    if config_path.exists():
        return config_path
    return None


def load_api_config() -> dict:
    """Load API configuration from Hermes config or environment"""
    # Try Hermes config first
    hermes_config_path = get_hermes_config_path()
    if hermes_config_path:
        try:
            with open(hermes_config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            model_cfg = config.get("model", {})
            api_key = model_cfg.get("api_key") or os.environ.get("MINIMAX_API_KEY")
            base_url = model_cfg.get("base_url") or "https://api.minimaxi.com/anthropic"
            if api_key:
                return {
                    "api_key": api_key,
                    "base_url": base_url,
                    "model": model_cfg.get("default", "MiniMax-M2.7"),
                }
        except Exception:
            pass

    # Fallback to local config.yaml
    local_config = Path(__file__).parent.parent.parent / "config.yaml"
    if local_config.exists():
        try:
            with open(local_config, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            model_cfg = config.get("model", {})
            api_key = model_cfg.get("api_key") or os.environ.get("MINIMAX_API_KEY")
            base_url = model_cfg.get("base_url") or "https://api.minimaxi.com/anthropic"
            if api_key:
                return {
                    "api_key": api_key,
                    "base_url": base_url,
                    "model": model_cfg.get("default", "MiniMax-M2.7"),
                }
        except Exception:
            pass

    # Environment variables fallback
    api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("MINIMAX_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "https://api.minimaxi.com/anthropic")

    if api_key:
        return {
            "api_key": api_key,
            "base_url": base_url,
            "model": "MiniMax-M2.7",
        }

    raise ValueError(
        "未找到API配置。请确保以下任一位置有配置：\n"
        "1. ~/.hermes/config.yaml 中的 model.api_key\n"
        "2. 当前目录的 config.yaml\n"
        "3. 环境变量 MINIMAX_API_KEY"
    )
