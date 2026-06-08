from typing import List, Dict, Any, Optional
import re
from src.llm_ops.core.exceptions import GuardrailViolation
from src.llm_ops.core.schemas import GuardrailResult

class Policy:
    # SQL Policies
    ALLOWED_SQL_PREFIXES = ["SELECT", "WITH", "EXPLAIN", "SHOW"]
    BLOCKED_SQL_KEYWORDS = [
        "DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE", 
        "MERGE", "CREATE", "GRANT", "REVOKE"
    ]
    
    # Tool Policies
    MAX_TOOL_ROWS = 1000
    MAX_TOOL_BYTES = 1000000000
    
    # Prompt Injection Keywords
    PROMPT_INJECTION_KEYWORDS = [
        "ignore previous", "disregard previous", "system prompt", 
        "you are a developer", "forget all", "bypass"
    ]
    
    # File Search Policies
    ALLOWED_REPO_EXTENSIONS = [".py", ".md", ".sql", ".json", ".yaml", ".txt"]
    BLOCKED_DIRS = [".git", "node_modules", ".venv", "__pycache__"]
    
    # Global System Settings
    ALLOW_PROD_WRITE = False
