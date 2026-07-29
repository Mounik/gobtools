import pytest
import respx
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_tools(client: AsyncClient):
    resp = await client.get("/api/v1/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    slugs = [t["slug"] for t in data]
    assert "test-tool" in slugs


@pytest.mark.asyncio
async def test_get_tool(client: AsyncClient):
    resp = await client.get("/api/v1/tools/test-tool")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Tool"
    assert data["prompt"] == "You are a test assistant.\nRespond with: TEST OK"


@pytest.mark.asyncio
async def test_get_tool_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/tools/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_run_tool(client: AsyncClient):
    with respx.mock:
        respx.post("http://localhost:11434/api/generate").respond(
            json={"response": "# Result\n\nMocked response"}
        )

        payload = {"tool_slug": "test-tool", "input": "Hello"}
        resp = await client.post("/api/v1/run", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data
        assert data["provider"] == "ollama"
        assert data["model"] == "qwen3"
        assert "Mocked response" in data["output"]


@pytest.mark.asyncio
async def test_run_tool_empty_slug(client: AsyncClient):
    payload = {"tool_slug": "", "input": "Hello"}
    resp = await client.post("/api/v1/run", json=payload)
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_run_tool_not_found(client: AsyncClient):
    payload = {"tool_slug": "nonexistent", "input": "Hello"}
    resp = await client.post("/api/v1/run", json=payload)
    assert resp.status_code == 404
