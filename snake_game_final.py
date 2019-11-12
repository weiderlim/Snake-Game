# ============================             MODULES              ===============================

import random, pygame

# ============================             CLASSES              ===============================

class Snake(object):
    def __init__(self):
        self.position_head = [250, 250]
        self.position_body = [[250, 250], [250, 260], [250, 270]]
        self.direction = "U"
        self.food_is_eaten = False

    def move_and_grow(self):
        """ Define movement of the head of the snake and grow when the food is eaten."""
        if self.direction == "R":
            self.position_head[0] += 10
        if self.direction == "L":
            self.position_head[0] -= 10
        if self.direction == "U":
            self.position_head[1] -= 10
        if self.direction == "D":
            self.position_head[1] += 10

        # insert at the position of the head; when the head moves again this new insertion will be in place of the head as the back does not move to complete the body
        self.position_body.insert(0, list(self.position_head))
        if self.food_is_eaten == False:
            self.position_body.pop()
        self.food_is_eaten = False

    def check_food_eaten(self, position_food):
        """ Check if food is eaten. """
        if self.position_head == position_food:
            self.food_is_eaten = True
            return True
        return False
    
    def collision(self):
        """ Check for collision with walls or with own body. """
        if self.position_head[0] in [0, 500] or self.position_head[1] in [0, 500]:
            return True
        if self.position_head in self.position_body[1:]:
            return True
        return False

    def check_and_change_dir (self, dir):
        """ 
            Check whether the snake is trying to turn in the opposite to its original direction.    
            Do not allow if so.
        """
        if dir == "R" and self.direction != "L":
            self.direction = "R"
        if dir == "L" and self.direction != "R":
            self.direction = "L"
        if dir == "U" and self.direction != "D":
            self.direction = "U"
        if dir == "D" and self.direction != "U":
            self.direction = "D"

class Food(object):
    def __init__(self):
        self.position_food = [random.randrange(1,50)*10, random.randrange(1,50)*10]
        self.food_exist = False
    
    def spawn_food(self, snake_body):
        """ Check and spawn food if eaten/does not exist. """
        if self.food_exist == False:
            while self.position_food in snake_body:
                self.position_food = [random.randrange(1,50)*10, random.randrange(1,50)*10]
        self.food_exist = True
        return self.position_food
    
    def food_eaten(self):
        self.food_exist = False

def message_display(text, position):
    """ A message display function that blits the window with text"""
    global window
    # creating the font object/instance
    myfont = pygame.font.SysFont("Comic Sans MS", 20)
    # rendering text on the surface
    textSurface = myfont.render(text, True, (255, 255, 255))
    # blitting the surface onto the window
    window.blit(textSurface, position)
    pygame.display.update()    

# setup for pygame
pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")
fps = pygame.time.Clock()
    
# main game loop
def play_game():
    game_over = False
    score = 0
    restart_game = False
    
    # initiate object instances
    snake = Snake()
    food = Food()

    while not game_over:
        # handling game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.check_and_change_dir("R")
                if event.key == pygame.K_LEFT:
                    snake.check_and_change_dir("L")
                if event.key == pygame.K_UP:
                    snake.check_and_change_dir("U")
                if event.key == pygame.K_DOWN:
                    snake.check_and_change_dir("D")

        # handling game logic
        position_food = food.spawn_food(snake.position_body)
        snake.move_and_grow()

        # main interaction between the classes
        if snake.check_food_eaten(position_food):
            food.food_eaten()
            score += 1
        
        if snake.collision():
            game_over = True

        # handling game display
        window.fill((0, 0, 0))
        pygame.draw.rect(window, pygame.Color(0, 255, 0), pygame.Rect(position_food[0], position_food[1], 10, 10))
        for position_parts in snake.position_body:
            pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(position_parts[0], position_parts[1], 10, 10))
        
        if not game_over:
            message_display("Score {}".format(score), (0, 0))

        pygame.display.update()
        fps.tick(20)
    
    # after game over, prompt player to restart game
    message_display("You lost with score of {}. Try to improve it!".format(score), (0, 0))
    message_display("Press R to restart or ESC to quit.", (0, 30))
    
    while not restart_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    play_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

play_game()


