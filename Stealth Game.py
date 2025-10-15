import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
DARK_BLUE = (0, 0, 100)
DARK_GREEN = (0, 100, 0)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active = True
        self.cooldown = 0
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos) and self.active

        color = self.hover_color if is_hover else self.color
        if not self.active:
            color = GRAY

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        if self.cooldown > 0:
            cooldown_text = font.render(f"{self.cooldown}s", True, YELLOW)
            screen.blit(cooldown_text, (self.rect.right + 5, self.rect.top + 5))

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos) and self.active

        def update(self):
            if self.cooldown > 0:
                self.cooldown -= 1/FPS
                self.active = False
            else:
                self.active = True
                self.cooldown = 0

class Guard:
    def __init__(self, patrol_id, patrol_time):
        self.id = patrol_id
        self.patrol_time = patrol_time
        self.current_time = 0
        self.position = 0
        self.alert = False
    
    def update(self, dt):
        self.current_time += dt
        self.position = (self.current_time % self.patrol_time) / self.patrol_time
    
    def draw(self, screen, x, y, width, height):
        route_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, DARK_GRAY, route_rect)
        pygame.draw.rect(screen, WHITE, route_rect, 1)

        guard_x = x + int(self.position * width)
        guard_color = RED if self.alert else BLUE
        pygame.draw.circle(screen, guard_color, (guard_x, y + height // 2), 8)

        font = pygame.font.Font(None, 20)
        label = font.render(f"Guard {self.id}", True, WHITE)
        screen.blit(label, (x, y - 20))
    
class StealthGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Terminal Infiltration")
        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

        self.state = "menu"
        self.mission_time = 60
        self.time_remaining = self.mission_time
        self.detection_level = 0
        self.max_detection = 100
        self.objective_progress = 0
        self.objectives_needed = 5

        self.guards = [
            Guard(1, 8),
            Guard(2, 12),
            Guard(3, 10)
        ]

        self.create_buttons()

        self.camera_disabled = False
        self.camera_disable_time = 0
        self.lights_disabled = False
        self.lights_disable_time = 0

        self.event_timer = 0
        self.event_interval = 5
        self.current_event = None

    def create_buttons(self):
        button_y = 450
        button_width = 140
        button_height = 50
        spacing = 160
        start_x = 100

        self.buttons = {
            'camera': Button(start_x, button_y, button_width, button_height, "Disable Cams", DARK_BLUE, BLUE),
            'lights': Button(start_x + spacing, button_y, button_width, button_height, "Cut Lights", DARK_BLUE, BLUE),
            'distract': Button(start_x + 2 * spacing, button_y, button_width, button_height, "Distraction", DARK_BLUE, BLUE),
            'hack': Button(start_x + 3 * spacing, button_y, button_width, button_height, "Hack System", DARK_GREEN, GREEN),
            'menu': Button(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50, "START MISSION", DARK_GREEN, GREEN)
        }

    def reset_game(self):
        self.time_remaining = self.mission_time
        self.detection_level = 0
        self.objective_progress = 0
        self.camera_disabled = False
        self.camera_disable_time = 0
        self.lights_disabled = False
        self.lights_disable_time = 0
        self.event_timer = 0
        self.current_event = None
        for guard in self.guards:
            guard.alert = False
            guard.current_time = random.uniform(0, guard.patrol_time)
        self.create_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.state == "menu":
                    if self.buttons['menu'].is_clicked(pos):
                        self.state = "playing"
                        self.reset_game()
                    
                elif self.state == "playing":
                    self.handle_game_clicks(pos)
                
                elif self.state in ["success", "failure"]:
                    if self.buttons['menu'].is_clicked(pos):
                        self.state = "menu"
        
    def handle_game_clicks(self, pos):
        if self.buttons['camera'].is_clicked(pos):
            self.camera_disabled = True
            self.camera_disable_time = 8
            self.buttons['camera'].cooldown = 15
            self.detection_level = max(0, self.detection_level - 15)

        elif self.buttons['lights'].is_clicked(pos):
            self.lights_disabled = True
            self.lights_disable_time = 6
            self.buttons['lights'].cooldown = 12
            self.detection_level = max(0, self.detection_level - 10)
        
        elif self.buttons['distract'].is_clicked(pos):
            for guard in self.guards:
                guard.alert = False
            self.detection_level = max(0, self.detection_level - 20)
            self.buttons['distract'].cooldown = 20
        
        elif self.buttons['hack'].is_clicked(pos):
            if self.detection_level < 30:
                self.objective_progress += 1
                self.buttons['hack'].cooldown = 3
            else:
                self.detection_level += 15
                self.buttons['hack'].cooldown = 5
    
    def update(self):
        if self.state == "playing":
            return
        
        dt = 1/FPS
        self.time_remaining -= dt

        for button in self.buttons.values():
            button.update()
        
        if self.camera_diable_time > 0:
            self.camera_disable_time -= dt
        else:
            self.camera_disabled = False
        
        if self.lights_disable_time > 0:
            self.lights_disable_time -= dt
        else:
            self.lights_disabled = False
        
        for guard in self.guards:
            guard.update(dt)
        
        base_detection = 2 * dict
        if self.camera_disabled:
            base_detection *= 0.3
        if self.lights_disabled:
            base_detection *= 0.5
        
        self.detection_level += base_detection

        for guard in self.guards:
            if 0.4 < guard.position < 0.6:
                detection_chance - 0.02
                if not self.lights_disabled:
                    detection_chance *= 2
                if not self.camera_disabled:
                    detection_chance *= 1.5
                
                if random.random() < detection_chance:
                    guard.alert = True
                    self.detection_level += 5
        
        self.event_timer += dt
        if self.event_timer >= self.event_interval:
            self.event_timer = 0
            self.trigger_random_event()
        
        if self.objective_progress >= self.objectives_needed:
            self.state = "success"
        elif self.detection_level >= self.max_detection or self.time_remaining <= 0:
            self.state = "failure"
        elif self.detection_level < 0:
            self.state = "failure"
        
    def trigger_random_event(self):
        events = [
            "Security sweep initiated",
            "Guard shift change",
            "System scan detected",
            "Patrol route adjusted"
        ]
        self.current_event = random.choice(events)
        self.detection_level += random.randint(5, 15)
    
    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "success":
            self.draw_end_screen("MISSION SUCCESS", GREEN)
        elif self.state == "failure":
            self.draw_end_screen("MISSION FAILED", RED)
        
        pygame.display.flip()
    
    def draw_menu(self):
        title = self.title_font.render("Terminal Infiltration", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(title, title_rect)

        instructions = [
            "Your agent is infiltrating a secure facility.",
            "Use the terminal to help them avoid detection.",
            "Complete 5 hacks before time runs out.",
            "Don't let the detection reach 100%!"
        ]

        y = 250
        for line in instructions:
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, y))
            self.screen.blit(text, text_rect)
            y += 40

        self.buttons['menu'].draw(self.screen)

    def draw_game(self):
        title = self.title_font.render("SECURITY TERMINAL", True, GREEN)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        self.draw_status_bars(100, 90, 300, 30, "TIME", self.time_remaining, self.mission_time, BLUE)
        self.draw_status_bars(WIDTH - 400, 90, 300, 30, "DETECTION", self.detection_level, self.max_detection, RED)

        obj_text = self.font.render(f"Objectives: {self.objective_progress}/{self.objectives_needed}", True, GREEN)
        self.screen.blit(obj_text, (WIDTH//2 - obj_text.get_width()//2, 90))

        monitor-Y = 150
        for i, guard in enumerate(self.guards):
            guard.draw(self.screen, 100, monitor_y + i * 60, 800, 40)

        status_y = 350
        systems = [
            ("CAMERAS", "OFFLINE" if self.camera_disabled else "ONLINE", GREEN if self.camera_disabled else RED)
            ("LIGHTS", "OFFLINE" if self.lights_disabled else "ONLINE", GREEN if self.lights_disabled else RED)
        ]

        for i, (name, statis, color) in enumerate(systems):
            text = self.small_font.render(f"{name}: {status}", True, color)
            self.screen.blit(text, (100 + i * 250, status_y))

        if self.current_event:
            event_text = self.small_font.render(f"! {self.current_event}", True, YELLOW)
            self.screen.blit(event_text, (WIDTH//2 - event_text.get_width()//2, 390))
        
        for key in ['camera', 'lights', 'distract', 'hack']:
            self.buttons[key].draw(self.screen, self.small_font)
        
    def draw_status_bars(self, x, y, width, height, label, value, max_value, color):
        label_text = self.small_font.render(label, True, WHITE)
        self.screen.blit(label_text, (x, y - 25))

        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, height))

        fill_width = int((value / max_value) * width)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, height))

        pyagame.draw.rect(self.screen, WHITE, (x, y, width, height), 2)

        value_text = self.small_font.render(f"{int(value)}/{max_value}", True, WHITE)
        self.screen.blit(value_text, (x + width//2 - value_text.get_width()//2, y + height//2 - value_text.get_height()//2))

    def draw_end_screen(self, message, color):
        text = self.title_font.render(message, True, color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(text, text_rect)

        stats = [
            f"Objectives Completed: {self.objective_progress}/{self.objectives_needed}",
            f"Final Detection: {int(self.detection_level)}%",
            f"Time Remaining: {int(self.time_remaining)}s"
        ]

        y = HEIGHT//2
        for stat in stats:
            stat_text = self.font.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(WIDTH//2, y))
            self.screen.blit(stat_text, stat_rect)
            y += 40
        
        self.buttons['menu'].text = "RETURN TO MENU"
        self.buttons['menu'].draw(self.screen, self.font)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = StealthGame()
    game.run()