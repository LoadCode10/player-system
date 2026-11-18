class SkillNotFound(Exception):
  def __init__(self, skill_id: int):
    self.skill_id = skill_id
    self.message = f"Skill with id '{skill_id}' was not found."
    super().__init__(self.message)

class SkillAlreadyExists(Exception):
  def __init__(self, name: str):
    self.name = name
    self.message = f"Skill with name '{name}' already exists."
    super().__init__(self.message)