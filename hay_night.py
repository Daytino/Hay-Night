import pygame
import os
import ast
from threading import Timer
from random import randint

x = y = cur_x = cur_y = 0
grassed = bedded = bedden_wheat = inventory_opened = bedden_cauliflower = bedden_pumpkin \
    = bedden_melon = inventory_opened = False
tuple_of_vertical_paths = ((300, 60), (300, 120), (300, 180), (300, 240), (300, 300), (300, 360), (300, 420))
tuple_of_horizontal_paths = ((120, 60), (180, 60), (240, 60), (360, 420), (420, 420), (480, 420), (540, 420))
screen = pygame.display.set_mode((600, 480))
pygame.init()
costs_of_seeds = {"Wheat_Seeds": 5, "Cauliflower_Seeds": 15, "Melon_Seeds": 50, "Pumpkin_Seeds": 200}
costs_of_vegs = {"Wheat_Ripe": 8, "Cauliflower_Ripe": 25, "Melon_Ripe": 75, "Pumpkin_Ripe": 300}
cooords_of_beds_in_store = [[540, 0, 0], [480, 0, 10], [420, 0, 20], [360, 0, 50],
                            [540, 60, 100], [480, 60, 200], [420, 60, 400], [360, 60, 500],
                            [540, 120, 600], [480, 120, 1000], [420, 120, 1500], [360, 120, 2000],
                            [540, 180, 3000], [480, 180, 4000], [420, 180, 4000], [360, 180, 4000],
                            [540, 240, 4000], [480, 240, 4000], [420, 240, 4000], [360, 240, 4000],
                            [540, 300, 4000], [480, 300, 4000], [420, 300, 4000], [360, 300, 4000],
                            [540, 360, 4500], [480, 360, 4500], [420, 360, 4500], [360, 360, 4500],
                            [540, 420, 5000], [480, 420, 5000], [420, 420, 5000], [360, 420, 5000]]

with open("data/player_stats.txt") as file:
    lines = file.readlines()
    plr_coords = lines[0].strip()
    money = int(lines[1])
    amount_of_beds = int(lines[2])

with open("data/map.txt") as file:
    lines = file.readlines()
    coords_of_beds = ast.literal_eval(lines[0].strip()).get("coords_of_beds")
    coords_of_wheat_beds = ast.literal_eval(lines[0].strip()).get("coords_of_wheat_beds")
    coords_of_pumpkin_beds = ast.literal_eval(lines[0].strip()).get("coords_of_pumpkin_beds")
    coords_of_melon_beds = ast.literal_eval(lines[0].strip()).get("coords_of_melon_beds")
    coords_of_cauliflower_beds = ast.literal_eval(lines[0].strip()).get("coords_of_cauliflower_beds")

with open("data/inventory.txt") as file:
    lines = file.readlines()
    d = ast.literal_eval(lines[0].strip())
    Wheat_Ripe = ast.literal_eval(lines[0].strip()).get("Wheat_Ripe")
    Wheat_Seeds = ast.literal_eval(lines[0].strip()).get("Wheat_Seeds")
    Pumpkin_Ripe = ast.literal_eval(lines[0].strip()).get("Pumpkin_Ripe")
    Pumpkin_Seeds = ast.literal_eval(lines[0].strip()).get("Pumpkin_Seeds")
    Melon_Ripe = ast.literal_eval(lines[0].strip()).get("Melon_Ripe")
    Melon_Seeds = ast.literal_eval(lines[0].strip()).get("Melon_Seeds")
    Cauliflower_Ripe = ast.literal_eval(lines[0].strip()).get("Cauliflower_Ripe")
    Cauliflower_Seeds = ast.literal_eval(lines[0].strip()).get("Cauliflower_Seeds")
    inventory = {"Wheat_Ripe": Wheat_Ripe, "Wheat_Seeds": Wheat_Seeds, "Pumpkin_Ripe": Pumpkin_Ripe,
                 "Pumpkin_Seeds": Pumpkin_Seeds, "Melon_Ripe": Melon_Ripe, "Melon_Seeds": Melon_Seeds,
                 "Cauliflower_Ripe": Cauliflower_Ripe, "Cauliflower_Seeds": Cauliflower_Seeds}


def save():
    global inventory, all_coords
    with open("data/map.txt", "w") as file:
        file.truncate(0)
        all_coords = {"coords_of_beds": [i[:2] for i in cooords_of_beds_in_store[:amount_of_beds]],
                      "coords_of_wheat_beds": [],
                      "coords_of_pumpkin_beds": [],
                      "coords_of_melon_beds": [],
                      "coords_of_cauliflower_beds": []}
        file.write(str(all_coords))
        file.close()

    with open("data/inventory.txt", "w") as file:
        file.truncate(0)
        file.write(str(inventory))
        file.close()


def save_player_stats():
    global plr_coords
    with open("data/player_stats.txt", "w") as file:
        file.truncate(0)
        plr_coords = str(str(cur_x) + " " + str(cur_y))
        file.write(plr_coords + "\n" + str(money) + "\n" + str(amount_of_beds))
        file.close()


def blit():
    if x + y != 0:
        if [x, y] in coords_of_beds:
            GardenBed().blit()
        elif ([x, y, 1] in coords_of_wheat_beds) or ([x, y, 2] in coords_of_wheat_beds) or (
                [x, y, 3] in coords_of_wheat_beds):
            Wheat().blit(x, y)
        elif ([x, y, 1] in coords_of_cauliflower_beds) or ([x, y, 2] in coords_of_cauliflower_beds) or (
                [x, y, 3] in coords_of_cauliflower_beds):
            Cauliflower().blit()
        elif ([x, y, 1] in coords_of_pumpkin_beds) or ([x, y, 2] in coords_of_pumpkin_beds) or (
                [x, y, 3] in coords_of_pumpkin_beds) or ([x, y, 4] in coords_of_pumpkin_beds):
            Pumpkin().blit()
        elif ([x, y, 1] in coords_of_melon_beds) or ([x, y, 2] in coords_of_melon_beds) or (
                [x, y, 3] in coords_of_melon_beds) or ([x, y, 4] in coords_of_melon_beds):
            Melon().blit()
        else:
            Grass().blit()


def set_inventory_invisible():
    screen = pygame.display.set_mode((600, 480))


def set_inventory_visible():
    font = pygame.font.SysFont("Comic Sans", 25)
    title_font = pygame.font.SysFont("Comic Sans", 30, bold=True)
    font1 = pygame.font.SysFont("Comic Sans", 40)
    font2 = pygame.font.SysFont("Comic Sans", 40)
    font3 = pygame.font.SysFont("Comic Sans", 27)

    screen.blit(pygame.image.load("data/images/leaves.png"), (600, 0))

    # название
    screen.blit(title_font.render("    Inventory", True, 'orange'), (652, 2))

    # пшеница
    screen.blit(pygame.image.load("data/images/seeds/Wheat_Seeds.png"), (620, 48))
    screen.blit(font.render("Wheat Seeds" + '             ' + str(inventory["Wheat_Seeds"]), True, 'yellow'), (658, 46))

    # цветная капуста
    screen.blit(pygame.image.load("data/images/seeds/Cauliflower_Seeds.png"), (620, 87))
    screen.blit(font.render("Cauliflower Seeds" + '     ' + str(inventory['Cauliflower_Seeds']), True, 'yellow'),
                (658, 86))

    # дыня
    screen.blit(pygame.image.load("data/images/seeds/Melon_Seeds.png"), (620, 130))
    screen.blit(font.render("Melon Seeds" + '              ' + str(inventory["Melon_Seeds"]), True, 'yellow'), (658, 128))

    # тыква
    screen.blit(pygame.image.load("data/images/seeds/Pumpkin_Seeds.png"), (620, 170))
    screen.blit(font.render("Pumpkin Seeds" + '           ' + str(inventory['Pumpkin_Seeds']), True, 'yellow'), (657, 169))

    # созревшая пшеница
    screen.blit(pygame.image.load("data/images/vegs/Wheat_Ripe.png"), (620, 211))
    screen.blit(font.render("Ripe Wheat" + '               ' + str(inventory["Wheat_Ripe"]), True, 'yellow'), (663, 208))

    # созревшая цветная капуста
    screen.blit(pygame.image.load("data/images/vegs/Cauliflower_Ripe.png"), (620, 247))
    screen.blit(font.render("Ripe Cauliflower" + '        ' + str(inventory["Cauliflower_Ripe"]), True, 'yellow'),
                (662, 245))

    # созревшая дыня
    screen.blit(pygame.image.load("data/images/vegs/Melon_Ripe.png"), (619, 285))
    screen.blit(font.render("Ripe Melon" + '                ' + str(inventory["Melon_Ripe"]), True, 'yellow'), (665, 285))

    # созревшая тыква
    screen.blit(pygame.image.load("data/images/vegs/Pumpkin_Ripe.png"), (620, 325))
    screen.blit(font.render("Ripe Pumpkin" + '             ' + str(inventory["Pumpkin_Ripe"]), True, 'yellow'), (664, 322))

    screen.blit(pygame.transform.scale(pygame.image.load("data/images/beds/bed1.png"), (45, 45)), (614, 372))

    if amount_of_beds <= 27:
        screen.blit(font2.render(str(cooords_of_beds_in_store[amount_of_beds][2]), True, 'orange'), (669, 365))
    else:
        screen.blit(font3.render("Ground is no more", True, 'orange'), (668, 375))

    screen.blit(pygame.image.load("data/images/coin.png"), (616, 432))
    screen.blit(font1.render(str(money), True, 'orange'), (665, 422))

    pygame.display.flip()


def buy_land():
    global amount_of_beds, coords_of_beds, money
    if len(coords_of_beds) <= 30:
        if money >= cooords_of_beds_in_store[amount_of_beds][2]:
            money -= cooords_of_beds_in_store[amount_of_beds][2]
            GardenBed().place(cooords_of_beds_in_store[amount_of_beds][0], cooords_of_beds_in_store[amount_of_beds][1])
            coords_of_beds.append(
                [cooords_of_beds_in_store[amount_of_beds][0], cooords_of_beds_in_store[amount_of_beds][1]])
            amount_of_beds += 1
            playsound(2)
    elif len(coords_of_beds) <= 31:
        pygame.display.set_caption('Groung is no more')
        if money >= cooords_of_beds_in_store[amount_of_beds][2]:
            money -= cooords_of_beds_in_store[amount_of_beds][2]
            GardenBed().place(cooords_of_beds_in_store[amount_of_beds][0], cooords_of_beds_in_store[amount_of_beds][1])
            coords_of_beds.append(
                [cooords_of_beds_in_store[amount_of_beds][0], cooords_of_beds_in_store[amount_of_beds][1]])
            amount_of_beds += 1
            playsound(2)
    else:
        pygame.display.set_caption('Groung is no more')
    sell_buy_store()


def sell_buy_store():
    font = pygame.font.SysFont("Comic Sans", 24)
    inventory_font = pygame.font.SysFont("Comic Sans", 32, bold=True)
    font1 = pygame.font.SysFont("Comic Sans", 40)
    font2 = pygame.font.SysFont("Comic Sans", 40)
    font3 = pygame.font.SysFont("Comic Sans", 27)

    image = pygame.image.load("data/images/leaves.png")
    screen.blit(image, (600, 0))

    # название
    screen.blit(inventory_font.render("    Store", True, 'orange'), (670, 1))

    # пшеница
    screen.blit(pygame.image.load("data/images/seeds/Wheat_Seeds.png"), (617, 46))
    screen.blit(font.render("Wheat Seeds" + '           ' + str(costs_of_seeds["Wheat_Seeds"]), True, 'yellow'), (660, 47))

    # цветная капуста
    screen.blit(pygame.image.load("data/images/seeds/Cauliflower_Seeds.png"), (618, 84))
    screen.blit(font.render("Cauliflower Seeds" + '   ' + str(costs_of_seeds['Cauliflower_Seeds']), True, 'yellow'), (659, 84))

    # дыня
    screen.blit(pygame.image.load("data/images/seeds/Melon_Seeds.png"), (618, 125))
    screen.blit(font.render("Melon Seeds" + '           ' + str(costs_of_seeds["Melon_Seeds"]), True, 'yellow'), (661, 124))

    # тыква
    screen.blit(pygame.image.load("data/images/seeds/Pumpkin_Seeds.png"), (618, 166))
    screen.blit(font.render("Pumpkin Seeds" + '       ' + str(costs_of_seeds['Pumpkin_Seeds']), True, 'yellow'), (660, 165))

    screen.blit(pygame.transform.scale(pygame.image.load("data/images/beds/bed1.png"), (42, 42)), (614, 212))
    if amount_of_beds <= 27:
        screen.blit(font2.render(str(cooords_of_beds_in_store[amount_of_beds][2]), True, 'orange'), (669, 205))
    else:
        screen.blit(font3.render("Ground is no more", True, 'orange'), (668, 212))

    # созревшая пшеница
    screen.blit(pygame.image.load("data/images/vegs/Wheat_Ripe.png"), (620, 260))
    screen.blit(font.render("Ripe Wheat" + '          ' + str(inventory["Wheat_Ripe"] * costs_of_vegs['Wheat_Ripe']),
                            True, 'yellow'), (663, 257))

    # созревшая цветная капуста
    screen.blit(pygame.image.load("data/images/vegs/Cauliflower_Ripe.png"), (619, 295))
    screen.blit(font.render("Ripe Cauliflower" + '   ' + str(inventory["Cauliflower_Ripe"] * costs_of_vegs['Cauliflower_Ripe']), True, 'yellow'),
                (662, 295))

    # созревшая дыня
    screen.blit(pygame.image.load("data/images/vegs/Melon_Ripe.png"), (619, 333))
    screen.blit(font.render("Ripe Melon" + '           ' + str(inventory["Melon_Ripe"] * costs_of_vegs['Melon_Ripe']
                                                                 ), True, 'yellow'), (664, 332))

    # созревшая тыква
    screen.blit(pygame.image.load("data/images/vegs/Pumpkin_Ripe.png"), (620, 366))
    screen.blit(font.render("Ripe Pumpkin" + '        ' + str(inventory["Pumpkin_Ripe"] * costs_of_vegs
    ['Pumpkin_Ripe']), True, 'yellow'), (662, 368))

    image = pygame.image.load("data/images/coin.png")
    screen.blit(image, (616, 432))
    text = font1.render(str(money), True, 'orange')
    screen.blit(text, (665, 422))

    pygame.display.flip()


def store_leave():
    grassed = bedded = bedden_wheat = bedden_cauliflower = bedden_pumpkin = bedden_melon = False
    set_inventory_visible()
    g.__init__()
    r.__init__()
    b.__init__()
    w.__init__()
    c.__init__()
    pum.__init__()
    m.__init__()
    p.__init__()


def playsound(variant):
    if variant == 1:
        sound = pygame.mixer.Sound(f"data/sounds/grass{(randint(1, 4))}.wav")
        sound.play().set_volume(0.4)
    elif variant == 2:
        sound = pygame.mixer.Sound(f"data/sounds/shop.wav")
        sound.play().set_volume(0.4)


class Decoration(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("data/images/water.png"), (60, 60))
        self.rect = pygame.image.load("data/images/water.png").get_rect()

        screen.blit(self.image, (0, 300))
        screen.blit(self.image, (60, 300))
        screen.blit(self.image, (60, 360))
        screen.blit(self.image, (60, 420))

        screen.blit(pygame.image.load("data/images/bag.png"), (0, 180))
        screen.blit(pygame.transform.scale(pygame.image.load("data/images/barrel.png"), (60, 60)), (240, 420))
        screen.blit(pygame.transform.scale(pygame.image.load("data/images/barrel.png"), (60, 60)), (180, 420))
        screen.blit(pygame.transform.scale(pygame.image.load("data/images/ladle.png"), (60, 60)), (0, 240))
        screen.blit(pygame.transform.scale(pygame.image.load("data/images/stone.png"), (60, 60)), (0, 420))

        pygame.display.flip()


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 1
        self.cur_frame_direction = '+'
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame_direction == '+':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.cur_frame == 15:
                self.cur_frame_direction = '-'
        elif self.cur_frame_direction == '-':
            self.cur_frame = (self.cur_frame - 1) % len(self.frames)
            if self.cur_frame == 8:
                self.cur_frame_direction = '+'
        self.image = self.frames[self.cur_frame]
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/player/farmer_front.png")
        self.rect = pygame.image.load("data/images/player/farmer_front.png").get_rect()
        self.rect.x, self.rect.y = int(plr_coords.split()[0]), int(plr_coords.split()[1])
        self.blit()
        pygame.display.flip()

    def blit(self):
        screen.blit(self.image, self.rect)
        pygame.display.flip()

    def go_up(self):
        global x, y, cur_x, cur_y
        self.image = pygame.image.load("data/images/player/farmer_back.png")
        if self.rect.y != 0 and self.rect[:2] != [0, 180] and self.rect[:2] != [60, 180]:
            x, y = self.rect.x, self.rect.y
            self.rect.y -= 60
        self.after_moving()

    def go_down(self):
        global x, y, cur_x, cur_y
        self.image = pygame.image.load("data/images/player/farmer_front.png")
        if self.rect.y != 420:
            x, y = self.rect.x, self.rect.y
            self.rect.y += 60
        self.after_moving()

    def go_left(self):
        global x, y, cur_x, cur_y
        self.image = pygame.image.load("data/images/player/farmer_left.png")
        if self.rect.x != 0 and self.rect[:2] != [120, 0] and self.rect[:2] != [120, 60] and self.rect[:2] != [120,
                                                                                                               120]:
            x, y = self.rect.x, self.rect.y
            self.rect.x -= 60
        self.after_moving()

    def go_right(self):
        global x, y, cur_x, cur_y
        self.image = pygame.image.load("data/images/player/farmer_right.png")
        if self.rect.x != 540:
            x, y = self.rect.x, self.rect.y
            self.rect.x += 60
        self.after_moving()

    def after_moving(self):
        global cur_x, cur_y
        cur_x, cur_y = self.rect.x, self.rect.y
        save_player_stats()
        screen.blit(self.image, self.rect)
        pygame.display.flip()


class Grass(pygame.sprite.Sprite):
    def __init__(self):
        global grassed
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/grass.png")
        self.rect = pygame.image.load("data/images/grass.png").get_rect()
        if not grassed:
            for i in range(8):
                for j in range(10):
                    screen.blit(self.image, self.rect)
                    pygame.display.flip()
                    self.rect.x += 60
                self.rect.x = 0
                self.rect.y += 60
            grassed = True

    def blit(self):
        screen.blit(self.image, (x, y))
        pygame.display.flip()


class Roof(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.image.load(f"data/images/roof/roof_rightdown.png").get_rect()
        coordinates = ((0, 60), (0, 120), (0, 0), (60, 60), (60, 120), (60, 0))
        count = 0
        for image in tuple(os.walk("data/images/roof"))[0][2]:
            self.image = pygame.image.load(f"data/images/roof/{image}")
            self.rect.x, self.rect.y = coordinates[count][0], coordinates[count][1]
            screen.blit(self.image, self.rect)
            count += 1
        pygame.display.flip()


class GardenBed(pygame.sprite.Sprite):
    def __init__(self):
        global bedded
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"data/images/beds/bed.png")
        self.rect = pygame.image.load("data/images/beds/bed.png").get_rect()
        if not bedded:
            for i in coords_of_beds:
                screen.blit(self.image, (i[0], i[1]))
            pygame.display.flip()
            bedded = True

    def blit(self):
        screen.blit(self.image, (x, y))
        pygame.display.flip()

    def place(self, x, y):
        screen.blit(self.image, (x, y))
        pygame.display.flip()

    def replace(self, x_c, y_c):
        screen.blit(self.image, (x_c, y_c))
        pygame.display.flip()


class Wheat(pygame.sprite.Sprite):
    def __init__(self):
        global bedden_wheat
        self.rect = pygame.image.load(f"data/images/beds/wheat/stage1.png").get_rect()
        pygame.sprite.Sprite.__init__(self)
        if not bedden_wheat:
            for i in coords_of_wheat_beds:
                if i[2] == 1:
                    self.image = pygame.image.load(f"data/images/beds/wheat/stage1.png")
                elif i[2] == 2:
                    self.image = pygame.image.load(f"data/images/beds/wheat/stage2.png")
                elif i[2] == 3:
                    self.image = pygame.image.load(f"data/images/beds/wheat/stage3.png")
                screen.blit(self.image, (i[0], i[1]))
                self.x_pos, self.y_pos = i[0], i[1]
            pygame.display.flip()
            bedded_wheat = True

    def plant(self):
        global cur_x, cur_y, inventory
        inventory['Wheat_Seeds'] -= 1
        if inventory_opened:
            set_inventory_visible()
        self.image = pygame.image.load(f"data/images/beds/wheat/stage1.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        coords_of_beds.remove([cur_x, cur_y])
        coords_of_wheat_beds.append([cur_x, cur_y, 1])
        self.x_pos, self.y_pos = cur_x, cur_y
        p.blit()
        self.t = Timer(5.0, self.stage2)
        self.t.start()

    def stage2(self):
        self.image = pygame.image.load(f"data/images/beds/wheat/stage2.png")
        coords_of_wheat_beds[coords_of_wheat_beds.index([self.x_pos, self.y_pos, 1])][2] = 2
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(6.0, self.stage3)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage3(self):
        self.image = pygame.image.load(f"data/images/beds/wheat/stage3.png")
        coords_of_wheat_beds[coords_of_wheat_beds.index([self.x_pos, self.y_pos, 2])][2] = 3
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def harvest(self):
        global cur_x, cur_y, inventory
        inventory['Wheat_Ripe'] += 1
        if inventory_opened:
            set_inventory_visible()
        coords_of_beds.append([cur_x, cur_y])
        coords_of_wheat_beds.remove([cur_x, cur_y, 3])
        self.image = pygame.image.load(f"data/images/beds/bed.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def blit(self, x, y):
        try:
            if coords_of_wheat_beds[coords_of_wheat_beds.index([x, y, 1])][2] == 1:
                self.image = pygame.image.load(f"data/images/beds/wheat/stage1.png")
            elif coords_of_wheat_beds[coords_of_wheat_beds.index([x, y, 2])][2] == 2:
                self.image = pygame.image.load(f"data/images/beds/wheat/stage2.png")
            elif coords_of_wheat_beds[coords_of_wheat_beds.index([x, y, 3])][2] == 3:
                self.image = pygame.image.load(f"data/images/beds/wheat/stage3.png")
            screen.blit(self.image, (self.x_pos, self.y_pos))
            pygame.display.flip()
            p.blit()
        except ValueError:
            p.blit()
            pass


class Cauliflower(pygame.sprite.Sprite):
    def __init__(self):
        global bedden_cauliflower
        self.rect = pygame.image.load(f"data/images/beds/cauliflower/stage1.png").get_rect()
        pygame.sprite.Sprite.__init__(self)
        if not bedden_cauliflower:
            for i in coords_of_cauliflower_beds:
                if i[2] == 1:
                    self.image = pygame.image.load(f"data/images/beds/cauliflower/stage1.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 2:
                    self.image = pygame.image.load(f"data/images/beds/cauliflower/stage2.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 3:
                    self.image = pygame.image.load(f"data/images/beds/cauliflower/stage3.png")
                    screen.blit(self.image, (i[0], i[1]))
                self.x_pos, self.y_pos = i[0], i[1]
            pygame.display.flip()
            bedden_cauliflower = True

    def plant(self):
        global cur_x, cur_y, inventory
        inventory['Cauliflower_Seeds'] -= 1
        if inventory_opened:
            set_inventory_visible()
        self.image = pygame.image.load(f"data/images/beds/cauliflower/stage1.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        coords_of_beds.remove([cur_x, cur_y])
        coords_of_cauliflower_beds.append([cur_x, cur_y, 1])
        self.x_pos, self.y_pos = cur_x, cur_y
        p.blit()
        self.t = Timer(6.0, self.stage2)
        self.t.start()

    def stage2(self):
        self.image = pygame.image.load(f"data/images/beds/cauliflower/stage2.png")
        coords_of_cauliflower_beds[coords_of_cauliflower_beds.index([self.x_pos, self.y_pos, 1])][2] = 2
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(8.0, self.stage3)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage3(self):
        self.image = pygame.image.load(f"data/images/beds/cauliflower/stage3.png")
        coords_of_cauliflower_beds[coords_of_cauliflower_beds.index([self.x_pos, self.y_pos, 2])][2] = 3
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def harvest(self):
        global cur_x, cur_y, inventory
        inventory['Cauliflower_Ripe'] += 1
        if inventory_opened:
            set_inventory_visible()
        coords_of_beds.append([cur_x, cur_y])
        coords_of_cauliflower_beds.remove([cur_x, cur_y, 3])
        self.image = pygame.image.load(f"data/images/beds/bed.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def blit(self):
        for i in coords_of_cauliflower_beds:
            if i[2] == 1:
                self.image = pygame.image.load(f"data/images/beds/cauliflower/stage1.png")
            elif i[2] == 2:
                self.image = pygame.image.load(f"data/images/beds/cauliflower/stage2.png")
            elif i[2] == 3:
                self.image = pygame.image.load(f"data/images/beds/cauliflower/stage3.png")
            screen.blit(self.image, (i[0], i[1]))
            pygame.display.flip()
            if cur_x == i[0] and cur_y == i[1]:
                p.blit()


class Melon(pygame.sprite.Sprite):
    def __init__(self):
        global bedden_melon
        self.rect = pygame.image.load(f"data/images/beds/melon/stage1.png").get_rect()
        pygame.sprite.Sprite.__init__(self)
        if not bedden_melon:
            for i in coords_of_melon_beds:
                if i[2] == 1:
                    self.image = pygame.image.load(f"data/images/beds/melon/stage1.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 2:
                    self.image = pygame.image.load(f"data/images/beds/melon/stage2.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 3:
                    self.image = pygame.image.load(f"data/images/beds/melon/stage3.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 4:
                    self.image = pygame.image.load(f"data/images/beds/melon/stage4.png")
                    screen.blit(self.image, (i[0], i[1]))
                self.x_pos, self.y_pos = i[0], i[1]
            pygame.display.flip()
            bedden_melon = True

    def plant(self):
        global cur_x, cur_y, inventory
        inventory['Melon_Seeds'] -= 1
        if inventory_opened:
            set_inventory_visible()
        self.image = pygame.image.load(f"data/images/beds/melon/stage1.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        coords_of_beds.remove([cur_x, cur_y])
        coords_of_melon_beds.append([cur_x, cur_y, 1])
        self.x_pos, self.y_pos = cur_x, cur_y
        p.blit()
        self.t = Timer(8.0, self.stage2)
        self.t.start()

    def stage2(self):
        self.image = pygame.image.load(f"data/images/beds/melon/stage2.png")
        coords_of_melon_beds[coords_of_melon_beds.index([self.x_pos, self.y_pos, 1])][2] = 2
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(9.0, self.stage3)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage3(self):
        self.image = pygame.image.load(f"data/images/beds/melon/stage3.png")
        coords_of_melon_beds[coords_of_melon_beds.index([self.x_pos, self.y_pos, 2])][2] = 3
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(2.0, self.stage4)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage4(self):
        self.image = pygame.image.load(f"data/images/beds/melon/stage4.png")
        coords_of_melon_beds[coords_of_melon_beds.index([self.x_pos, self.y_pos, 3])][2] = 4
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def harvest(self):
        global cur_x, cur_y, inventory
        inventory['Melon_Ripe'] += 1
        if inventory_opened:
            set_inventory_visible()
        coords_of_beds.append([cur_x, cur_y])
        coords_of_melon_beds.remove([cur_x, cur_y, 4])
        self.image = pygame.image.load(f"data/images/beds/bed.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def blit(self):
        for i in coords_of_melon_beds:
            if i[2] == 1:
                self.image = pygame.image.load(f"data/images/beds/melon/stage1.png")
            elif i[2] == 2:
                self.image = pygame.image.load(f"data/images/beds/melon/stage2.png")
            elif i[2] == 3:
                self.image = pygame.image.load(f"data/images/beds/melon/stage3.png")
            elif i[2] == 4:
                self.image = pygame.image.load(f"data/images/beds/melon/stage4.png")
            screen.blit(self.image, (i[0], i[1]))
            pygame.display.flip()
            if cur_x == i[0] and cur_y == i[1]:
                p.blit()


class Pumpkin(pygame.sprite.Sprite):
    def __init__(self):
        global bedden_pumpkin
        self.rect = pygame.image.load(f"data/images/beds/pumpkin/stage1.png").get_rect()
        pygame.sprite.Sprite.__init__(self)
        if not bedden_pumpkin:
            for i in coords_of_pumpkin_beds:
                if i[2] == 1:
                    self.image = pygame.image.load(f"data/images/beds/pumpkin/stage1.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 2:
                    self.image = pygame.image.load(f"data/images/beds/pumpkin/stage2.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 3:
                    self.image = pygame.image.load(f"data/images/beds/pumpkin/stage3.png")
                    screen.blit(self.image, (i[0], i[1]))
                elif i[2] == 4:
                    self.image = pygame.image.load(f"data/images/beds/pumpkin/stage4.png")
                    screen.blit(self.image, (i[0], i[1]))
                self.x_pos, self.y_pos = i[0], i[1]
            pygame.display.flip()
            bedden_pumpkin = True

    def plant(self):
        global cur_x, cur_y, inventory
        inventory['Pumpkin_Seeds'] -= 1
        if inventory_opened:
            set_inventory_visible()
        self.image = pygame.image.load(f"data/images/beds/pumpkin/stage1.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        coords_of_beds.remove([cur_x, cur_y])
        coords_of_pumpkin_beds.append([cur_x, cur_y, 1])
        self.x_pos, self.y_pos = cur_x, cur_y
        p.blit()
        self.t = Timer(9.0, self.stage2)
        self.t.start()

    def stage2(self):
        self.image = pygame.image.load(f"data/images/beds/pumpkin/stage2.png")
        coords_of_pumpkin_beds[coords_of_pumpkin_beds.index([self.x_pos, self.y_pos, 1])][2] = 2
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(10.0, self.stage3)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage3(self):
        self.image = pygame.image.load(f"data/images/beds/pumpkin/stage3.png")
        coords_of_pumpkin_beds[coords_of_pumpkin_beds.index([self.x_pos, self.y_pos, 2])][2] = 3
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        self.t = Timer(2.0, self.stage4)
        self.t.start()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def stage4(self):
        self.image = pygame.image.load(f"data/images/beds/pumpkin/stage4.png")
        coords_of_pumpkin_beds[coords_of_pumpkin_beds.index([self.x_pos, self.y_pos, 3])][2] = 4
        self.rect.x, self.rect.y = self.x_pos, self.y_pos
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def harvest(self):
        global cur_x, cur_y, inventory
        inventory['Pumpkin_Ripe'] += 1
        if inventory_opened:
            set_inventory_visible()
        coords_of_beds.append([cur_x, cur_y])
        coords_of_pumpkin_beds.remove([cur_x, cur_y, 4])
        self.image = pygame.image.load(f"data/images/beds/bed.png")
        self.rect.x, self.rect.y = cur_x, cur_y
        screen.blit(self.image, self.rect)
        pygame.display.flip()
        if cur_x == self.rect.x and cur_y == self.rect.y:
            p.blit()

    def blit(self):
        for i in coords_of_pumpkin_beds:
            if i[2] == 1:
                self.image = pygame.image.load(f"data/images/beds/pumpkin/stage1.png")
                screen.blit(self.image, (i[0], i[1]))
            elif i[2] == 2:
                self.image = pygame.image.load(f"data/images/beds/pumpkin/stage2.png")
                screen.blit(self.image, (i[0], i[1]))
            elif i[2] == 3:
                self.image = pygame.image.load(f"data/images/beds/pumpkin/stage3.png")
                screen.blit(self.image, (i[0], i[1]))
            elif i[2] == 4:
                self.image = pygame.image.load(f"data/images/beds/pumpkin/stage4.png")
                screen.blit(self.image, (i[0], i[1]))
            pygame.display.flip()
            if cur_x == i[0] and cur_y == i[1]:
                p.blit()


if __name__ == '__main__':
    pygame.display.set_icon(pygame.image.load("data/images/chicken_night.png"))
    pygame.display.set_caption('HayNight')
    all_sprites = SpriteGroup()
    coin = AnimatedSprite(pygame.image.load("data/images/rotating_coin.png"), 8, 1, 180, 0)
    clock = pygame.time.Clock()
    FPS = 10
    g = Grass()
    r, b, w, c, pum, m, d, p = Roof(), GardenBed(), Wheat(), Cauliflower(), Pumpkin(), Melon(), Decoration(), Player()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cur_x == 180 and cur_y == 0:
                    if not inventory_opened:
                        if 620 <= event.pos[0] <= 816 and 45 <= event.pos[1] <= 72:
                            if money >= 5:
                                playsound(2)
                                inventory["Wheat_Seeds"] += 1
                                money -= 5
                                sell_buy_store()
                        if 620 <= event.pos[0] <= 860 and 80 <= event.pos[1] <= 110:
                            if money >= 15:
                                playsound(2)
                                inventory["Cauliflower_Seeds"] += 1
                                money -= 15
                                sell_buy_store()
                        if 620 <= event.pos[0] <= 803 and 125 <= event.pos[1] <= 150:
                            if money >= 50:
                                playsound(2)
                                inventory["Melon_Seeds"] += 1
                                money -= 50
                                sell_buy_store()
                        if 618 <= event.pos[0] <= 825 and 166 <= event.pos[1] <= 190:
                            if money >= 200:
                                playsound(2)
                                inventory["Pumpkin_Seeds"] += 1
                                money -= 200
                                sell_buy_store()
                        if 614 <= event.pos[0] <= 735 and 211 <= event.pos[1] <= 247:
                            buy_land()

                        if 618 <= event.pos[0] <= 792 and 255 <= event.pos[1] <= 285:
                            if inventory["Wheat_Ripe"] != 0:
                                playsound(2)
                            money += inventory["Wheat_Ripe"] * costs_of_vegs["Wheat_Ripe"]
                            inventory["Wheat_Ripe"] = 0
                            sell_buy_store()
                        if 617 <= event.pos[0] <= 842 and 297 <= event.pos[1] <= 322:
                            if inventory["Cauliflower_Ripe"] != 0:
                                playsound(2)
                            money += inventory["Cauliflower_Ripe"] * costs_of_vegs["Cauliflower_Ripe"]
                            inventory["Cauliflower_Ripe"] = 0
                            sell_buy_store()
                        if 619 <= event.pos[0] <= 786 and 333 <= event.pos[1] <= 358:
                            if inventory["Melon_Ripe"] != 0:
                                playsound(2)
                            money += inventory["Melon_Ripe"] * costs_of_vegs["Melon_Ripe"]
                            inventory["Melon_Ripe"] = 0
                            sell_buy_store()
                        if 618 <= event.pos[0] <= 807 and 370 <= event.pos[1] <= 392:
                            if inventory["Pumpkin_Ripe"] != 0:
                                playsound(2)
                            money += inventory["Pumpkin_Ripe"] * costs_of_vegs["Pumpkin_Ripe"]
                            inventory["Pumpkin_Ripe"] = 0
                            sell_buy_store()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    xy = [cur_x, cur_y]
                    if xy != [0, 240] and xy != [60, 240] and xy != [180, 360] and xy != [240, 360] and cur_y != 420:
                        p.go_down()
                    blit()
                    if x == 180 and y == 0:
                        store_leave()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    xy = [cur_x, cur_y]
                    if xy != [0, 180] and xy != [60, 180] and cur_y != 0:
                        p.go_up()
                    blit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    xy = [cur_x, cur_y]
                    if xy != [120, 300] and xy != [120, 360] and xy != [120, 420]\
                            and xy != [120, 0] and xy != [120, 60] and xy != [120, 120]\
                            and xy != [60, 180] and xy != [60, 240] and xy != [60, 180] and xy != [300, 420] and cur_x != 0:
                        p.go_left()
                    blit()
                    if x == 180 and y == 0:
                        store_leave()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    xy = [cur_x, cur_y]
                    if xy != [120, 420] and cur_x != 540:
                        p.go_right()
                    blit()
                    if x == 180 and y == 0:
                        store_leave()

                if event.key == pygame.K_u:
                    if [cur_x, cur_y] in coords_of_beds and inventory['Wheat_Seeds'] > 0:
                        Wheat().plant()
                        playsound(1)
                    elif [cur_x, cur_y, 3] in coords_of_wheat_beds:
                        Wheat().harvest()
                        playsound(1)
                    set_inventory_visible()
                if event.key == pygame.K_i:
                    if [cur_x, cur_y] in coords_of_beds and inventory['Cauliflower_Seeds'] > 0:
                        Cauliflower().plant()
                        playsound(1)
                    elif [cur_x, cur_y, 3] in coords_of_cauliflower_beds:
                        Cauliflower().harvest()
                        playsound(1)
                    set_inventory_visible()
                if event.key == pygame.K_o:
                    if [cur_x, cur_y] in coords_of_beds and inventory['Melon_Seeds'] > 0:
                        Melon().plant()
                        playsound(1)
                    elif [cur_x, cur_y, 4] in coords_of_melon_beds:
                        Melon().harvest()
                        playsound(1)
                    set_inventory_visible()
                if event.key == pygame.K_p:
                    if [cur_x, cur_y] in coords_of_beds and inventory['Pumpkin_Seeds'] > 0:
                        Pumpkin().plant()
                        playsound(1)
                    elif [cur_x, cur_y, 4] in coords_of_pumpkin_beds:
                        Pumpkin().harvest()
                        playsound(1)
                    set_inventory_visible()

                if event.key == pygame.K_e:
                    pygame.display.set_caption(str(money))
                if event.key == pygame.K_f:
                    grassed = bedded = bedden_wheat = bedden_cauliflower = bedden_pumpkin = bedden_melon = False
                    if not inventory_opened:
                        screen = pygame.display.set_mode((940, 480))
                        set_inventory_visible()
                        inventory_opened = True
                    else:
                        set_inventory_invisible()
                        inventory_opened = False
                    g.__init__()
                    d.__init__()
                    r.__init__()
                    b.__init__()
                    w.__init__()
                    c.__init__()
                    pum.__init__()
                    m.__init__()
                    p.__init__()
                if event.key == pygame.K_c:
                    if cur_x == 180 and cur_y == 0:
                        screen = pygame.display.set_mode((940, 480))
                        grassed = bedded = bedden_wheat = bedden_cauliflower = bedden_pumpkin = bedden_melon = False
                        if inventory_opened:
                            inventory_opened = False
                        sell_buy_store()
                        g.__init__()
                        d.__init__()
                        r.__init__()
                        b.__init__()
                        w.__init__()
                        c.__init__()
                        pum.__init__()
                        m.__init__()
                        p.__init__()
            if event.type == pygame.KEYUP:
                pygame.display.set_caption('HayNight')
            if event.type == pygame.QUIT:
                with open("data/player_stats.txt", "w") as file:
                    file.truncate(0)
                    plr_coords = "120 60"
                    file.write(plr_coords + "\n" + str(money) + "\n" + str(amount_of_beds))
                    file.close()
                for i in coords_of_wheat_beds:
                    if i[2] == 1 or i[2] == 2:
                        inventory['Wheat_Seeds'] += 1
                    elif i[2] == 3:
                        inventory['Wheat_Ripe'] += 1
                for i in coords_of_pumpkin_beds:
                    if i[2] == 1 or i[2] == 2 or i[2] == 3:
                        inventory['Pumpkin_Seeds'] += 1
                    elif i[2] == 4:
                        inventory['Pumpkin_Ripe'] += 1
                for i in coords_of_melon_beds:
                    if i[2] == 1 or i[2] == 2 or i[2] == 3:
                        inventory['Melon_Seeds'] += 1
                    elif i[2] == 4:
                        inventory['Melon_Ripe'] += 1
                for i in coords_of_cauliflower_beds:
                    if i[2] == 1 or i[2] == 2 or i[2] == 3:
                        inventory['Cauliflower_Seeds'] += 1
                    elif i[2] == 4:
                        inventory['Cauliflower_Ripe'] += 1
                save()
                running = False
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
