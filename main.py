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

# ゲームループ
def main():
    clock = pygame.time.Clock()
    running = True
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

        # 背景色を設定
        screen.fill(BLACK)
        current_block.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()