"""
Ruler Skills Core Module

This module provides the core infrastructure for loading and managing skills.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
import re
import yaml
from dataclasses import dataclass
from .registry import SkillRegistry


@dataclass
class Skill:
    """Represents a single skill."""

    id: str
    name: str
    category: str
    description: str
    triggers: List[str]
    content: str

    def matches(self, query: str) -> float:
        """Calculate how well this skill matches a query.

        Returns a score from 0.0 to 1.0.
        """
        query_lower = query.lower()
        score = 0.0

        # Check triggers (highest weight)
        for trigger in self.triggers:
            trigger_lower = trigger.lower()
            if trigger_lower in query_lower:
                score = max(score, 0.9)
            elif query_lower in trigger_lower:
                score = max(score, 0.7)

        # Check name
        if query_lower in self.name.lower():
            score = max(score, 0.6)

        # Check description
        if query_lower in self.description.lower():
            score = max(score, 0.3)

        return score


class SkillLoader:
    """Loads and manages Ruler skills."""

    def __init__(self, skills_dir: Path):
        """Initialize the skill loader.

        Args:
            skills_dir: Path to the skills directory
        """
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self._load_all()

    def _load_all(self):
        """Load all skills from the skills directory."""
        if not self.skills_dir.exists():
            return

        for category_dir in self.skills_dir.iterdir():
            if not category_dir.is_dir():
                continue
            if category_dir.name.startswith("_"):
                continue

            for skill_file in category_dir.glob("*.md"):
                skill = self._load_skill(skill_file)
                if skill:
                    self.skills[skill.id] = skill

    def _load_skill(self, path: Path) -> Optional[Skill]:
        """Load a single skill from a markdown file.

        Args:
            path: Path to the skill markdown file

        Returns:
            Skill object or None if loading failed
        """
        try:
            content = path.read_text(encoding="utf-8")

            # Parse frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                else:
                    frontmatter = {}
                    body = content
            else:
                frontmatter = {}
                body = content

            return Skill(
                id=f"{path.parent.name}/{path.stem}",
                name=frontmatter.get("name", path.stem.replace("-", " ").title()),
                category=path.parent.name,
                description=frontmatter.get("description", ""),
                triggers=frontmatter.get("triggers", []),
                content=body,
            )
        except Exception as e:
            print(f"Warning: Failed to load skill from {path}: {e}")
            return None

    def find_skill(self, query: str) -> Optional[Skill]:
        """Find the best matching skill for a query.

        Args:
            query: The user's query or task description

        Returns:
            The best matching skill or None
        """
        best_match = None
        best_score = 0.0

        for skill in self.skills.values():
            score = skill.matches(query)
            if score > best_score:
                best_score = score
                best_match = skill

        # Only return if score is above threshold
        if best_score >= 0.3:
            return best_match
        return None

    def find_skills(self, query: str, max_results: int = 5) -> List[Skill]:
        """Find all skills matching a query.

        Args:
            query: The user's query
            max_results: Maximum number of results to return

        Returns:
            List of matching skills sorted by relevance
        """
        matches = []
        for skill in self.skills.values():
            score = skill.matches(query)
            if score > 0:
                matches.append((score, skill))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [skill for _, skill in matches[:max_results]]

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a specific skill by ID.

        Args:
            skill_id: The skill ID (e.g., "components/button-patterns")

        Returns:
            The skill or None
        """
        return self.skills.get(skill_id)

    def list_skills(self, category: Optional[str] = None) -> List[Skill]:
        """List all skills, optionally filtered by category.

        Args:
            category: Optional category to filter by

        Returns:
            List of skills
        """
        if category:
            return [s for s in self.skills.values() if s.category == category]
        return list(self.skills.values())

    def list_categories(self) -> Set[str]:
        """Get all available categories.

        Returns:
            Set of category names
        """
        return {s.category for s in self.skills.values()}

    def get_skill_prompt(self, skill_id: str) -> str:
        """Get the full prompt content for a skill.

        Args:
            skill_id: The skill ID

        Returns:
            The skill content as a prompt string
        """
        skill = self.get_skill(skill_id)
        if not skill:
            return ""

        return f"""# {skill.name}

{skill.content}

---
Category: {skill.category}
Description: {skill.description}
"""


# Global instance (initialized lazily)
_loader: Optional[SkillLoader] = None


def get_skill_loader(skills_dir: Optional[Path] = None) -> SkillLoader:
    """Get or create the global skill loader instance.

    Args:
        skills_dir: Path to skills directory. Uses default if not provided.

    Returns:
        SkillLoader instance
    """
    global _loader
    if _loader is None:
        if skills_dir is None:
            # Default path - will be configured via environment
            import os

            skills_dir = Path(os.environ.get("RULER_SKILLS_PATH", "./skills"))
        _loader = SkillLoader(skills_dir)
    return _loader


def load_skill(query: str) -> str:
    """Load the best matching skill for a query.

    This is the main entry point for MCP integration.

    Args:
        query: The user's query or task description

    Returns:
        Formatted skill content or "No matching skill found."
    """
    loader = get_skill_loader()
    skill = loader.find_skill(query)

    if skill:
        return f"""# {skill.name}

{skill.content}

---
*Category: {skill.category}*
*Trigger phrases: {", ".join(skill.triggers[:3])}*
"""
    else:
        # Try to find related skills
        related = loader.find_skills(query, max_results=3)
        if related:
            suggestions = "\n".join([f"- {s.name} ({s.category})" for s in related])
            return f"""No exact match found. 

Related skills:
{suggestions}

Try a different query or browse skills by category."""

        return "No matching skill found. Try describing your task differently."
