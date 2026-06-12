import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
pacman_icon = pygame.image.load("src/inc/img/pacman/stay/S01.png").convert_alpha()
# pacman_icon = pygame.transform.scale(pacman_icon, (24, 24))
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        self.selected = False
    
    def draw(self, surface):
        # Draw button border
        pygame.draw.rect(surface, "yellow", self.rect, 2)
        
        # Draw image on the left if selected
        if self.selected:
            img_rect = pacman_icon.get_rect(center=(self.rect.left - 40, self.rect.centery))
            surface.blit(pacman_icon, img_rect)
        
        # Draw text
        text_surf = font_small.render(self.text, True, "yellow")
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

def start_menu():
    buttons = [
        Button(SCREEN_WIDTH//2 - 75, 200, 150, 50, "START GAME"),
        Button(SCREEN_WIDTH//2 - 75, 300, 220, 50, "VIEW HIGHSCORES"),
        Button(SCREEN_WIDTH//2 - 75, 400, 200, 50, "INSTRUCTIONS"),
        Button(SCREEN_WIDTH//2 - 75, 500, 150, 50, "EXIT"),
    ]

    selected_index = 0
    buttons[selected_index].selected = True
    
    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    buttons[selected_index].selected = False
                    selected_index = (selected_index - 1) % len(buttons)
                    buttons[selected_index].selected = True
                
                elif event.key == pygame.K_DOWN:
                    buttons[selected_index].selected = False
                    selected_index = (selected_index + 1) % len(buttons)
                    buttons[selected_index].selected = True
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_button = buttons[selected_index]
                    if selected_button.text == "START GAME":
                        print("Starting game...")
                        # Call game function here
                    elif selected_button.text == "VIEW HIGHSCORES":
                        print("Opening highscores...")
                    elif selected_button.text == "INSTRUCTIONS":
                        print("Opening instructions...")
                    elif selected_button.text == "EXIT":
                        running = False

                elif event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        buttons[selected_index].selected = False
                        selected_index = i
                        buttons[selected_index].selected = True
                        
                        # Trigger button action
                        if button.text == "START GAME":
                            print("Starting game...")
                        elif button.text == "VIEW HIGHSCORES":
                            print("Opening highscores...")
                        elif button.text == "INSTRUCTIONS":
                            print("Opening instructions...")
                        elif button.text == "EXIT":
                            running = False

        for button in buttons:
            button.update(mouse_pos)
        
        screen.fill("black")
        title = font_large.render("PAC-MAN", True, "yellow")
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    start_menu()
    pygame.quit()
