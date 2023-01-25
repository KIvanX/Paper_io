import math
import time
import pygame


class Player:
    def __init__(self, x, y, color):
        self.color = color
        self.way_color = tuple([min(255, e + 100) for e in color])
        self.terr_color = tuple([min(255, e + 50) for e in color])
        self.in_terr, self.in_terr_new, self.s_ind = True, True, 0
        self.x, self.y, self.ang, self.lng = x, y, 0, 0
        self.terr, self.way = [], []

        for angle in range(0, 361, 3):
            x0 = self.x + math.cos(math.radians(angle)) * 30
            y0 = self.y + math.sin(math.radians(angle)) * 30
            self.terr.append((int(x0 if angle < 180 else 2 * self.x - x0), int(y0)))

        self.new_territory(self.terr, fill=True)

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

        if (int(self.x), int(self.y)) in self.way[:-5]:
            self.dead("Вы убили себя...")

        self.in_terr_new = world.get_at((int(self.x), int(self.y))) == self.terr_color
        if self.in_terr and not self.in_terr_new:
            self.s_ind = self.get_in_territory()
        elif not self.in_terr and self.in_terr_new:
            f_ind = self.get_in_territory()
            if self.s_ind > f_ind:
                self.s_ind, f_ind = f_ind, self.s_ind
                self.way = self.way[::-1]

            terr1 = self.terr[:self.s_ind] + self.way + self.terr[f_ind:]
            terr2 = self.way[::-1] + self.terr[self.s_ind: f_ind]
            self.terr = terr1 if self.new_territory(terr1, fill=True) > self.new_territory(terr2) else terr2
            self.way.clear()
        self.in_terr = self.in_terr_new

    def run(self):
        if num_tick % 3 == 0:
            xm, ym = pygame.mouse.get_pos()
            self.lng = ((xm - w_window // 2) ** 2 + (ym - h_window // 2) ** 2) ** 0.5
            if xm - w_window // 2 != 0 or ym - h_window // 2 != 0:
                self.ang = math.degrees(math.acos((xm - w_window // 2) / self.lng))
            else:
                self.ang = 0
            self.ang = int(self.ang) if h_window // 2 > ym else int(-self.ang + 360)

        if abs(self.lng) > 20:
            for _ in range(3):
                self.x += math.cos(math.radians(self.ang))
                self.y -= math.sin(math.radians(self.ang))

                self.x = 30 if self.x < 30 else w - 33 if self.x > w - 33 else self.x
                self.y = 30 if self.y < 30 else h - 33 if self.y > h - 33 else self.y

                if not self.in_terr and (not self.way or self.way and int(self.y) != self.way[-1][1]):
                    self.way.append((int(self.x), int(self.y)))
                self.check_events()

    def draw(self):
        offset_x, offset_y = w_window // 2 - self.x, h_window // 2 - self.y

        window.fill((200, 200, 200))
        window.blit(world, (offset_x, offset_y))
        for i in range(len(self.way) - 1):
            t1 = self.way[i][0] + offset_x, self.way[i][1] + offset_y
            t2 = self.way[i + 1][0] + offset_x, self.way[i + 1][1] + offset_y
            pygame.draw.line(window, self.way_color, t1, t2, 10)
        pygame.draw.circle(window, self.color, (w_window // 2, h_window // 2), 12)

        pygame.display.flip()

    def get_in_territory(self):
        min_p = min(self.terr, key=lambda t: (t[0] - self.x) ** 2 + (t[1] - self.y) ** 2)
        return self.terr.index(min_p)

    def dead(self, text):
        font = pygame.font.SysFont('Comic Sans MS', 40)
        text = font.render(text, False, (160, 0, 0))
        window.blit(text, (w_window // 2 - 36 * 5, h_window // 2 - 36 * 2))
        pygame.display.flip()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

    def new_territory(self, my_way, fill=False):
        k = 0
        ys = [y1 for x1, y1 in my_way]
        min_y, max_y = min(ys), max(ys)
        for y_line in range(max(1, min_y), max_y + 1, 2):
            xs_line = sorted([x1 for x1, y1 in my_way if y1 == y_line])

            if len(xs_line) % 2 == 0:
                for i in range(len(xs_line) // 2):
                    k += (xs_line[i * 2 + 1] - xs_line[i * 2])
                    if fill:
                        pygame.draw.line(world, self.terr_color, (xs_line[i * 2], y_line),
                                         (xs_line[i * 2 + 1], y_line), 10)

        if fill:
            for i in range(len(my_way)-1):
                pygame.draw.line(world, self.terr_color, my_way[i], my_way[i+1], 10)

        return k


w, h = 1000, 1000
w_window, h_window = 600, 400
window = pygame.display.set_mode((w_window, h_window))
pygame.display.set_caption('Paper_io')
window.fill((200, 200, 200))
clock = pygame.time.Clock()
pygame.font.init()
world = pygame.Surface((w, h), pygame.SRCALPHA)

world.fill((50, 50, 50))
pygame.draw.rect(world, (0, 0, 0, 0), (30, 30, w - 60, h - 60))
player1 = Player(w // 4, h // 2, (50, 50, 250, 255))

show, num_tick = True, 0
while show:
    num_tick += 1
    clock.tick(80)

    player1.run()
    player1.check_events()
    player1.draw()
