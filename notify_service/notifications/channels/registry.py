import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from dataclasses import dataclass

from .base import BaseNotifier


@dataclass(frozen=True)
class ChannelMeta:
    code: str
    label: str
    notifier_class: Type[BaseNotifier]


def load_channels() -> Dict[str, ChannelMeta]:
    registry: Dict[str, ChannelMeta] = {}

    # Получаем абсолютный путь к директории notifiers
    notifiers_dir = Path(__file__).parent / "notifiers"

    # Определяем имя пакета на основе __package__
    package_prefix = f"{__package__}.notifiers"

    for file in notifiers_dir.glob("*.py"):
        if file.name.startswith("__") or file.stem in {"base", "registry"}:
            continue

        module_name = file.stem
        import_path = f"{package_prefix}.{module_name}"

        try:
            module = importlib.import_module(import_path)
        except ModuleNotFoundError as e:
            raise ImportError(f"Не удалось импортировать модуль '{import_path}': {e}") from e

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, BaseNotifier) and cls is not BaseNotifier:
                registry[module_name] = ChannelMeta(
                    code=module_name,
                    label=module_name.capitalize(),
                    notifier_class=cls
                )

    return registry


CHANNEL_REGISTRY = load_channels()
