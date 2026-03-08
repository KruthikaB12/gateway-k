import pygame
import random

pygame.init()
ARENA_W, ARENA_H = 600, 400
SCOREBOARD_W = 200
W, H = ARENA_W + SCOREBOARD_W, ARENA_H
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

SIZE = 20
high_score = 0
last_score = 0
last_time = 0

def reset_game():
    return [(ARENA_W//2, ARENA_H//2)], (SIZE, 0), (random.randrange(0, ARENA_W, SIZE), random.randrange(0, ARENA_H, SIZE)), 0, False, pygame.time.get_ticks()

snake, direction, food, score, game_over, start_time = reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                snake, direction, food, score, game_over, start_time = reset_game()
            elif not game_over:
                if event.key == pygame.K_UP and direction != (0, SIZE):
                    direction = (0, -SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -SIZE):
                    direction = (0, SIZE)
                elif event.key == pygame.K_LEFT and direction != (SIZE, 0):
                    direction = (-SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-SIZE, 0):
                    direction = (SIZE, 0)
    
    if not game_over:
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        if head[0] < 0 or head[0] >= ARENA_W or head[1] < 0 or head[1] >= ARENA_H or head in snake:
            game_over = True
            last_score = score
            last_time = (pygame.time.get_ticks() - start_time) // 1000
            if score > high_score:
                high_score = score
        else:
            snake.insert(0, head)
            
            if head == food:
                score += 1
                food = (random.randrange(0, ARENA_W, SIZE), random.randrange(0, ARENA_H, SIZE))
            else:
                snake.pop()
    
    screen.fill((0, 0, 0))
    
    for i, segment in enumerate(snake):
        if i == 0:
            pygame.draw.rect(screen, (0, 200, 0), (*segment, SIZE, SIZE))
            pygame.draw.circle(screen, (255, 255, 255), (segment[0] + SIZE//4, segment[1] + SIZE//4), 3)
            pygame.draw.circle(screen, (255, 255, 255), (segment[0] + 3*SIZE//4, segment[1] + SIZE//4), 3)
        else:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, SIZE, SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (*food, SIZE, SIZE))
    
    pygame.draw.line(screen, (255, 255, 255), (ARENA_W, 0), (ARENA_W, ARENA_H), 2)
    
    pygame.draw.rect(screen, (30, 30, 30), (ARENA_W, 0, SCOREBOARD_W, ARENA_H))
    
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    
    font = pygame.font.Font(None, 28)
    y_pos = 20
    
    title = font.render('SCOREBOARD', True, (255, 255, 0))
    screen.blit(title, (ARENA_W + 20, y_pos))
    y_pos += 50
    
    current_score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(current_score_text, (ARENA_W + 20, y_pos))
    y_pos += 35
    
    current_time_text = font.render(f'Time: {elapsed_time}s', True, (255, 255, 255))
    screen.blit(current_time_text, (ARENA_W + 20, y_pos))
    y_pos += 60
    
    pygame.draw.line(screen, (100, 100, 100), (ARENA_W + 10, y_pos - 20), (W - 10, y_pos - 20), 1)
    
    high_score_text = font.render(f'High: {high_score}', True, (0, 255, 0))
    screen.blit(high_score_text, (ARENA_W + 20, y_pos))
    y_pos += 50
    
    if last_score > 0:
        last_score_text = font.render(f'Last: {last_score}', True, (200, 200, 200))
        screen.blit(last_score_text, (ARENA_W + 20, y_pos))
        y_pos += 35
        
        last_time_text = font.render(f'Time: {last_time}s', True, (200, 200, 200))
        screen.blit(last_time_text, (ARENA_W + 20, y_pos))
    
    if game_over:
        font = pygame.font.Font(None, 36)
        game_over_text = font.render('Game Over! Press SPACE', True, (255, 255, 0))
        screen.blit(game_over_text, (ARENA_W//2 - 180, ARENA_H//2))
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
