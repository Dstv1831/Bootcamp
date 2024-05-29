import time
from turtle import Screen
from snake import Snake
from food import Food
from score import Score

screen = Screen()
screen.setup(600, 600)
screen.title("Snake Game")
screen.bgcolor('beige')
screen.tracer(0)  # turns the screen update off
points = 0
game = True
# todo 1 - Create snake by joining three squares one next to the other
snake = Snake()
food = Food()
score = Score()
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# todo 2 - Animating the snake automatically,
#  by moving each segment to the position of the next one
#  in line, meanwhile pushing the first one forwards.
while game:
    screen.update()
    time.sleep(0.09)
    snake.move()

# todo 3 - Detect collision with the food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extent()
        score.plus()
# todo 4 - Detect collision with the wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        score.reset()
        snake.reset()
# todo 5 - Detect collision with the tail
    for segment in snake.segments[1:]:  # Slicing a list on python list[ and tuples
        if snake.head.distance(segment) < 10:
            score.reset()
            snake.reset()

screen.exitonclick()
