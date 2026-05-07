import io
import zipfile
from typing import Dict, List

import structlog

from app.config import get_settings
from app.schemas.review import ProjectContext

logger = structlog.get_logger(__name__)
settings = get_settings()

def extract_project_context(zip_content: bytes, filename: str) -> ProjectContext:
    """
    Extract code files from ZIP for review.
    Security rules — enforce all:
    - Reject zip bombs: check uncompressed size before extracting
    - Reject path traversal: skip any path containing '..' or starting with '/'
    - Reject absolute paths
    - Skip binary files (check magic bytes)
    - Skip: node_modules/, __pycache__/, .git/, dist/, .next/, venv/, *.pyc
    - Only read: .py .ts .tsx .js .jsx .json .yml .yaml .md .toml .sh .env.example
    - Max files: settings.MAX_FILES_PER_REVIEW
    - Max file size: settings.MAX_FILE_SIZE_KB KB per file
    """
    files_content: Dict[str, str] = {}
    file_tree: List[str] = []
    readme_content: str | None = None
    
    # 1. Zip bomb check
    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
            total_uncompressed_size = sum(info.file_size for info in zf.infolist())
            if total_uncompressed_size > settings.max_zip_bytes * 5: # 5x limit for decompression
                raise ValueError("Potential zip bomb detected: uncompressed size too large")

            # 2. Iterate and filter files
            allowed_extensions = {
                ".py", ".ts", ".tsx", ".js", ".jsx", ".json", 
                ".yml", ".yaml", ".md", ".toml", ".sh", ".env.example"
            }
            skip_dirs = {
                "node_modules/", "__pycache__/", ".git/", "dist/", 
                ".next/", "venv/", "env/", "target/", "build/"
            }

            for info in zf.infolist():
                if info.is_dir():
                    continue
                
                path = info.filename
                
                # Security: Path traversal & absolute paths
                if ".." in path or path.startswith("/"):
                    logger.warning("security_zip_traversal_skip", path=path)
                    continue
                
                # Filtering: Directories
                if any(skip in path for skip in skip_dirs):
                    continue
                
                file_tree.append(path)
                
                # Filtering: Extensions & Count
                ext = "." + path.split(".")[-1] if "." in path else ""
                if ext.lower() not in allowed_extensions:
                    continue
                
                if len(files_content) >= settings.MAX_FILES_PER_REVIEW:
                    continue

                # Filtering: File size
                if info.file_size > settings.MAX_FILE_SIZE_KB * 1024:
                    logger.warning("zip_file_too_large_skip", path=path, size=info.file_size)
                    continue

                # 3. Read content
                try:
                    with zf.open(info) as f:
                        content = f.read()
                        
                        # Magic bytes check for binary (simple check for null byte)
                        if b'\x00' in content:
                            logger.warning("binary_file_skip", path=path)
                            continue
                            
                        decoded = content.decode("utf-8", errors="ignore")
                        files_content[path] = decoded[:3000] # Cap at 3000 chars as per requirement
                        
                        if path.lower().endswith("readme.md"):
                            readme_content = decoded
                except Exception as e:
                    logger.error("zip_file_read_error", path=path, error=str(e))

    except zipfile.BadZipFile:
        raise ValueError("Invalid ZIP file")
    except Exception as e:
        logger.error("zip_extraction_error", error=str(e))
        raise

    project_name = filename.rsplit(".", 1)[0] if "." in filename else filename
    
    return ProjectContext(
        project_name=project_name,
        files=files_content,
        file_tree=file_tree,
        readme_content=readme_content,
        languages=[] # Could be inferred from extensions if needed
    )
