from turtle import Turtle

ALIGNMENT = "center"
FONT = ('Comic sans MS', 15, 'normal')


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color('saddle brown')
        self.goto(0, 270)
        self.score = 0
        with open("data.txt") as data:
            self.highscore = int(data.read())
        print(self.highscore)
        self.update_score_board()

    def plus(self):
        self.score += 1
        self.update_score_board()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.highscore}")
        self.score = 0
        self.update_score_board()

    def update_score_board(self):
        self.clear()
        self.write(f'Score: {self.score} High Score: {self.highscore}', align=ALIGNMENT, font=FONT)
