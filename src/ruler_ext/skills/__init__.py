"""
Skills Module

Integrates the skill system with MCP.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Skill:
    """Represents a skill."""

    id: str
    name: str
    category: str
    description: str
    triggers: List[str]
    content: str


class SkillLoader:
    """Loads and manages skills."""

    def __init__(self, skills_dir: Path):
        """Initialize the skill loader."""
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self._load_all()

    def _load_all(self):
        """Load all skills from the directory."""
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
        """Load a skill from a markdown file."""
        try:
            content = path.read_text(encoding="utf-8")

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

    def _score_skill(self, skill: Skill, query: str) -> float:
        """Calculate how well a skill matches a query."""
        query_lower = query.lower()
        score = 0.0

        for trigger in skill.triggers:
            trigger_lower = trigger.lower()
            if trigger_lower in query_lower:
                score = max(score, 0.9)
            elif query_lower in trigger_lower:
                score = max(score, 0.7)

        if query_lower in skill.name.lower():
            score = max(score, 0.6)

        if query_lower in skill.description.lower():
            score = max(score, 0.3)

        return score

    def find_skill(self, query: str) -> Optional[Skill]:
        """Find the best matching skill for a query."""
        best_match = None
        best_score = 0.0

        for skill in self.skills.values():
            score = self._score_skill(skill, query)
            if score > best_score:
                best_score = score
                best_match = skill

        if best_score >= 0.3:
            return best_match
        return None

    def find_skills(self, query: str, max_results: int = 5) -> List[Skill]:
        """Find all skills matching a query."""
        matches = []
        for skill in self.skills.values():
            score = self._score_skill(skill, query)
            if score > 0:
                matches.append((score, skill))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [skill for _, skill in matches[:max_results]]

    def list_skills(self, category: Optional[str] = None) -> List[Skill]:
        """List all skills, optionally filtered by category."""
        if category:
            return [s for s in self.skills.values() if s.category == category]
        return list(self.skills.values())

    def load_skill(self, query: str) -> str:
        """Load the best matching skill for a query."""
        skill = self.find_skill(query)

        if skill:
            return f"""# {skill.name}

{skill.content}

---
*Category: {skill.category}*
*Trigger phrases: {", ".join(skill.triggers[:3])}*
"""
        else:
            related = self.find_skills(query, max_results=3)
            if related:
                suggestions = "\n".join([f"- {s.name} ({s.category})" for s in related])
                return f"""No exact match found.

Related skills:
{suggestions}

Try a different query or browse skills by category."""

            return "No matching skill found. Try describing your task differently."
