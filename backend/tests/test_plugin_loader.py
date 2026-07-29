from app.plugins.loader import plugin_loader


def test_plugin_loader_loads_plugin():
    plugins = plugin_loader.list_all()
    slugs = [p.slug for p in plugins]
    assert "test-tool" in slugs


def test_plugin_loader_get_manifest():
    manifest = plugin_loader.get("test-tool")
    assert manifest is not None
    assert manifest.name == "Test Tool"
    assert manifest.provider == "ollama"
    assert manifest.model == "qwen3"
    assert manifest.temperature == 0.2
    assert manifest.category == "test"
    assert manifest.has_workflow is False


def test_plugin_loader_get_prompt():
    prompt = plugin_loader.get_prompt("test-tool")
    assert prompt == "You are a test assistant.\nRespond with: TEST OK"


def test_plugin_loader_unknown_plugin():
    assert plugin_loader.get("nonexistent") is None
    assert plugin_loader.get_prompt("nonexistent") == ""
