import io
import zipfile

import pytest

from app.core.zip_parser import extract_project_context


def test_extract_project_context_valid_zip():
    # Create a dummy zip in memory
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("main.py", "print('hello')")
        zf.writestr("README.md", "# Test Project")
        zf.writestr("node_modules/index.js", "console.log('skip me')")
    
    zip_content = buf.getvalue()
    context = extract_project_context(zip_content, "test.zip")
    
    assert context.project_name == "test"
    assert "main.py" in context.files
    assert context.files["main.py"] == "print('hello')"
    assert "README.md" in context.files
    assert "node_modules/index.js" not in context.files
    assert context.readme_content == "# Test Project"

def test_extract_project_context_invalid_zip():
    with pytest.raises(ValueError, match="Invalid ZIP file"):
        extract_project_context(b"not a zip", "bad.zip")
