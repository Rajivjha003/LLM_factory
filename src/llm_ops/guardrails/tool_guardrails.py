from typing import Dict, Any, Optional
from src.llm_ops.core.schemas import GuardrailResult, ToolCall
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def check_tool_guardrails(tool_call: ToolCall) -> GuardrailResult:
    if not settings.guardrail.guardrails_enabled:
        return GuardrailResult(passed=True, action_taken="allow")
        
    logger.debug(f"Checking tool guardrails for {tool_call.tool_name}")
    
    # Block all write tools if setting is off
    if not settings.mcp.mcp_allow_write_tools or not settings.security.allow_prod_write:
        # Simplistic check: if tool name implies writing
        if any(word in tool_call.tool_name.lower() for word in ["write", "update", "delete", "create", "insert"]):
            return GuardrailResult(
                passed=False, 
                reason=f"Write tools are disabled. Blocked: {tool_call.tool_name}", 
                action_taken="block"
            )
            
    # Check shell tools
    if not settings.security.allow_shell_tools:
        if "shell" in tool_call.tool_name.lower() or "cmd" in tool_call.tool_name.lower():
            return GuardrailResult(
                passed=False, 
                reason=f"Shell tools are disabled. Blocked: {tool_call.tool_name}", 
                action_taken="block"
            )

    return GuardrailResult(passed=True, action_taken="allow")
