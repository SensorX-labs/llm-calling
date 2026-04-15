"""Prompt building service."""
from typing import Dict, List, Optional


class PromptBuilder:
    """Build and format prompts for LLM."""

    def __init__(self):
        """Initialize prompt builder."""
        self.system_prompt: Optional[str] = None
        self.template_vars: Dict[str, str] = {}

    def set_system_prompt(self, prompt: str) -> "PromptBuilder":
        """Set system prompt."""
        self.system_prompt = prompt
        return self

    def add_variables(self, variables: Dict[str, str]) -> "PromptBuilder":
        """Add template variables."""
        self.template_vars.update(variables)
        return self

    def build(self, user_prompt: str) -> str:
        """
        Build final prompt.

        Args:
            user_prompt: User input prompt

        Returns:
            Formatted prompt string
        """
        prompt = user_prompt

        # Substitute template variables
        for key, value in self.template_vars.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        return prompt

    def build_with_context(
        self, user_prompt: str, context: Optional[List[str]] = None
    ) -> str:
        """
        Build prompt with context.

        Args:
            user_prompt: User input prompt
            context: List of context strings

        Returns:
            Formatted prompt with context
        """
        parts = []

        if self.system_prompt:
            parts.append(f"System: {self.system_prompt}")

        if context:
            parts.append("Context:")
            parts.extend(context)

        parts.append(f"User: {user_prompt}")

        return "\n\n".join(parts)
