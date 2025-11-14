from .general_service import (
    list_all_generals, get_general_by_id, get_generals_by_name, 
    add_general, update_general, delete_general
)
from .skill_service import (
    list_all_skills, get_skill_by_id, add_skill, update_skill, delete_skill
)

__all__ = [
    'list_all_generals', 'get_general_by_id', 'get_generals_by_name',
    'add_general', 'update_general', 'delete_general',
    'list_all_skills', 'get_skill_by_id', 'add_skill', 'update_skill', 'delete_skill'
]