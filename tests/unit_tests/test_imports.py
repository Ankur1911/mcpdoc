def test_imports():
    """Test that main modules can be imported."""
    from mcpdoc import main  # noqa
    from mcpdoc import cli  # noqa
    from mcpdoc import langgraph  # noqa

    assert True


def test_mcp_requirement_excludes_v2() -> None:
    """The code uses `mcp.server.fastmcp`, which mcp 2.x removed.

    A fresh install without the lockfile must not resolve to mcp 2.x.
    """
    from importlib.metadata import requires, version

    from packaging.requirements import Requirement

    mcp_req = next(
        req
        for req in map(Requirement, requires("mcpdoc") or [])
        if req.name == "mcp" and req.marker is None
    )
    assert not mcp_req.specifier.contains("2.0.0")
    assert not mcp_req.specifier.contains("2.3.0")
    assert mcp_req.specifier.contains("1.28.1")

    # The installed mcp must satisfy the declared range and expose FastMCP.
    assert mcp_req.specifier.contains(version("mcp"))
    from mcp.server.fastmcp import FastMCP  # noqa: F401
