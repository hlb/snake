import pygame
import random
import sys
import os
from pygame import mixer

# 初始化 Pygame
pygame.init()

# 初始化音效系統
pygame.mixer.quit()  # 先關閉可能已經在運行的音效系統
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(8)  # 設置更多聲道

# 載入音效
def load_sound(file_path):
    if not os.path.exists(file_path):
        print(f"找不到音效文件: {file_path}")
        return None
    try:
        sound = pygame.mixer.Sound(file_path)
        print(f"成功載入音效: {file_path}")
        return sound
    except Exception as e:
        print(f"載入音效文件失敗 {file_path}: {str(e)}")
        return None

# 設置音效
eat_sound = load_sound('sounds/eat.wav')
crash_sound = load_sound('sounds/crash.wav')
background_music = load_sound('sounds/background.wav')

# 設置音量
if eat_sound:
    eat_sound.set_volume(0.4)
if crash_sound:
    crash_sound.set_volume(0.3)
if background_music:
    background_music.set_volume(0.8)  # 增加音量到 0.8
    channel = pygame.mixer.Channel(0)
    channel.set_volume(0.8)  # 增加通道音量到 0.8
    try:
        channel.play(background_music, loops=-1)
        print("背景音樂開始播放")
    except Exception as e:
        print(f"播放背景音樂失敗: {str(e)}")

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (40, 44, 52)
GRID_COLOR = (50, 54, 62)
SNAKE_COLOR = (152, 195, 121)
FOOD_COLOR = (224, 108, 117)
SCORE_COLOR = (229, 192, 123)
GAME_OVER_COLOR = (224, 108, 117)
OBSTACLE_COLOR = (97, 175, 239)

# 遊戲設置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10
OBSTACLE_COUNT = 5  # 障礙物數量

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 設置字體
def get_font(size):
    # macOS 系統字體路徑
    system_fonts = [
        '/System/Library/Fonts/PingFang.ttc',  # PingFang
        '/System/Library/Fonts/STHeiti Light.ttc',  # Heiti
        '/System/Library/Fonts/Hiragino Sans GB.ttc'  # Hiragino
    ]
    
    # 嘗試載入系統字體
    for font_path in system_fonts:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # 如果找不到中文字體，使用默認字體
    return pygame.font.Font(None, size)

# 創建遊戲窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('現代風格貪食蛇')
clock = pygame.time.Clock()

def draw_rounded_rect(surface, color, rect, radius):
    """繪製圓角矩形"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_grid():
    """繪製背景網格"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

class Obstacle:
    def __init__(self):
        self.positions = set()
        self.color = OBSTACLE_COLOR
        self.generate_obstacles()

    def generate_obstacles(self):
        self.positions.clear()
        # 生成指定數量的障礙物
        while len(self.positions) < OBSTACLE_COUNT:
            pos = (random.randint(2, GRID_WIDTH-3), 
                  random.randint(2, GRID_HEIGHT-3))
            # 確保障礙物不會生成在蛇的初始位置附近
            if pos[0] < GRID_WIDTH//2-2 or pos[0] > GRID_WIDTH//2+2 or \
               pos[1] < GRID_HEIGHT//2-2 or pos[1] > GRID_HEIGHT//2+2:
                self.positions.add(pos)

    def render(self):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE + 1,
                             pos[1] * GRID_SIZE + 1,
                             GRID_SIZE - 2, GRID_SIZE - 2)
            draw_rounded_rect(screen, self.color, rect, 3)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = SNAKE_COLOR
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self, obstacles):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        # 檢查是否撞到障礙物
        if new in obstacles.positions:
            if crash_sound:
                crash_sound.play()
            return False
        
        # 檢查是否撞到自己
        if new in self.positions[3:]:
            if crash_sound:
                crash_sound.play()
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self):
        for i, p in enumerate(self.positions):
            radius = 8 if i == 0 else 5  # 蛇頭較大
            rect = pygame.Rect(p[0] * GRID_SIZE + 1, p[1] * GRID_SIZE + 1,
                             GRID_SIZE - 2, GRID_SIZE - 2)
            draw_rounded_rect(screen, self.color, rect, radius)

class Food:
    def __init__(self, obstacles):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.obstacles = obstacles
        self.randomize_position()

    def randomize_position(self):
        while True:
            self.position = (random.randint(0, GRID_WIDTH-1), 
                           random.randint(0, GRID_HEIGHT-1))
            # 確保食物不會出現在障礙物上
            if self.position not in self.obstacles.positions:
                break

    def render(self):
        rect = pygame.Rect(self.position[0] * GRID_SIZE + 1,
                         self.position[1] * GRID_SIZE + 1,
                         GRID_SIZE - 2, GRID_SIZE - 2)
        draw_rounded_rect(screen, self.color, rect, 8)

def show_game_over(screen, score):
    """顯示遊戲結束畫面"""
    font_big = get_font(72)
    font_small = get_font(36)
    
    game_over_text = font_big.render('遊戲結束', True, GAME_OVER_COLOR)
    score_text = font_small.render(f'最終分數: {score}', True, SCORE_COLOR)
    restart_text = font_small.render('按空格鍵重新開始', True, WHITE)
    
    screen.blit(game_over_text, 
                (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                 WINDOW_HEIGHT//2 - 60))
    screen.blit(score_text, 
                (WINDOW_WIDTH//2 - score_text.get_width()//2, 
                 WINDOW_HEIGHT//2))
    screen.blit(restart_text, 
                (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                 WINDOW_HEIGHT//2 + 60))

def main():
    snake = Snake()
    obstacles = Obstacle()
    food = Food(obstacles)
    font = get_font(36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if background_music:
                    background_music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        obstacles.generate_obstacles()
                        food.randomize_position()
                        game_over = False
                        if background_music:
                            pygame.mixer.Channel(0).play(background_music, -1)
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            if not snake.update(obstacles):
                game_over = True
                if background_music:
                    background_music.stop()
            
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
                if eat_sound:
                    eat_sound.play()

        # 繪製
        screen.fill(BACKGROUND)
        draw_grid()
        obstacles.render()
        snake.render()
        food.render()
        
        # 顯示分數
        score_text = font.render(f'分數: {snake.score}', True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))

        if game_over:
            show_game_over(screen, snake.score)

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == '__main__':
    main()
