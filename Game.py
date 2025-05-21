import sys
import random
import pygame

def main():
    pygame.init()

    #-----------------------play music------------------------
    # background
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("background.mp3")  # Load your music file
    pygame.mixer.music.play(-1)  # Play infinitely (-1 means loop forever)

    # for drop the circle
    drop_sound = pygame.mixer.Sound("drop.mp3")  
    drop_sound.set_volume(0.7)  # Optional: Set volume (0.0 to 1.0)

    # for gun 
    dash_p1_sound = pygame.mixer.Sound("shoot_for_p1.mp3")  # Sound when player shoot
    dash_p1_sound.set_volume(0.5)

    # for gun 
    dash_p2_sound = pygame.mixer.Sound("shoot1.mp3")  # Sound when player shoot
    dash_p2_sound.set_volume(0.5)
    
    # for pickup
    pickup_sound = pygame.mixer.Sound("collect_circle.mp3")  # Sound when player collects
    pickup_sound.set_volume(10)
    
    # for hurt
    hurt_sound = pygame.mixer.Sound("hurt.mp3")  # Sound when player Hits
    hurt_sound.set_volume(10)
    
    # for win
    win_sound = pygame.mixer.Sound("win.mp3")  # Sound when player Win
    win_sound.set_volume(10)
     
    #for loss
    loss_sound = pygame.mixer.Sound("loss.mp3")  # Sound when player Loss
    loss_sound.set_volume(10)
    
    # for Mission start
    mission_sound = pygame.mixer.Sound("mission_open.mp3")  # Sound when player Loss
    mission_sound.set_volume(10)

    # for Game play
    game_play_sound = pygame.mixer.Sound("start_play.mp3")  # Sound when player Loss
    game_play_sound.set_volume(10)
    
    
    # --------------------- Window Setup ---------------------
    window_width, window_height = 1200, 700
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Squares within the Big Square")

    # --------------------- Big Square (Play Area) ---------------------
    big_border_color = (255, 0, 0)
    big_square_height = 500
    big_square_width = 1000
    big_x_pos, big_y_pos = 100, 100
    big_border_width = 5

    # --------------------- Player 1 (Manual Player) Setup ---------------------
    # Vertical border
    p1_a_border_color = (0, 0, 225)
    p1_a_square_height = 500
    p1_a_square_width = 10
    p1_a_x_pos, p1_a_y_pos = 200, 100
    p1_a_border_width = 2

    # Horizontal border
    p1_b_border_color = (0, 0, 225)
    p1_b_square_height = 10
    p1_b_square_width = 1000
    p1_b_x_pos, p1_b_y_pos = 100, 500
    p1_b_border_width = 2

    # Dash Effect for Player 1
    p1_dash_active = False
    p1_dash_x = p1_a_x_pos + p1_a_square_width //2 # Start from current player position
    p1_dash_y = p1_b_y_pos + p1_b_square_height // 2
    p1_dash_speed = 10  # Dash speed in pixels

    # speed
    p1_speed = 1.7

    # --------------------- Player 2 (Bot) Setup ---------------------
    # Vertical border
    p2_a_border_color = (0, 225, 0)
    p2_a_square_height = 500
    p2_a_square_width = 10
    p2_a_x_pos, p2_a_y_pos = 300, 100
    p2_a_border_width = 2

    # Horizontal border
    p2_b_border_color = (0, 225, 0)
    p2_b_square_height = 10
    p2_b_square_width = 1000
    p2_b_x_pos, p2_b_y_pos = 100, 200
    p2_b_border_width = 2

    # dash 
    p2_attack_active = False
    p2_attack_x = 0
    p2_attack_y = 0
    p2_attack_speed = 10

    # speed
    p2_speed = 1.5
    
    #----------------------Game winning condition----------------------
    win_score = 2
    winner = None  # Will store "Player 1" or "Bot"
    font = pygame.font.Font(None, 36)

    # --------------------- Corner Squares (Drop zones) ---------------------
    corner_square_size = 90
    corner_square_border_width = 5

    # Player 2 (Bot) drop zone: Top-right
    corner_square_top_right_x = big_x_pos + big_square_width - corner_square_size
    corner_square_top_right_y = big_y_pos

    # Player 1 (Manual) drop zone: Bottom-left
    corner_square_bottom_left_x = big_x_pos
    corner_square_bottom_left_y = big_y_pos + big_square_height - corner_square_size

    # --------------------- Circle Properties ---------------------
    circle_radius = 20
    circle_border_width = 2
    default_circle_color = (255, 165, 0)

    # --------------------- Font Setup ---------------------
    font = pygame.font.SysFont("Arial", 30)

    # --------------------- Circle Generator ---------------------
    def generate_random_circles(num_circles=5):
        circles = []
        for _ in range(num_circles):
            x = random.randint(big_x_pos + circle_radius, big_x_pos + big_square_width - circle_radius)
            y = random.randint(big_y_pos + circle_radius, big_y_pos + big_square_height - circle_radius)
            timestamp = pygame.time.get_ticks()  # Time when circle was created
            color = default_circle_color
            circles.append({"pos": (x, y), "timestamp": timestamp, "color": color})
        return circles

    circles = generate_random_circles()

    # --------------------- Game State ---------------------
    p1_score = 0
    p2_score = 0
    p1_z_pressed = False
    p2_x_pressed = False
    collected_p1_circle = False
    collected_p2_circle = False
    p2_last_collected_color = default_circle_color

    # --------------------- Game Loop ---------------------
    running = True
    clock = pygame.time.Clock()
    
    def get_game_settings():
        font = pygame.font.Font(None, 48)
        clock = pygame.time.Clock()

        def get_input(prompt_text):
            input_text = ""
            input_box = pygame.Rect(300, 250, 200, 50)
            while True:
                screen.fill((255, 255, 255))
                prompt = font.render(prompt_text, True, (100, 100, 100))
                screen.blit(prompt, (280, 180))

                txt_surface = font.render(input_text, True, (0, 0, 255))
                pygame.draw.rect(screen, (200, 200, 200), input_box)
                screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            dash_p1_sound.play()
                            # Only accept positive digits (float speeds allowed)
                            if input_text.replace('.', '', 1).isdigit() and float(input_text) > 0:
                                return float(input_text) if '.' in input_text else int(input_text)
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in input_text):
                            input_text += event.unicode
                clock.tick(30)

        
        
        # Get win score as int
        win_score = int(get_input("Enter score to win:"))
        # Get user speed as float
        p1_speed = float(get_input("Enter Your speed: Default 1.7"))
        
        # cheack valid speed for p1
        while True:
            if 0 < p1_speed and p1_speed < 21:
                break
            else:
                loss_sound.play()
                # get_input("Not be less than 0 or greater than 20")
                p1_speed = float(get_input("Enter Your speed: Default 1.7"))

        # Get bot speed as float
        p2_speed = float(get_input("Enter bot speed: Default 1.5"))

        # cheack valid speed for p2 or bot
        while True:
            if 0 < p2_speed and p2_speed < 21:
                break
            else:
                loss_sound.play()                
                # get_input("Not be less than 0 or greate than 20")
                p2_speed = float(get_input("Enter Bot speed: Default 1.5"))
        game_play_sound.play()
        return win_score, p1_speed , p2_speed

    def mission():
        font = pygame.font.Font(None, 64)
        small_font = pygame.font.Font(None, 40)
        clock = pygame.time.Clock()
        button_rect = pygame.Rect(250, 450, 300, 60)

        # List of mission lines to display
        missions = [
            "1. Speed : You = 1.5, Bot = 1.5, Win Score = 10",
            "2. Speed : You = 1, Bot = 10, Win Score = 2",
            "3. Shoot Bot 10 Time ",
            "4. Win with 0 score of Bot with Speed : You = 2, Bot = 3, Win Score = 10",
            "5. Avoid bot attacks with Speed : You = 10, Bot = 9 Win Score = 10"
        ]
        mission_sound.play()
        
        while True:
            screen.fill((255, 255, 255))

            # Mission Title
            m = font.render("Missions:", True, (250, 0, 0))
            screen.blit(m, (220, 100))

            # Display each mission line, spaced by 50 pixels vertically
            for i, line in enumerate(missions):
                mission_text = small_font.render(line, True, (100, 100, 0))
                screen.blit(mission_text, (100, 180 + i * 50))

            # Restart button
            pygame.draw.rect(screen, (0, 120, 255), button_rect)
            button_text = small_font.render("Start Game", True, (255, 255, 255))
            screen.blit(button_text, (button_rect.x + 70, button_rect.y + 15))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dash_p1_sound.play()
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        dash_p1_sound.play()
                        return  # Exit mission screen to continue

            clock.tick(30)



    # Show mission screen first
    mission()
    
    # Then collect settings from user
    win_score, p1_speed , p2_speed = get_game_settings()

    
    def show_win_screen(winner_text):
        font = pygame.font.Font(None, 64)
        small_font = pygame.font.Font(None, 40)
        clock = pygame.time.Clock()
        button_rect = pygame.Rect(250, 350, 300, 60)

        while True:
            screen.fill((255, 255, 255))
            
            # Win text
            win_text = font.render(winner_text, True, (0, 150, 0))
            screen.blit(win_text, (220, 200))
            
            # Restart button
            pygame.draw.rect(screen, (0, 120, 255), button_rect)
            button_text = small_font.render("Restart Game", True, (255, 255, 255))
            screen.blit(button_text, (button_rect.x + 40, button_rect.y + 15))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        dash_p1_sound.play()
                        return  # Exit this screen to restart the game

            clock.tick(30)


    while running:        
        screen.fill((255, 255, 255))  # Clear screen with white background

            # Check for win condition
        if p1_score >= win_score:
            winner = "Player 1"
            running = False
        elif p2_score >= win_score:
            winner = "Bot"
            running = False

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit on window close
            # Allow user to change win_score with + and - keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    win_score += 1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    if win_score > 1:
                        win_score -= 1

                
                # Key press handling
            if event.type == pygame.KEYDOWN:
                #   dash
                if event.key == pygame.K_c and not p1_dash_active:
                    dash_p1_sound.play()                    
                    p1_dash_active = True
                    p1_dash_x = p1_a_x_pos  # Start dash from left

                # Player 1 collects circle with 'Z'
                if event.key == pygame.K_z and not p1_z_pressed:
                    p1_z_pressed = True
                    for circle in circles[:]:  # Check for collision with any circle
                        if (p1_a_x_pos < circle["pos"][0] + circle_radius and
                            p1_a_x_pos + p1_a_square_width > circle["pos"][0] - circle_radius and
                            p1_b_y_pos < circle["pos"][1] + circle_radius and
                            p1_b_y_pos + p1_b_square_height > circle["pos"][1] - circle_radius):
                            circles.remove(circle)
                            circles.append(generate_random_circles(1)[0])
                            collected_p1_circle = True
                            # collected_p2_circle = False
                            pickup_sound.play()

                # Player 2 (bot) manual trigger using 'X' (optional/debug)
                if event.key == pygame.K_x and not p2_x_pressed:
                    p2_x_pressed = True
                    for circle in circles[:]:
                        if (p2_a_x_pos < circle["pos"][0] + circle_radius and
                            p2_a_x_pos + p2_a_square_width > circle["pos"][0] - circle_radius and
                            p2_b_y_pos < circle["pos"][1] + circle_radius and
                            p2_b_y_pos + p2_b_square_height > circle["pos"][1] - circle_radius):
                            circles.remove(circle)
                            circles.append(generate_random_circles(1)[0])
                            collected_p2_circle = True
                            # collected_p1_circle = False
                            p2_last_collected_color = circle["color"]
                            pickup_sound.play()

            # Key release handling
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    p1_z_pressed = False
                if event.key == pygame.K_x:
                    p2_x_pressed = False

        # --------------------- Circle Expiration Logic ---------------------
        current_time = pygame.time.get_ticks()
        for circle in circles[:]:
            if current_time - circle["timestamp"] >= 3000:  # 3 seconds lifespan
                circles.remove(circle)
                circles.append(generate_random_circles(1)[0])

        keys = pygame.key.get_pressed()

        # --------------------- Player 1 Movement ---------------------
        if keys[pygame.K_LEFT] and p1_a_x_pos > big_x_pos:
            p1_a_x_pos -= p1_speed
        if keys[pygame.K_RIGHT] and p1_a_x_pos < big_x_pos + big_square_width - p1_a_square_width:
            p1_a_x_pos += p1_speed
        if keys[pygame.K_UP] and p1_b_y_pos > big_y_pos:
            p1_b_y_pos -= p1_speed
            p1_dash_y -= p1_speed
        if keys[pygame.K_DOWN] and p1_b_y_pos < big_y_pos + big_square_height - p1_b_square_height:
            p1_b_y_pos += p1_speed
            p1_dash_y += p1_speed

        # --------------------- Bot (Player 2) Logic ---------------------
        if not collected_p2_circle and circles:
            # Go to nearest circle
            nearest = min(circles, key=lambda c: (c["pos"][0] - (p2_a_x_pos + 5))**2 + (c["pos"][1] - (p2_b_y_pos + 4))**2)
            target_x, target_y = nearest["pos"]

            # Move bot toward the target circle
            if p2_a_x_pos + 5 < target_x and p2_a_x_pos < big_x_pos + big_square_width - p2_a_square_width:
                p2_a_x_pos += p2_speed
            elif p2_a_x_pos + 5 > target_x and p2_a_x_pos > big_x_pos:
                p2_a_x_pos -= p2_speed
            if p2_b_y_pos + 4 < target_y and p2_b_y_pos < big_y_pos + big_square_height - p2_b_square_height:
                p2_b_y_pos += p2_speed
            elif p2_b_y_pos + 4 > target_y and p2_b_y_pos > big_y_pos:
                p2_b_y_pos -= p2_speed

            # Collect if close enough
            if abs(p2_a_x_pos + 5 - target_x) < circle_radius and abs(p2_b_y_pos + 4 - target_y) < circle_radius:
                circles.remove(nearest)
                circles.append(generate_random_circles(1)[0])
                collected_p2_circle = True
                p2_last_collected_color = nearest["color"]

        elif collected_p2_circle:
            # Move to top-right drop zone
            if p2_a_x_pos + p2_a_square_width < corner_square_top_right_x + corner_square_size:
                p2_a_x_pos += 1.1
            elif p2_a_x_pos + p2_a_square_width > corner_square_top_right_x + corner_square_size:
                p2_a_x_pos -= 1.1
            if p2_b_y_pos > corner_square_top_right_y:
                p2_b_y_pos -= 1.1
            elif p2_b_y_pos < corner_square_top_right_y:
                p2_b_y_pos += 1.1

            # Check drop-off and increment score
            if (p2_a_x_pos + p2_a_square_width > corner_square_top_right_x and
                    p2_b_y_pos < corner_square_top_right_y + corner_square_size):
                p2_score += 1
                collected_p2_circle = False
                drop_sound.play()

        # --------------------- Player 1 Drop-off Logic ---------------------
        if collected_p1_circle and (p1_a_x_pos < corner_square_bottom_left_x + corner_square_size and
                                    p1_b_y_pos + p1_b_square_height > corner_square_bottom_left_y):
            p1_score += 1
            collected_p1_circle = False
            drop_sound.play()

        # Check for win
        if p1_score >= win_score:
            win_sound.play()
            show_win_screen("Player 1 Wins!")
            
            main()  # Restart the whole game

        if p2_score >= win_score:
            loss_sound.play()
            show_win_screen("Player 2 Wins!")
            
            main()  # Restart the whole game



        # Dash movement
        if p1_dash_active:
            p1_dash_x += p1_dash_speed
            if p1_dash_x > big_x_pos + big_square_width:
                p1_dash_active = False
    

        # Bot auto-attack when Player 1 is in front (face-to-face horizontally)
        if not p2_attack_active:
            same_row = abs(p1_b_y_pos - p2_b_y_pos) < 30  # Nearly same Y
            p1_to_left = p1_a_x_pos < p2_a_x_pos  # P1 is to the left of P2
            aligned = same_row and p1_to_left and abs(p1_b_y_pos - p2_b_y_pos) < 20

            if aligned:
                dash_p2_sound.play()
                p2_attack_active = True
                p2_attack_x = p2_a_x_pos  # Start at bot's position
                p2_attack_y = p2_b_y_pos + 4  # Center Y of bot

        # Move P2's attack bar left
        if p2_attack_active:
            p2_attack_x -= p2_attack_speed
            if p2_attack_x < big_x_pos:
                p2_attack_active = False  # Reset when off screen

        # Check if bot attack hits Player 1 carrying a circle
        if p2_attack_active and collected_p1_circle:
            p1_center_x = p1_a_x_pos + p1_a_square_width // 2
            p1_center_y = p1_b_y_pos + p1_b_square_height // 2
            if abs(p2_attack_x - p1_center_x) < 10 and abs(p2_attack_y - p1_center_y) < 20:
                # Attack hits Player 1
                hurt_sound.play()
                collected_p1_circle = False  # Drop the circle
                p2_attack_active = False     # End the attack


        # Check if dash hits bot while it carries a circle
        if p1_dash_active and collected_p2_circle:
            bot_center_x = p2_a_x_pos + p2_a_square_width // 2
            bot_center_y = p2_b_y_pos + p2_b_square_height // 2
            dash_center_x = p1_dash_x + 10  # center of dash line
            dash_center_y = p1_dash_y

            distance = ((dash_center_x - bot_center_x) ** 2 + (dash_center_y - bot_center_y) ** 2) ** 0.5
            if distance < circle_radius:  # collision threshold
                hurt_sound.play()
                collected_p2_circle = False  # Remove bot's carried circle

        # --------------------- Drawing Section ---------------------
        # Draw play area and players
        pygame.draw.rect(screen, big_border_color, (big_x_pos, big_y_pos, big_square_width, big_square_height), big_border_width)
        pygame.draw.rect(screen, p1_a_border_color, (p1_a_x_pos, p1_a_y_pos, p1_a_square_width, p1_a_square_height), p1_a_border_width)
        pygame.draw.rect(screen, p1_b_border_color, (p1_b_x_pos, p1_b_y_pos, p1_b_square_width, p1_b_square_height), p1_b_border_width)
        pygame.draw.rect(screen, p2_a_border_color, (p2_a_x_pos, p2_a_y_pos, p2_a_square_width, p2_a_square_height), p2_a_border_width)
        pygame.draw.rect(screen, p2_b_border_color, (p2_b_x_pos, p2_b_y_pos, p2_b_square_width, p2_b_square_height), p2_b_border_width)

        # Draw drop zones
        pygame.draw.rect(screen, (0, 0, 0), (corner_square_top_right_x, corner_square_top_right_y, corner_square_size, corner_square_size), corner_square_border_width)
        pygame.draw.rect(screen, (0, 0, 0), (corner_square_bottom_left_x, corner_square_bottom_left_y, corner_square_size, corner_square_size), corner_square_border_width)

        # Draw active circles in the game
        for circle in circles:
            pygame.draw.circle(screen, circle["color"], circle["pos"], circle_radius)

        # Draw circle held by player 1
        if collected_p1_circle:
            pygame.draw.circle(screen, default_circle_color, (p1_a_x_pos + 5, p1_b_y_pos + 4), circle_radius)
        else:
            pygame.draw.circle(screen, default_circle_color, (p1_a_x_pos + 5, p1_b_y_pos + 4), circle_radius, circle_border_width)

        # Draw circle held by player 2
        if collected_p2_circle:
            pygame.draw.circle(screen, p2_last_collected_color, (p2_a_x_pos + 5, p2_b_y_pos + 4), circle_radius)
        else:
            pygame.draw.circle(screen, p2_last_collected_color, (p2_a_x_pos + 5, p2_b_y_pos + 4), circle_radius, circle_border_width)

        # Draw dash line
        if p1_dash_active:
            pygame.draw.line(screen, (0, 0, 255), (p1_dash_x, p1_dash_y), (p1_dash_x + 20, p1_dash_y), 3)

        # Draw bot's attack bar (right to left)
        if p2_attack_active:
            pygame.draw.line(screen, (0, 200, 0), (p2_attack_x, p2_attack_y), (p2_attack_x - 20, p2_attack_y), 3)

        # Draw scores
        screen.blit(font.render(f"P1 Score: {p1_score}", True, (0, 0, 255)), (50, 20))
        screen.blit(font.render(f"P2 Score: {p2_score}", True, (0, 255, 0)), (window_width - 200, 20))

        # Display win score
        win_text = font.render(f"Win Score: {win_score}", True, (0, 0, 0))
        screen.blit(win_text, (600, 30))


        # Define button properties
        button_font = pygame.font.SysFont("arial", 28)  # Use Arial, size 28
        button_color = (100, 200, 255)                  # Light blue
        button_hover = (70, 170, 230)                   # Slightly darker blue when hovered
        button_text_color = (255, 255, 255)             # White text

        # Position buttons below the game area
        reset_button = pygame.Rect(150, 650, 100, 40)
        exit_button = pygame.Rect(300, 650, 100, 40)

        def draw_button(screen, rect, text):
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, button_hover if rect.collidepoint(mouse_pos) else button_color, rect)
            text_surf = button_font.render(text, True, button_text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # In your main loop (after drawing game elements)
        draw_button(screen, reset_button, "Reset")
        draw_button(screen, exit_button, "Exit")

        # In your event loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if reset_button.collidepoint(event.pos):
                    hurt_sound.play()                
                    # Reset scores here (adjust variable names as needed)
                    p1_score = 0
                    p2_score = 0
                    # print("Scores reset.")

                elif exit_button.collidepoint(event.pos):
                    hurt_sound.play()
    
                    pygame.quit()
                    sys.exit()

                

        # Refresh screen
        pygame.display.flip()
        clock.tick(60)  # Limit FPS to 60

    # --- Display the winner on the screen ---
    screen.fill((255, 255, 255))
    winner_text = font.render(f"{winner} wins!", True, (0, 128, 0))
    screen.blit(winner_text, (1200 // 2 - 100, 700 // 2))
    pygame.display.flip()

    # --- Wait and quit ---
    pygame.time.delay(1)
    pygame.quit()    # Exit game
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        main()