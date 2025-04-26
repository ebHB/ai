import pygame
import sys
import random

# 初期化
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("改造テトリス")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ブロックの形状
BLOCK_SHAPES = [
    [[1, 1, 1, 1]],  # I字型
    [[1, 1], [1, 1]],  # O字型
    [[0, 1, 0], [1, 1, 1]],  # T字型
    [[1, 1, 0], [0, 1, 1]],  # S字型
    [[0, 1, 1], [1, 1, 0]],  # Z字型
    [[1, 0, 0], [1, 1, 1]],  # L字型
    [[0, 0, 1], [1, 1, 1]]   # J字型
]

class Block:
    def __init__(self):
        self.shape = random.choice(BLOCK_SHAPES)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.x = SCREEN_WIDTH // 2 // 30  # ブロックの初期位置（30はブロックサイズ）
        self.y = 0

    def draw(self, surface):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        pygame.Rect((self.x + col_index) * 30, (self.y + row_index) * 30, 30, 30)
                    )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # ブロックを回転させる（90度時計回り）
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class GameBoard:
    def __init__(self):
        self.width = SCREEN_WIDTH // 30
        self.height = SCREEN_HEIGHT // 30
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def add_block_to_grid(self, block):
        for row_index, row in enumerate(block.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_y = block.y + row_index
                    grid_x = block.x + col_index
                    if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
                        self.grid[grid_y][grid_x] = 1

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])
        self.grid = new_grid
        return lines_cleared

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        surface,
                        WHITE,
                        pygame.Rect(x * 30, y * 30, 30, 30)
                    )

# ゲームループ
def main():
    clock = pygame.time.Clock()
    running = True
    game_board = GameBoard()
    current_block = Block()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_block.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_block.move(0, 1)
                elif event.key == pygame.K_UP:
                    current_block.rotate()

        # ブロックが下に到達した場合
        reached_bottom = False
        for row_index, row in enumerate(current_block.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_y = current_block.y + row_index + 1
                    grid_x = current_block.x + col_index
                    if grid_y >= game_board.height or \
                       (0 <= grid_y < game_board.height and 0 <= grid_x < game_board.width and game_board.grid[grid_y][grid_x] == 1):
                        reached_bottom = True
                        break
            if reached_bottom:
                break
        if reached_bottom:
            game_board.add_block_to_grid(current_block)
            lines_cleared = game_board.clear_lines()
            print(f"Lines cleared: {lines_cleared}")
            current_block = Block()

        # 背景色を設定
        screen.fill(BLACK)
        game_board.draw(screen)
        current_block.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()