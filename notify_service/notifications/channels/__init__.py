from .registry import CHANNEL_REGISTRY


CHANNEL_MAP = {k: v.notifier_class() for k, v in CHANNEL_REGISTRY.items()}
CHANNEL_CHOICES = [(k, v.label) for k, v in CHANNEL_REGISTRY.items()]