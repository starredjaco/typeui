"""Tool handlers for installing TypeUI MCP in Hermes Agent."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - Hermes ships YAML support.
    yaml = None


TYPEUI_MCP_URL = "https://mcp.typeui.sh"
TYPEUI_MCP_SERVER = {
    "url": TYPEUI_MCP_URL,
    "auth": "oauth",
}
_RAW_CONFIG_TEXT = "__typeui_raw_config_text"


def _json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def _default_config_path() -> Path:
    hermes_home = os.environ.get("HERMES_HOME")
    if hermes_home:
        return Path(hermes_home).expanduser() / "config.yaml"
    return Path.home() / ".hermes" / "config.yaml"


def _resolve_config_path(value: Any) -> Path:
    if isinstance(value, str) and value.strip():
        return Path(value).expanduser()
    return _default_config_path()


def _unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _load_config_without_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    raw_text = path.read_text(encoding="utf-8")
    config: dict[str, Any] = {_RAW_CONFIG_TEXT: raw_text}

    if not raw_text.strip():
        return config

    lines = raw_text.splitlines()
    mcp_index = None
    for index, line in enumerate(lines):
        if line.startswith("mcp_servers:"):
            mcp_index = index
            break

    if mcp_index is None:
        config["mcp_servers"] = {}
        return config

    typeui_server: dict[str, Any] | None = None
    in_typeui = False
    in_auth = False

    for line in lines[mcp_index + 1 :]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            break

        if indent == 2 and stripped.startswith("typeui:"):
            typeui_server = {}
            in_typeui = True
            in_auth = False
            continue

        if in_typeui and indent <= 2:
            break

        if not in_typeui or typeui_server is None:
            continue

        if indent == 4 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.split(" #", 1)[0].strip()

            if key == "url":
                typeui_server["url"] = _unquote_yaml_scalar(value)
                in_auth = False
            elif key == "auth" and value:
                typeui_server["auth"] = _unquote_yaml_scalar(value)
                in_auth = False
            elif key == "auth":
                typeui_server["auth"] = {}
                in_auth = True
            else:
                in_auth = False
            continue

        if in_auth and indent == 6 and ":" in stripped:
            key, value = stripped.split(":", 1)
            if key.strip() == "type":
                typeui_server["auth"]["type"] = _unquote_yaml_scalar(
                    value.split(" #", 1)[0].strip()
                )

    config["mcp_servers"] = {"typeui": typeui_server} if typeui_server else {}
    return config


def _load_config(path: Path) -> dict[str, Any]:
    if yaml is None:
        return _load_config_without_yaml(path)

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a YAML mapping at the top level.")

    return loaded


def _typeui_server_yaml() -> str:
    return "\n".join(
        [
            "mcp_servers:",
            "  typeui:",
            f'    url: "{TYPEUI_MCP_URL}"',
            "    auth: oauth",
            "",
        ]
    )


def _write_config_without_yaml(path: Path, config: dict[str, Any]) -> str | None:
    raw_text = config.get(_RAW_CONFIG_TEXT)
    server = (config.get("mcp_servers") or {}).get("typeui")

    if not _is_typeui_mcp_configured(server):
        raise RuntimeError("Cannot write TypeUI MCP config without a valid typeui server entry.")

    if raw_text and raw_text.strip():
        if "\nmcp_servers:" in f"\n{raw_text}" and "typeui:" not in raw_text:
            raise RuntimeError(
                "PyYAML is required to update an existing Hermes config that already contains mcp_servers."
            )
        next_text = raw_text.rstrip() + "\n\n" + _typeui_server_yaml()
    else:
        next_text = _typeui_server_yaml()

    path.parent.mkdir(parents=True, exist_ok=True)
    backup_path = _backup_config(path)
    path.write_text(next_text, encoding="utf-8")
    return backup_path


def _backup_config(path: Path) -> str | None:
    if not path.exists():
        return None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    backup_path = path.with_name(f"{path.name}.typeui.{stamp}.bak")
    shutil.copy2(path, backup_path)
    return str(backup_path)


def _write_config(path: Path, config: dict[str, Any]) -> str | None:
    if yaml is None:
        return _write_config_without_yaml(path, config)

    path.parent.mkdir(parents=True, exist_ok=True)
    backup_path = _backup_config(path)

    config = {key: value for key, value in config.items() if key != _RAW_CONFIG_TEXT}

    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, sort_keys=False, default_flow_style=False)

    return backup_path


def _has_oauth_auth(auth: Any) -> bool:
    if auth == "oauth":
        return True

    if isinstance(auth, dict):
        return auth.get("type") == "oauth"

    return False


def _is_typeui_mcp_configured(server: Any) -> bool:
    return (
        isinstance(server, dict)
        and server.get("url") == TYPEUI_MCP_URL
        and _has_oauth_auth(server.get("auth"))
    )


def _server_payload(current: Any) -> dict[str, Any]:
    server = dict(current) if isinstance(current, dict) else {}
    server.update(TYPEUI_MCP_SERVER)
    return server


def install_mcp(args: dict[str, Any], **kwargs: Any) -> str:
    """Install TypeUI MCP into Hermes config.yaml."""
    try:
        config_path = _resolve_config_path(args.get("config_path"))
        force = bool(args.get("force", False))
        config = _load_config(config_path)

        mcp_servers = config.get("mcp_servers")
        if mcp_servers is None:
            mcp_servers = {}
            config["mcp_servers"] = mcp_servers
        elif not isinstance(mcp_servers, dict):
            raise ValueError("mcp_servers must be a YAML mapping.")

        current = mcp_servers.get("typeui")
        was_configured = _is_typeui_mcp_configured(current)
        changed = False
        backup_path = None

        if force or not was_configured:
            mcp_servers["typeui"] = _server_payload(current)
            backup_path = _write_config(config_path, config)
            changed = True

        return _json(
            {
                "changed": changed,
                "was_configured": was_configured,
                "config_path": str(config_path),
                "backup_path": backup_path,
                "server": mcp_servers.get("typeui"),
                "next_steps": [
                    "hermes mcp login typeui",
                    "Restart Hermes or run /reload-mcp in an active Hermes session.",
                ],
            }
        )
    except Exception as exc:
        return _json({"error": str(exc)})


def mcp_status(args: dict[str, Any], **kwargs: Any) -> str:
    """Return TypeUI MCP status for Hermes config.yaml."""
    try:
        config_path = _resolve_config_path(args.get("config_path"))
        config = _load_config(config_path)
        mcp_servers = config.get("mcp_servers") or {}

        if not isinstance(mcp_servers, dict):
            raise ValueError("mcp_servers must be a YAML mapping.")

        server = mcp_servers.get("typeui")

        return _json(
            {
                "configured": _is_typeui_mcp_configured(server),
                "config_path": str(config_path),
                "server": server,
                "expected": TYPEUI_MCP_SERVER,
            }
        )
    except Exception as exc:
        return _json({"error": str(exc)})
