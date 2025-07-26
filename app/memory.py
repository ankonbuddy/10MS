from typing import List, Dict

class ShortTermMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history: List[Dict] = []

    def add(self, user: str, message: str):
        self.history.append({'user': user, 'message': message})
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_history(self) -> List[Dict]:
        return self.history 