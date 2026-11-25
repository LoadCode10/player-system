import enum

class Rank(str, enum.Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"

class QuestStatus(str, enum.Enum): 
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    CLEARED = "cleared"