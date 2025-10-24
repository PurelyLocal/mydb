import pytest
import frontmatter
import pathlib

DOCS_PATH = pathlib.Path("docs")

@pytest.mark.parametrize("file_path", DOCS_PATH.rglob("*.md"))
def test_yaml_frontmatter(file_path):
    """Ensure all Markdown files have valid YAML frontmatter."""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        assert "id" in post.metadata, f"Missing 'id' in {file_path}"
        assert "status" in post.metadata, f"Missing 'status' in {file_path}"