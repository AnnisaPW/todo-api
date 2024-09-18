from typing import Optional


class Todo:
    def __init__(
        self,
        title,
        description,
        is_completed=True,
        id: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
