import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Schere Stein Papier")

background_image = pygame.image.load(r'C:\Users\zmandd\PycharmProjects\pythongame\assets\images\hackerman.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
shrift = pygame.font.SysFont('Arial', 40)
small_shrift = pygame.font.SysFont('Arial', 30)

rock_img = pygame.image.load(r'C:\Users\zmandd\PycharmProjects\pythongame\assets\images\rock-default.png')
paper_img = pygame.image.load(r'C:\Users\zmandd\PycharmProjects\pythongame\assets\images\paper.png')
scissors_img = pygame.image.load(r'C:\Users\zmandd\PycharmProjects\pythongame\assets\images\11198_1.jpg')
rock_img = pygame.transform.scale(rock_img, (100, 100))
paper_img = pygame.transform.scale(paper_img, (100, 100))
scissors_img = pygame.transform.scale(scissors_img, (100, 100))

button_width, button_height = 160, 50
button_color = pygame.Color("blue")
player_score = 0
computer_score = 0
winning_score = 3
choices = {'Stein': rock_img, 'Papier': paper_img, 'Schere': scissors_img}

# Musik
pygame.mixer.init()

music_file = r'C:\Users\zmandd\PycharmProjects\pythongame\assets\sounds\tetris-melodiya-klassika.mp3'

pygame.mixer.music.load(music_file)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

def draw_text(text, shrift, color, surface, x, y):
    text_obj = shrift.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def get_computer_choice():
    return random.choice(['Schere', 'Stein', 'Papier'])

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Unentschieden!"
    if (player_choice == 'Schere' and computer_choice == 'Papier') or \
            (player_choice == 'Papier' and computer_choice == 'Stein') or \
            (player_choice == 'Stein' and computer_choice == 'Schere'):
        return "Du hast gewonnen!"
    else:
        return "Computer hat gewonnen!"

def draw_choice(choice, x, y):
    screen.blit(choices[choice], (x, y))

def game_loop():
    global player_score, computer_score
    running = True
    player_choice = 0
    computer_choice = 0
    round_result = 0

    input_locked = False # Anti-spam

    button_x = (SCREEN_WIDTH - (button_width * 3 )) / 2
    button_y = (SCREEN_HEIGHT - button_height) / 2

    while running:
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not input_locked:
                    if event.key == pygame.K_s:
                        player_choice = 'Stein'
                    if event.key == pygame.K_p:
                        player_choice = 'Papier'
                    if event.key == pygame.K_c:
                        player_choice = 'Schere'

                    if player_choice:
                        computer_choice = get_computer_choice()
                        round_result = determine_winner(player_choice, computer_choice)
                        if "Du" in round_result:
                            player_score += 1
                        if "Computer" in round_result:
                            computer_score += 1

                        input_locked = True

                if event.key == pygame.K_q:
                    main_menu()

        pygame.draw.rect(screen, button_color, pygame.Rect(button_x, button_y, button_width, button_height))
        draw_text("Stein (S)", shrift, "white", screen, button_x + button_width / 2, button_y + button_height / 2)
        pygame.draw.rect(screen, button_color, pygame.Rect(button_x + button_width + 20, button_y, button_width, button_height))
        draw_text("Papier (P)", shrift, "white", screen, button_x + button_width + 20 + button_width / 2, button_y + button_height / 2)
        pygame.draw.rect(screen, button_color, pygame.Rect(button_x + 2 * (button_width + 20), button_y, button_width, button_height))
        draw_text("Schere (C)", shrift, "white", screen, button_x + 2 * (button_width + 20) + button_width / 2, button_y + button_height / 2)

        draw_text(f"Spieler: {player_score}", small_shrift, "black", screen, SCREEN_WIDTH / 5, SCREEN_HEIGHT - 30)
        draw_text(f"Computer: {computer_score}", small_shrift, "black", screen, 3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT - 30)

        draw_text('Drücken Sie "Q", um zum Hauptmenü zurückzukehren', small_shrift, "black", screen, SCREEN_WIDTH / 2.6, SCREEN_HEIGHT / 50)

        screen.blit(rock_img, (190, 285))
        screen.blit(paper_img, (370, 275))
        screen.blit(scissors_img, (550, 275))
        if player_choice:
            draw_choice(player_choice, 50,  SCREEN_HEIGHT / 1.6)
        if computer_choice:
            draw_choice(computer_choice, 650, SCREEN_HEIGHT / 1.6)

        if round_result:
            draw_text(round_result, shrift, "blue", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 50)
            draw_text(f"Computer wählte: {computer_choice}", small_shrift, "blue", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

            pygame.display.flip()
            pygame.time.wait(2000)
            input_locked = False
            player_choice, computer_choice, round_result = 0, 0, 0

        if player_score >= winning_score:
            draw_text("Du hast das Spiel gewonnen!", shrift, "blue", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.7)
            pygame.display.flip()
            pygame.time.wait(2000)
            player_score, computer_score = 0, 0

        if computer_score >= winning_score:
            draw_text("Der Computer hat das Spiel gewonnen!", shrift, "blue", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.7)
            pygame.display.flip()
            pygame.time.wait(2000)
            player_score, computer_score = 0, 0

        pygame.display.flip()

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))
        rect_width = 800
        rect_height = 50
        rect_x = (SCREEN_WIDTH - rect_width) / 2
        rect_y = 376

        pygame.draw.rect(screen, "white", pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        draw_text('Drücken Sie eine beliebige Taste, um zu starten', shrift, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_loop()

main_menu()
