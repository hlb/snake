import pygame
import random
import sys
import os
from pygame import mixer
from pygame_emojis import load_emoji

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
GRID_SIZE = 40
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
INITIAL_SPEED = 6  # 初始速度
SPEED_INCREMENT = 1  # 每 10 分增加的速度
OBSTACLE_COUNT = 3

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
        self.generate_obstacles(OBSTACLE_COUNT)  # 初始障礙物數量

    def generate_obstacles(self, count):
        """生成指定數量的障礙物"""
        self.positions.clear()
        while len(self.positions) < count:
            pos = (random.randint(2, GRID_WIDTH-3), 
                  random.randint(2, GRID_HEIGHT-3))
            # 確保障礙物不會生成在蛇的初始位置附近
            if pos[0] < GRID_WIDTH//2-2 or pos[0] > GRID_WIDTH//2+2 or \
               pos[1] < GRID_HEIGHT//2-2 or pos[1] > GRID_HEIGHT//2+2:
                self.positions.add(pos)

    def add_obstacle(self, snake):
        """添加一個新的障礙物，避免放在蛇的正前方"""
        head = snake.get_head_position()
        direction = snake.direction
        
        # 計算蛇頭前方的三個格子位置
        danger_positions = set()
        x, y = head
        dx, dy = direction
        for i in range(3):  # 檢查前方 3 格
            x = (x + dx) % GRID_WIDTH
            y = (y + dy) % GRID_HEIGHT
            danger_positions.add((x, y))
            # 添加左右兩側的格子
            danger_positions.add(((x + dy) % GRID_WIDTH, (y - dx) % GRID_HEIGHT))  # 左側
            danger_positions.add(((x - dy) % GRID_WIDTH, (y + dx) % GRID_HEIGHT))  # 右側

        # 嘗試放置新障礙物
        attempts = 100  # 最大嘗試次數
        while attempts > 0:
            pos = (random.randint(0, GRID_WIDTH-1), 
                  random.randint(0, GRID_HEIGHT-1))
            
            # 檢查是否符合所有條件：
            # 1. 不在蛇身上
            # 2. 不在其他障礙物上
            # 3. 不在危險區域內
            # 4. 不在食物上
            if (pos not in snake.positions and 
                pos not in self.positions and 
                pos not in danger_positions):
                self.positions.add(pos)
                break
            attempts -= 1

    def render(self):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE + 2,
                             pos[1] * GRID_SIZE + 2,
                             GRID_SIZE - 4, GRID_SIZE - 4)
            draw_rounded_rect(screen, self.color, rect, 10)

class Snake:
    def __init__(self):
        """Initialize a new snake with default settings."""
        self.score = 0
        self.speed = INITIAL_SPEED
        self.color = SNAKE_COLOR
        self._initialize_snake()
    
    def _initialize_snake(self):
        """Initialize or reset snake's position and length."""
        self.length = 3
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # Start at center
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [center]
        # Add body segments behind head based on direction
        dx, dy = self.direction
        for i in range(1, self.length):
            self.positions.append((
                (center[0] - dx * i) % GRID_WIDTH,
                (center[1] - dy * i) % GRID_HEIGHT
            ))

    def get_head_position(self):
        """Return the position of snake's head."""
        return self.positions[0]

    def _check_collision(self, new_pos, obstacles):
        """Check if the new position results in a collision.
        
        Args:
            new_pos: Tuple of (x, y) for the new head position
            obstacles: Obstacle object containing obstacle positions
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        # Check obstacle collision
        if new_pos in obstacles.positions:
            if crash_sound:
                crash_sound.play()
            return True
            
        # Check self collision (excluding head)
        if new_pos in self.positions[1:]:
            if crash_sound:
                crash_sound.play()
            return True
            
        return False

    def update(self, obstacles):
        """Update snake position and check for collisions.
        
        Args:
            obstacles: Obstacle object containing obstacle positions
            
        Returns:
            bool: True if collision occurred, False otherwise
        """
        # Calculate new head position
        cur = self.get_head_position()
        dx, dy = self.direction
        new_pos = ((cur[0] + dx) % GRID_WIDTH, (cur[1] + dy) % GRID_HEIGHT)
        
        # Check for collisions
        if self._check_collision(new_pos, obstacles):
            return True
        
        # Update snake length based on score
        self.length = 3 + self.score
        
        # Move snake by adding new head
        self.positions.insert(0, new_pos)
        
        # Remove tail if we haven't grown
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return False

    def reset(self):
        """Reset snake to initial state."""
        self.score = 0
        self.speed = INITIAL_SPEED
        self._initialize_snake()

    def render(self):
        """Render the snake on the screen."""
        for i, pos in enumerate(self.positions):
            radius = 12 if i == 0 else 8  # Larger radius for head
            rect = pygame.Rect(
                pos[0] * GRID_SIZE + 2,
                pos[1] * GRID_SIZE + 2,
                GRID_SIZE - 4, 
                GRID_SIZE - 4
            )
            draw_rounded_rect(screen, self.color, rect, radius)

class Food:
    def __init__(self, obstacles):
        self.position = (0, 0)
        self.obstacles = obstacles
        self.food_emojis = ['🍕', '🍇', '🍪', '🍓', '🍎', '🍮', '🍜']
        self.emoji = random.choice(self.food_emojis)
        # Load the emoji surface
        self.emoji_surface = load_emoji(self.emoji, (GRID_SIZE - 4, GRID_SIZE - 4))
        self.randomize_position()

    def randomize_position(self):
        while True:
            self.position = (random.randint(0, GRID_WIDTH-1), 
                           random.randint(0, GRID_HEIGHT-1))
            # 確保食物不會出現在障礙物上
            if self.position not in self.obstacles.positions:
                # Change to a new random food emoji
                self.emoji = random.choice(self.food_emojis)
                self.emoji_surface = load_emoji(self.emoji, (GRID_SIZE - 4, GRID_SIZE - 4))
                break

    def render(self):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        # Center the emoji in the grid cell
        rect = self.emoji_surface.get_rect(center=(x + GRID_SIZE//2, y + GRID_SIZE//2))
        screen.blit(self.emoji_surface, rect)

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
                        obstacles.generate_obstacles(OBSTACLE_COUNT)  # 重置為初始數量
                        food.randomize_position()
                        game_over = False
                        if background_music:
                            pygame.mixer.Channel(0).play(background_music, loops=-1)
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
            if snake.update(obstacles):  # Removed the 'not' operator
                game_over = True
                if background_music:
                    background_music.stop()
            
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                # 每得到 10 分增加速度和障礙物
                if snake.score % 10 == 0:
                    snake.speed += SPEED_INCREMENT
                    obstacles.add_obstacle(snake)  # 添加新障礙物
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
        clock.tick(snake.speed)  # 使用蛇的當前速度

if __name__ == '__main__':
    main()
