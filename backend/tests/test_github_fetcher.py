from app.core.github_fetcher import _select_files_to_fetch


def test_select_files_to_fetch():
    file_tree = [
        "main.py",
        "app/config.py",
        "src/index.ts",
        "package.json",
        "README.md",
        "images/logo.png",
        "docs/api.md",
        "tests/test_main.py"
    ]
    
    selected = _select_files_to_fetch(file_tree)
    
    assert "main.py" in selected
    assert "app/config.py" in selected
    assert "src/index.ts" in selected
    assert "package.json" in selected
    # README.md is usually handled separately, but included if in priority
    assert "images/logo.png" not in selected
