"""
Ruler Skills Package

A collection of skills for AI-assisted design with Penpot.
"""

from .loader import SkillLoader, Skill, get_skill_loader, load_skill
from .registry import SkillRegistry

__all__ = [
    "SkillLoader",
    "Skill",
    "SkillRegistry",
    "get_skill_loader",
    "load_skill",
]

__version__ = "1.0.0"
