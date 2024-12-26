import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // 2 // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),    # 红色
    (0, 255, 0),    # 绿色
    (0, 0, 255),    # 蓝色
    (255, 255, 0),  # 黄色
    (255, 0, 255),  # 紫色
    (0, 255, 255),  # 青色
    (255, 128, 0)   # 橙色
]

# 俄罗斯方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I型
    [[1, 1], [1, 1]],  # 方块
    [[1, 1, 1], [0, 1, 0]],  # T型
    [[1, 1, 0], [0, 1, 1]],  # Z型
    [[0, 1, 1], [1, 1, 0]],  # S型
    [[1, 1, 1], [1, 0, 0]],  # L型
    [[1, 1, 1], [0, 0, 1]]   # 反L型
]

class Tetris:
    def __init__(self):
        # 设置游戏窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.reset_game()
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_shape = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        
        # 字体
        self.font = pygame.font.SysFont('simsun', 36)
        
        # 生成第一个方块
        self.new_shape()
    
    def new_shape(self):
        # 随机选择形状和颜色
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_shape = SHAPES[shape_index]
        self.current_color = COLORS[shape_index]
        
        # 从顶部中间开始
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        
        # 检查是否游戏结束
        if self.check_collision():
            self.game_over = True
    
    def draw_grid(self):
        self.screen.fill(BLACK)
        
        # 绘制背景网格
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(
                    x * GRID_SIZE, 
                    y * GRID_SIZE, 
                    GRID_SIZE - 1, 
                    GRID_SIZE - 1
                )
                pygame.draw.rect(self.screen, GRAY, rect, 1)
        
        # 绘制已经固定的方块
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        x * GRID_SIZE, 
                        y * GRID_SIZE, 
                        GRID_SIZE - 1, 
                        GRID_SIZE - 1
                    )
                    pygame.draw.rect(self.screen, cell, rect)
        
        # 绘制当前方块
        if self.current_shape:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            (self.current_x + x) * GRID_SIZE,
                            (self.current_y + y) * GRID_SIZE,
                            GRID_SIZE - 1,
                            GRID_SIZE - 1
                        )
                        pygame.draw.rect(self.screen, self.current_color, rect)
        
        # 绘制分数
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 + 50, 50))
        
        # 游戏结束提示
        if self.game_over:
            game_over_text = self.font.render('游戏结束', True, WHITE)
            restart_text = self.font.render('按 R 重新开始', True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50))
    
    def move(self, dx, dy):
        # 尝试移动方块
        self.current_x += dx
        self.current_y += dy
        
        # 如果发生碰撞，撤销移动
        if self.check_collision():
            self.current_x -= dx
            self.current_y -= dy
            
            # 如果是向下移动，说明方块已经落地
            if dy > 0:
                self.freeze_shape()
                self.clear_lines()
                self.new_shape()
    
    def rotate(self):
        # 旋转方块
        rotated_shape = list(zip(*self.current_shape[::-1]))
        
        # 保存原始位置
        original_x = self.current_x
        original_shape = self.current_shape
        
        # 尝试旋转
        self.current_shape = rotated_shape
        
        # 如果旋转后发生碰撞，恢复原状
        if self.check_collision():
            self.current_shape = original_shape
            self.current_x = original_x
    
    def check_collision(self):
        # 检查方块是否与边界或其他方块碰撞
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_x + x
                    grid_y = self.current_y + y
                    
                    # 检查边界
                    if (grid_x < 0 or grid_x >= GRID_WIDTH or 
                        grid_y >= GRID_HEIGHT):
                        return True
                    
                    # 检查是否与已有方块重叠
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        
        return False
    
    def freeze_shape(self):
        # 将当前方块固定到网格
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_x + x
                    grid_y = self.current_y + y
                    
                    if 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = self.current_color
    
    def clear_lines(self):
        # 消除已经填满的行
        full_lines = [y for y, row in enumerate(self.grid) if all(row)]
        
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.score += 10
    
    def run(self):
        fall_time = 0
        fall_speed = 0.5  # 控制方块下落速度
        
        while True:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate()
                    
                    # 重新开始游戏
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
            
            # 自动下落
            if not self.game_over:
                current_time = pygame.time.get_ticks()
                if current_time - fall_time > fall_speed * 1000:
                    self.move(0, 1)
                    fall_time = current_time
            
            # 绘制
            self.draw_grid()
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)

def main():
    game = Tetris()
    game.run()

if __name__ == "__main__":
    main()
