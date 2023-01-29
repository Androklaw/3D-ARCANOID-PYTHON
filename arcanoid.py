from ursina import *
from objects import *

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.borderless = False
        DirectionalLight(color=(0.5, 0.5, 0.5, 0.5, 1)).look_at(Vec3(1, -1, 1))
        DirectionalLight(color=(0.5, 0.5, 0.5, 0.5, 1)).look_at(Vec3(-1, -1, 1))
        AmbientLight(color=(0.5, 0.5, 0.5, 0.5, 1))
        self.MAP_SIZE = 24
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -28.5, -38)
        camera.rotation_x = -47
        self.ball_direction_x = 1
        self.ball_direction_y = 1

    def create_map(self, MAP_SIZE):
        self.sky_texture = load_texture("skybox.png")
        Entity(model='cube', scale=(self.MAP_SIZE + 0.2, 0.6, 0.6),
               position=(self.MAP_SIZE // 2, self.MAP_SIZE + 0.7, 0.3), color=color.dark_gray)
        Entity(model='cube', scale=(0.6, self.MAP_SIZE, 0.6),
               position=(-0.4, self.MAP_SIZE // 2 + 1, 0.3), color=color.dark_gray)
        Entity(model='cube', scale=(0.6, self.MAP_SIZE, 0.6),
               position=(self.MAP_SIZE + 0.4, self.MAP_SIZE // 2 + 1, 0.3), color=color.dark_gray)
        self.sky = Entity(parent=scene, model='quad', texture=self.sky_texture, scale=250, double_sided=True, rotation=(7, 0, 0), position=(0, 0, 15))

    def new_game(self):
        scene.clear()
        self.ball_direction_y = 1
        self.ball_direction_x = 1
        self.brick_texture = load_texture("brick.jpg")
        self.paddle_texture = load_texture("paddle.jpg")
        self.create_map(self.MAP_SIZE)
        self.bricks = [Bricks(self.MAP_SIZE, i, j, model='cube', texture=self.brick_texture, scale=(1.8, 0.9, 0.9), collider='box') for i in range(12) for j in range(5)]
        self.paddle = Paddle(self.MAP_SIZE, model='cube', texture=self.paddle_texture, scale=(5, 0.6, 0.6), collider='box')
        self.ball = Ball(self.MAP_SIZE, model='sphere', color=color.light_gray, scale=(0.8, 0.8, 0.8), collider='sphere')

    def detect_collision_bricks(self):
        for item in self.bricks:
            if self.ball.intersects(item).hit and item.y - 0.45 <= self.ball.y <= item.y + 0.45:
                self.ball_direction_x *= -1
                self.ball.x += self.ball_direction_x * 0.3
                destroy(self.bricks.pop(self.bricks.index(item)))
                break
            elif self.ball.intersects(item).hit and item.x - 2.5 <= self.ball.x <= item.x + 2.5:
                self.ball_direction_y *= -1
                self.ball.y += self.ball_direction_y * 0.3
                destroy(self.bricks.pop(self.bricks.index(item)))
                break
            elif self.ball.intersects(item).hit:
                self.ball_direction_x *= -1
                self.ball_direction_y *= -1
                self.ball.x += self.ball_direction_x * 0.3
                self.ball.y += self.ball_direction_y * 0.3
                destroy(self.bricks.pop(self.bricks.index(item)))
                break

    def detect_out_of_border(self):
        if self.ball.x + 0.1 > self.MAP_SIZE \
                or self.ball.y + 0.1 > self.MAP_SIZE \
                or self.ball.x - 0.1 < 0:
            self.new_game()

    def detect_collision_wall(self):
         if self.ball.x + 0.4 >= self.MAP_SIZE or self.ball.x - 0.4 <= 0:
             self.ball_direction_x *= -1
         if self.ball.y + 0.4 >= self.MAP_SIZE:
             self.ball_direction_y *= -1
         if self.ball.y - 0.4 <= 0:
             print_on_screen('GAME OVER', position=(-0.018, 0.004), scale=0.25, duration=1)
             invoke(self.new_game, delay=1)

    def detect_collision_paddle(self):
        if self.ball.intersects(self.paddle).hit and self.paddle.y - 0.3 <= self.ball.y <= self.paddle.y + 0.3:
            self.ball_direction_x *= -1
        elif self.ball.intersects(self.paddle).hit and self.paddle.x - 2.4 <= self.ball.x <= self.paddle.x + 2.4:
            self.ball_direction_y *= -1
        elif self.ball.intersects(self.paddle).hit:
            self.ball_direction_y *= -1
            self.ball_direction_x *= -1

    def if_win(self):
        if len(self.bricks) == 0:
            print_on_screen('YOU WON!', position=(-0.0159, 0.0036), scale=0.25, duration=1)
            self.ball_direction_y = 0
            self.ball_direction_x = 0
            invoke(application.quit, delay=2)

    def update(self):
        self.if_win()
        self.detect_collision_paddle()
        self.detect_collision_bricks()
        self.detect_out_of_border()
        self.detect_collision_wall()
        self.ball.x += self.ball_direction_x * time.dt * 5
        self.ball.y += self.ball_direction_y * time.dt * 5
        self.detect_collision_paddle()
        self.detect_collision_bricks()
        self.detect_out_of_border()
        self.detect_collision_wall()
        self.ball.x += self.ball_direction_x * time.dt * 5
        self.ball.y += self.ball_direction_y * time.dt * 5
        if self.paddle.x + 2.5 < self.MAP_SIZE - 0.3:
            self.paddle.x += held_keys['d'] * time.dt * 15
        if self.paddle.x - 2.5 > 0.3:
            self.paddle.x -= held_keys['a'] * time.dt * 15


if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
