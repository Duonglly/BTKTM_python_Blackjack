
import pygame
import random
import sys
import time

pygame.init()

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

try:
    background = pygame.image.load("cards/casino_background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    card_back = pygame.image.load("cards/card_back.png")
    card_back = pygame.transform.scale(card_back, (80, 120))
    pygame.mixer.music.load("sounds/casino_music.mp3")
    pygame.mixer.music.play(-1)

    # Load sound effects
    card_sound = pygame.mixer.Sound("sounds/rut_bai.mp3")
    win_sound = pygame.mixer.Sound("sounds/win.wav")
    lose_sound = pygame.mixer.Sound("sounds/lose.wav")
   

except pygame.error as e:
    print(f"Error loading media: {e}")
    sys.exit()

card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

for suit in suits:
    for value in values:
        card_name = f"{value}_of_{suit}"
        card_images[card_name] = pygame.image.load(f"cards/{card_name}.png")
        card_images[card_name] = pygame.transform.scale(card_images[card_name], (80, 120))

large_font = pygame.font.Font(None, 74)
medium_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

player_cards = []
dealer_cards = []
game_over = False
player_score = 0
dealer_score = 0
player_busted = False
dealer_busted = False
winner = None

def deal_card():
    suit = random.choice(suits)
    value = random.choice(values)
    return f"{value}_of_{suit}"

def calculate_score(cards):
    score = 0
    ace_count = 0
    for card in cards:
        value = card.split("_")[0]
        if value in ['jack', 'queen', 'king']:
            score += 10
        elif value == 'ace':
            score += 11
            ace_count += 1
        else:
            score += int(value)
    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1
    return score

def draw_cards(cards, x, y, hide_first=False):
    for i, card in enumerate(cards):
        if hide_first and i == 0:
            screen.blit(card_back, (x + i * 100, y))
        else:
            screen.blit(card_images[card], (x + i * 100, y))

def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_instructions():
    screen.fill(GREEN)
    display_text("Welcome to Blackjack!", large_font, WHITE, 100, 100)
    display_text("Instructions:", medium_font, WHITE, 100, 200)
    display_text("1. Try to get as close to 21 as possible.", small_font, WHITE, 100, 250)
    display_text("2. Dealer must stand on 17 or higher.", small_font, WHITE, 100, 300)
    display_text("3. Ace can be 1 or 11.", small_font, WHITE, 100, 350)
    display_text("4. Press 'H' to Hit and 'S' to Stand.", small_font, WHITE, 100, 400)
    display_text("Click 'PLAY NOW' to start!", medium_font, WHITE, 100, 450)
    pygame.draw.rect(screen, BLACK, (300, 500, 200, 50))
    display_text("PLAY NOW", small_font, WHITE, 330, 510)
    pygame.display.update()

def game_over_screen(winner):
    screen.fill(BLACK)
    display_text(f"Your Score: {player_score}", medium_font, WHITE, 50, 50)
    draw_cards(player_cards, 50, 100)
    display_text(f"Dealer's Score: {dealer_score}", medium_font, WHITE, 600, 50)
    draw_cards(dealer_cards, 600, 100)
    if winner == "Tie":
        display_text("It's a Tie!", large_font, WHITE, 350, 250)
    else:
        display_text(f"{winner} Wins!", large_font, WHITE, 350, 250)
    pygame.draw.rect(screen, GREEN, (375, 500, 200, 50))
    display_text("PLAY AGAIN", small_font, WHITE, 402.5, 510)
    pygame.display.update()

def reset_game():
    global player_cards, dealer_cards, game_over, player_score, dealer_score, player_busted, dealer_busted, winner
    player_cards = []
    dealer_cards = []
    game_over = False
    player_score = 0
    dealer_score = 0
    player_busted = False
    dealer_busted = False
    winner = None

def main():
    global player_cards, dealer_cards, game_over, player_score, dealer_score, player_busted, dealer_busted, winner
    clock = pygame.time.Clock()
    running = True
    on_instructions = True
    while running:
        if on_instructions:
            game_instructions()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 300 <= x <= 500 and 500 <= y <= 550:
                        on_instructions = False
                        reset_game()
        else:
            screen.blit(background, (0, 0))
            if not player_cards and not dealer_cards:
                for _ in range(2):
                    player_cards.append(deal_card())
                    dealer_cards.append(deal_card())
                player_score = calculate_score(player_cards)
                dealer_score = calculate_score(dealer_cards)
            draw_cards(player_cards, 400, 400)
            draw_cards(dealer_cards, 400, 100, hide_first=True)
            display_text(f"Your Score: {player_score}", medium_font, WHITE, 375, 350)
            display_text(f"Dealer's Cards", medium_font, WHITE, 375, 50)
            if game_over:
                if winner:
                    game_over_screen(winner)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and not game_over:
                        player_cards.append(deal_card())
                        card_sound.play()
                        player_score = calculate_score(player_cards)
                        if player_score > 21:
                            player_busted = True
                            winner = "Dealer"
                            lose_sound.play()
                            game_over = True
                    if event.key == pygame.K_s and not game_over:
                        while dealer_score < 17:
                            dealer_cards.append(deal_card())
                            card_sound.play()
                            dealer_score = calculate_score(dealer_cards)
                        if dealer_score > 21:
                            dealer_busted = True
                            winner = "Player"
                            win_sound.play()
                        elif player_score == dealer_score:
                            winner = "Tie"
                        elif not winner:
                            winner = "Player" if player_score > dealer_score else "Dealer"
                            if winner == "Player":
                                win_sound.play()
                            else:
                                lose_sound.play()
                        game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                    x, y = event.pos
                    if 300 <= x <= 500 and 510 <= y <= 560:
                        reset_game()
            if player_busted:
                winner = "Dealer"
                game_over = True
            elif dealer_busted:
                winner = "Player"
                game_over = True
            clock.tick(30)

if __name__ == "__main__":
    main()
