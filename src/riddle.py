class Riddle:

    def __init__(self, pk: int, riddle: str, answers: list):
        self.pk = pk
        self.riddle = riddle
        self.answers = answers

    def riddle(self):
        return self.riddle

    def answers(self):
        return self.answers

    def check(self, value):
        if value in self.answers:
            return True

    def __str__(self):
        return f"'current_riddle': {self.riddle}, 'answers': {self.answers}"
