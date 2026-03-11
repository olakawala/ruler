"""
Skill Registry Module

Provides skill registration and indexing functionality.
"""

from typing import Dict, List, Optional, Set
from collections import defaultdict
from dataclasses import dataclass
from .loader import Skill


@dataclass
class SkillIndex:
    """Index for fast skill lookup."""

    by_trigger: Dict[str, List[str]]  # trigger phrase -> skill IDs
    by_category: Dict[str, List[str]]  # category -> skill IDs
    by_name: Dict[str, str]  # lowercase name -> skill ID


class SkillRegistry:
    """Registry for managing skill metadata and indexes."""

    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.index = SkillIndex(
            by_trigger=defaultdict(list), by_category=defaultdict(list), by_name={}
        )

    def register(self, skill: Skill):
        """Register a skill.

        Args:
            skill: The skill to register
        """
        self.skills[skill.id] = skill

        # Index by triggers
        for trigger in skill.triggers:
            trigger_lower = trigger.lower()
            self.index.by_trigger[trigger_lower].append(skill.id)

        # Index by category
        self.index.by_category[skill.category].append(skill.id)

        # Index by name
        self.index.by_name[skill.name.lower()] = skill.id

    def get(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        return self.skills.get(skill_id)

    def find_by_trigger(self, trigger: str) -> List[Skill]:
        """Find skills by trigger phrase."""
        trigger_lower = trigger.lower()
        results = []

        for t, skill_ids in self.index.by_trigger.items():
            if trigger_lower in t or t in trigger_lower:
                for sid in skill_ids:
                    if sid not in results:
                        results.append(self.skills[sid])

        return results

    def find_by_category(self, category: str) -> List[Skill]:
        """Find all skills in a category."""
        skill_ids = self.index.by_category.get(category, [])
        return [self.skills[sid] for sid in skill_ids]

    def get_categories(self) -> Set[str]:
        """Get all categories."""
        return set(self.index.by_category.keys())

    def search(self, query: str) -> List[Skill]:
        """Search skills by query."""
        query_lower = query.lower()
        results = []

        for skill in self.skills.values():
            score = 0

            # Check triggers
            for trigger in skill.triggers:
                if query_lower in trigger.lower():
                    score += 3
                elif trigger.lower() in query_lower:
                    score += 2

            # Check name
            if query_lower in skill.name.lower():
                score += 2

            # Check description
            if query_lower in skill.description.lower():
                score += 1

            if score > 0:
                results.append((score, skill))

        results.sort(key=lambda x: x[0], reverse=True)
        return [skill for _, skill in results]
