import pygame
import random
import sys
import os

# 初始化 Pygame
pygame.init()

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (40, 44, 52)
GRID_COLOR = (50, 54, 62)
SNAKE_COLOR = (152, 195, 121)
FOOD_COLOR = (224, 108, 117)
SCORE_COLOR = (229, 192, 123)
GAME_OVER_COLOR = (224, 108, 117)

# 遊戲設置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

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

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = SNAKE_COLOR
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
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
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), 
                        random.randint(0, GRID_HEIGHT-1))

    def render(self):
        rect = pygame.Rect(self.position[0] * GRID_SIZE + 1,
                         self.position[1] * GRID_SIZE + 1,
                         GRID_SIZE - 2, GRID_SIZE - 2)
        draw_rounded_rect(screen, self.color, rect, 8)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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
    food = Food()
    font = get_font(36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
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
            if not snake.update():
                game_over = True
            
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

        # 繪製
        screen.fill(BACKGROUND)
        draw_grid()
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
