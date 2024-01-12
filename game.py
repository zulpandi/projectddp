import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Variabel Global
WIDTH, HEIGHT = 500, 300
PLAYER_SIZE = 50
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 30, 50
PLAYER_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 255)
SCORE_FONT = pygame.font.Font(None, 36)
FPS = 40

# Membuat layar permainan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Lompat-lompatan")

# Membuat pemain
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT)  # Mengatur posisi pemain ke bagian bawah layar

# Membuat rintangan
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()

# Grup pemain dan rintangan
all_sprites = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Membuat clock untuk mengatur FPS
clock = pygame.time.Clock()

# Variabel permainan
jumping = False
jump_count = 10
obstacle_frequency = 100  # Frekuensi rintangan yang lebih rendah
obstacle_speed = 5
score = 0
min_obstacle_distance = 200  # Jarak minimum antara rintangan
speed_increase_interval = 10  # Setiap 10 skor, kecepatan akan meningkat

# Fungsi untuk membuat rintangan baru
def create_obstacle():
    obstacle = Obstacle()
    obstacle.rect.x = WIDTH
    obstacle.rect.y = HEIGHT - OBSTACLE_HEIGHT
    obstacle_group.add(obstacle)
    all_sprites.add(obstacle)

# Loop permainan
playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True

    # Gerakan pemain
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.rect.left > 0:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
        player.rect.x += 5

    # Melompat
    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player.rect.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    # Membuat rintangan dengan frekuensi tertentu
    if random.randrange(0, obstacle_frequency) == 0:
        if not obstacle_group or WIDTH - obstacle_group.sprites()[-1].rect.x > min_obstacle_distance:
            create_obstacle()

    # Gerakan rintangan dengan kecepatan tertentu
    for obstacle in obstacle_group:
        obstacle.rect.x -= obstacle_speed
        if pygame.sprite.spritecollide(player, obstacle_group, False):
            playing = False
        elif obstacle.rect.right < player.rect.left and not hasattr(obstacle, 'collided'):
            obstacle.collided = True
            score += 1

    # Hapus rintangan yang sudah melewati layar
    obstacle_group = pygame.sprite.Group([obstacle for obstacle in obstacle_group if obstacle.rect.right > 0])

    # Pastikan pemain tidak tenggelam ke luar layar
    player.rect.y = min(player.rect.y, HEIGHT - PLAYER_SIZE)

    # Menggambar pemain dan rintangan
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Menampilkan skor
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update layar
    pygame.display.flip()

    # Mengatur FPS
    clock.tick(FPS)

    # Cek apakah permainan berakhir
    if not playing:
        play_again = input("Apakah Anda ingin bermain lagi? (y/n): ")
        if play_again.lower() == 'y':
            # Reset kondisi permainan
            all_sprites.empty()
            obstacle_group.empty()
            player = Player()
            all_sprites.add(player)
            jumping = False
            jump_count = 10
            obstacle_speed = 5
            score = 0
            playing = True
        else:
            pygame.quit()
            sys.exit()
