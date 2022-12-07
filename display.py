import sys
import pygame
from simulator import Simulator

class Display:
    def __init__(self, simulator: Simulator, width=800, height=600):
        pygame.init()
        self.simulator = simulator
        self.width = width
        self.height = height        
        self.fonts: dict = {}
        self.playpause = pygame.transform.smoothscale(
            pygame.image.load("playpause.png"), (160, 80)
        )
        self.step = pygame.transform.smoothscale(
            pygame.image.load("step.png"), (80, 80)
        )
        self.paused = True
        self.timer_event = pygame.USEREVENT + 1

    def country_size(self, country_count):
        return (self.width, ((self.height - 100) / country_count))

    def draw_text(self, screen, where, text, size=50, color="white", align="center"):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont("futura,futurattc,futurattf", size)
        font = self.fonts[size]
        surface = font.render(text, True, pygame.Color(color))
        surface_rect = surface.get_rect()
        setattr(surface_rect, align, where)
        return screen.blit(surface, surface_rect)

    def linear_interpolation(self, color1, color2, amount):
        """
        Interpolation for color spaces is hard to do well, because
        the human eye and brain complicate things. See: 
        https://en.wikipedia.org/wiki/HSL_and_HSV

        Here, we'll just do a naive interpolation that doesn't try 
        to account for any of that. It's good enough for this display!
        """        
        if(amount > 1.0):
            raise ValueError(f'linear_interpolation given amount > 1.0: {amount}')
        r = color1.r + (color2.r - color1.r) * amount
        g = color1.g + (color2.g - color1.g) * amount
        b = color1.b + (color2.b - color1.b) * amount
        return pygame.Color(int(r), int(g), int(b))

    def color_from_temperature(self, curr_temp, baseline_temp):
        green = pygame.Color("darkgreen")
        yellow = pygame.Color("yellow")
        red = pygame.Color("darkred")

        pct_change = (curr_temp - baseline_temp) / baseline_temp
        if pct_change > 0.35:
            return self.linear_interpolation(
                yellow,
                red,
                min(1.0, pct_change),
            )
        else:
            return self.linear_interpolation(
                green, yellow, pct_change
            )

    def draw_country(self, screen, country_count, index, country):
        (width, height) = self.country_size(country_count)
        location = (0, (index * height))
        pygame.draw.rect(
            screen,
            self.color_from_temperature(country["temperature"], self.simulator.initial_country_temps[country["name"]]),
            pygame.Rect(location, (width, height)),
        )
        pygame.draw.rect(
            screen, pygame.Color("black"), pygame.Rect(location, (width, height)), 2
        )

        self.draw_text(
            screen,
            (location[0] + width / 2, location[1]),
            country["name"],
            align="midtop",
        )
        self.draw_text(
            screen,
            (location[0] + width / 2, location[1] + 50),
            "{0:.1f}º".format(country["temperature"]),
            size=30,
            align="midtop",
        )

    def draw_countries(self, screen):
        countries = self.simulator.report()
        for (index, country) in enumerate(countries):
            self.draw_country(screen, len(countries), index, country)

    def draw_ui(self, screen):
        cropped_playpause = pygame.Surface((80, 80))
        if self.paused:
            cropped_playpause.blit(self.playpause, (0, 0), (0, 0, 80, 80))
        else:
            cropped_playpause.blit(self.playpause, (0, 0), (80, 0, 160, 80))
        playpause_rect = cropped_playpause.get_rect()
        playpause_rect.bottomleft = (10, self.height - 10)
        self.playpause_rect = screen.blit(cropped_playpause, playpause_rect)
        step_rect = self.step.get_rect()
        step_rect.bottomleft = (120, self.height - 10)
        self.step_rect = screen.blit(self.step, step_rect)
        self.draw_text(
            screen,
            (self.width - 10, self.height),
            "Year: " +  str(self.simulator.time),
            color="black",
            align="bottomright",
            size=40 
        )
        self.draw_text(
            screen,
            (self.width - 10, self.height - 50),
            ("Global surface temp inc: " + str('%.3f'%self.simulator.global_surface_temp_inc)),
            color="black",
            align="bottomright",
            size=40,
        ) 

    def draw(self, screen):
        screen.fill(pygame.Color("white"))
        self.draw_countries(screen)
        self.draw_ui(screen)
        pygame.display.flip()

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.time.set_timer(self.timer_event, 100)
        while True:
            self.draw(screen)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.playpause_rect.collidepoint(pos):
                    self.paused = not self.paused
                if self.step_rect.collidepoint(pos):
                    self.simulator.advance_year()
            elif event.type == self.timer_event:
                if not self.paused:
                    self.simulator.advance_year()
