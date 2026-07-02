"""Directory-plugin entrypoint for TypeUI Hermes integration."""

try:
    from .typeui_hermes import register
except ImportError:
    from typeui_hermes import register

__all__ = ["register"]
