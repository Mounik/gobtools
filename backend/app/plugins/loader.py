from pathlib import Path

import yaml

from app.core.config import settings
from app.plugins.models import PluginManifest


class PluginLoader:
    def __init__(self):
        self._plugins: dict[str, PluginManifest] = {}
        self._prompts: dict[str, str] = {}

    def load_all(self) -> None:
        plugins_dir = Path(settings.PLUGINS_DIR)
        if not plugins_dir.exists():
            return

        for plugin_dir in sorted(plugins_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue

            manifest_path = plugin_dir / "manifest.yaml"
            if not manifest_path.exists():
                continue

            with open(manifest_path) as f:
                data = yaml.safe_load(f)

            manifest = PluginManifest(**data)
            manifest.slug = plugin_dir.name

            prompt_path = plugin_dir / manifest.prompt_file
            if prompt_path.exists():
                self._prompts[manifest.slug] = prompt_path.read_text()

            workflow_path = plugin_dir / "workflow.py"
            manifest.has_workflow = workflow_path.exists()

            self._plugins[manifest.slug] = manifest

    def list_all(self) -> list[PluginManifest]:
        return list(self._plugins.values())

    def get(self, slug: str) -> PluginManifest | None:
        return self._plugins.get(slug)

    def get_prompt(self, slug: str) -> str:
        return self._prompts.get(slug, "")

    def reload(self) -> None:
        self._plugins.clear()
        self._prompts.clear()
        self.load_all()


plugin_loader = PluginLoader()
