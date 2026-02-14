import pygame
import sys
import random

# ========================
# Налаштування
# ========================
pygame.init()
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Монополія - Ходи по клітинках")
FONT = pygame.font.SysFont("Arial", 18)
BIG_FONT = pygame.font.SysFont("Arial", 28)
CLOCK = pygame.time.Clock()

START_MONEY = 1500
PASS_START_BONUS = 200

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 100)
ORANGE = (255, 165, 0)
BUTTON_COLOR = (0, 120, 255)
BUTTON_HOVER = (0, 180, 255)

# ========================
# Поле (24 клітинки)
# ========================
TILE_SIZE = 80
BOARD_POSITIONS = []
OFFSET_X, OFFSET_Y = 150, 150

for i in range(8):
    BOARD_POSITIONS.append((OFFSET_X + i*TILE_SIZE, OFFSET_Y))
for i in range(1, 7):
    BOARD_POSITIONS.append((OFFSET_X + 7*TILE_SIZE, OFFSET_Y + i*TILE_SIZE))
for i in range(6, -2, -1):
    BOARD_POSITIONS.append((OFFSET_X + i*TILE_SIZE, OFFSET_Y + 6*TILE_SIZE))
for i in range(5, 3, -1):
    BOARD_POSITIONS.append((OFFSET_X, OFFSET_Y + i*TILE_SIZE))

# ========================
# Міста та типи
# ========================
cities = ["Київ","Львів","Одеса","Харків","Дніпро","Вінниця","Чернівці","Запоріжжя",
          "Полтава","Житомир","Черкаси","Миколаїв","Херсон","Суми","Івано-Франківськ",
          "Рівне","Луцьк","Тернопіль","Хмельницький","Кропивницький","Ужгород","Біла Церква",
          "Кам'янець-Подільський","Чернігів"]

board = []
types = ["start", "city", "city", "chance", "city", "tax", "city", "chance",
         "city", "city", "city", "chance", "city", "tax", "city", "chance",
         "city", "city", "city", "chance", "city", "tax", "city", "jail"]

prices = [0, 500, 450, 0, 400, 100, 350, 0,
          300, 250, 200, 0, 150, 100, 120, 0,
          180, 220, 270, 0, 300, 100, 350, 0]

for i in range(24):
    tile_type = types[i]
    name = cities[i] if tile_type == "city" else types[i].capitalize()
    if tile_type == "city":
        board.append({"name": name, "type": "city",
                      "price": prices[i], "rent": prices[i]//10, "owner": None, "level":0})
    elif tile_type == "tax":
        board.append({"name": "Податок", "type": "tax", "amount": 100})
    elif tile_type == "chance":
        board.append({"name": "Шанс", "type": "chance"})
    elif tile_type == "start":
        board.append({"name": "Старт", "type": "start"})
    elif tile_type == "jail":
        board.append({"name": "В'язниця", "type": "jail"})

# ========================
# Гравець
# ========================
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pos = 0
        self.money = START_MONEY
        self.properties = []

    def move_one(self):
        old_pos = self.pos
        self.pos = (self.pos + 1) % len(board)
        if self.pos < old_pos:
            self.money += PASS_START_BONUS

# ========================
# Кубик
# ========================
def roll_dice():
    return random.randint(1, 6)

# ========================
# Малювання поля та гравців
# ========================
def draw_board(win, players):
    win.fill(GREEN)
    for i, tile in enumerate(board):
        x, y = BOARD_POSITIONS[i]
        color = YELLOW if tile["type"] == "city" else GRAY
        pygame.draw.rect(win, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(win, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
        text_name = tile["name"]
        if tile["type"]=="city" and tile.get("level",0)>0:
            text_name += f" ({tile['level']})"
        text_surf = FONT.render(text_name, True, BLACK)
        text_rect = text_surf.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        win.blit(text_surf, text_rect)
    for idx, player in enumerate(players):
        x, y = BOARD_POSITIONS[player.pos]
        offset = idx * 15
        pygame.draw.circle(win, player.color, (x + TILE_SIZE//2 + offset, y + TILE_SIZE//2), 12)

# ========================
# Малювання кнопок
# ========================
def draw_button(win, text, rect, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(win, color, rect)
    pygame.draw.rect(win, BLACK, rect, 2)
    text_surf = BIG_FONT.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    win.blit(text_surf, text_rect)

# ========================
# Стартове меню для гравців
# ========================
def start_screen():
    input_box = pygame.Rect(WIDTH//2 - 50, HEIGHT//2, 100, 50)
    color_inactive = GRAY
    color_active = BLUE
    color = color_inactive
    active = False
    text = ''
    while True:
        WIN.fill(GREEN)
        msg = BIG_FONT.render("Введіть кількість гравців (2-4):", True, WHITE)
        msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        WIN.blit(msg, msg_rect)
        txt_surface = BIG_FONT.render(text, True, BLACK)
        WIN.blit(txt_surface, (input_box.x+10, input_box.y+10))
        pygame.draw.rect(WIN, color, input_box, 2)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type==pygame.KEYDOWN and active:
                if event.key==pygame.K_RETURN:
                    if text.isdigit() and 2 <= int(text) <=4:
                        return int(text)
                    text=''
                elif event.key==pygame.K_BACKSPACE:
                    text=text[:-1]
                else:
                    if len(text)<1:
                        text += event.unicode
        pygame.display.update()
        CLOCK.tick(30)

# ========================
# Продаж міста під заставу
# ========================
def mortgage_property(player):
    if not player.properties:
        return False, "У вас немає міст для застави!"
    tile = player.properties.pop(0)
    tile["owner"] = None
    tile["level"] = 0
    money_gained = tile["price"]//2
    player.money += money_gained
    return True, f"{player.name} продав {tile['name']} під заставу за {money_gained}$"

# ========================
# Обробка клітинки
# ========================
def handle_tile(player):
    tile = board[player.pos]
    message = ""
    buy_prompt = False
    upgrade_prompt = False
    mortgage_prompt = False

    if tile["type"]=="city":
        if tile["owner"] is None:
            message = f"{player.name}, купити {tile['name']} за {tile['price']}$?"
            buy_prompt = True
        elif tile["owner"]==player:
            message = f"{player.name} на власному місті {tile['name']}"
            upgrade_prompt = True
        else:
            rent = tile["rent"] * (1 + tile.get("level",0))
            player.money -= rent
            tile["owner"].money += rent
            message = f"{player.name} платить оренду {rent}$ гравцю {tile['owner'].name}"
    elif tile["type"]=="tax":
        player.money -= tile["amount"]
        message = f"{player.name} платить податок {tile['amount']}$"
    elif tile["type"]=="chance":
        event = random.choice(["money","lose","move"])
        if event=="money":
            player.money += 100
            message = f"{player.name} виграв 100$"
        elif event=="lose":
            player.money -=50
            message = f"{player.name} втратив 50$"
        else:
            player.move_one()
            message = f"{player.name} пересунувся на 1 клітинку через шанс"
            handle_tile(player)
    elif tile["type"]=="jail":
        message = f"{player.name} у в'язниці :)"

    if player.money < 0:
        mortgage_prompt = True

    return message, buy_prompt, upgrade_prompt, mortgage_prompt

# ========================
# Баланс гравців
# ========================
def draw_balance(win, players):
    start_y = 200
    pygame.draw.rect(win, GRAY, (WIDTH-220, start_y, 210, 30 + len(players)*30))
    pygame.draw.rect(win, BLACK, (WIDTH-220, start_y, 210, 30 + len(players)*30), 2)
    title = BIG_FONT.render("Баланс гравців", True, BLACK)
    win.blit(title, (WIDTH-210, start_y + 5))
    for idx, p in enumerate(players):
        text = FONT.render(f"{p.name}: {p.money}$", True, p.color)
        win.blit(text, (WIDTH-210, start_y + 40 + idx*25))

# ========================
# Головна гра
# ========================
def main():
    num_players = start_screen()
    colors = [RED, BLUE, ORANGE, BLACK]
    players = [Player(f"Гравець {i+1}", colors[i]) for i in range(num_players)]
    turn = 0
    last_message = ""
    buy_prompt = False
    upgrade_prompt = False
    mortgage_prompt = False
    current_player = None

    dice_roll = 0
    steps_left = 0

    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 80)
    buy_yes_rect = pygame.Rect(WIDTH//2 - 110, HEIGHT//2 + 50, 100, 50)
    buy_no_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 50, 100, 50)
    upgrade_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 120, 100, 50)
    mortgage_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 50, 240, 50)

    while True:
        CLOCK.tick(30)
        mouse_pos = pygame.mouse.get_pos()
        hover_button = button_rect.collidepoint(mouse_pos)
        hover_yes = buy_yes_rect.collidepoint(mouse_pos)
        hover_no = buy_no_rect.collidepoint(mouse_pos)
        hover_upgrade = upgrade_rect.collidepoint(mouse_pos)
        hover_mortgage = mortgage_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                # Купівля
                if buy_prompt:
                    if hover_yes:
                        tile = board[current_player.pos]
                        if current_player.money >= tile["price"]:
                            current_player.money -= tile["price"]
                            tile["owner"] = current_player
                            current_player.properties.append(tile)
                            last_message = f"{current_player.name} купив {tile['name']} за {tile['price']}$"
                        else:
                            last_message = f"Недостатньо грошей!"
                        buy_prompt = False
                        turn = (turn+1)%len(players)
                        dice_roll = 0
                        steps_left = 0
                    elif hover_no:
                        last_message = f"{current_player.name} пропустив покупку"
                        buy_prompt = False
                        turn = (turn+1)%len(players)
                        dice_roll = 0
                        steps_left = 0
                # Прокачка
                elif upgrade_prompt and hover_upgrade:
                    tile = board[current_player.pos]
                    upgrade_cost = tile['price']//2
                    if current_player.money >= upgrade_cost:
                        current_player.money -= upgrade_cost
                        tile['level'] +=1
                        last_message = f"{current_player.name} прокачав {tile['name']} до рівня {tile['level']}"
                    else:
                        last_message = "Недостатньо грошей для прокачки!"
                    upgrade_prompt = False
                    turn = (turn+1)%len(players)
                    dice_roll = 0
                    steps_left = 0
                # Застава
                elif mortgage_prompt and hover_mortgage:
                    success, msg = mortgage_property(current_player)
                    last_message = msg
                    if not success:
                        players.remove(current_player)
                        if len(players)==1:
                            last_message += f" {players[0].name} виграв гру!"
                            pygame.display.update()
                            pygame.time.wait(5000)
                            pygame.quit()
                            sys.exit()
                    mortgage_prompt = False
                    turn = (turn+1)%len(players)
                    dice_roll = 0
                    steps_left = 0
                # Кинути кубик лише якщо не рухаємося
                elif steps_left == 0 and not buy_prompt and not upgrade_prompt and not mortgage_prompt and hover_button:
                    current_player = players[turn]
                    dice_roll = roll_dice()
                    steps_left = dice_roll
                    last_message = f"{current_player.name} випало {dice_roll}"

        # Рух по одній клітинці за кадр
        if steps_left > 0:
            current_player.move_one()
            steps_left -= 1
            if steps_left == 0:
                last_message, buy_prompt, upgrade_prompt, mortgage_prompt = handle_tile(current_player)

        # Малюємо поле та гравців
        draw_board(WIN, players)

        # Кнопки
        if mortgage_prompt:
            draw_button(WIN, "Продати місто під заставу", mortgage_rect, hover_mortgage)
        elif buy_prompt:
            draw_button(WIN, "Купити", buy_yes_rect, hover_yes)
            draw_button(WIN, "Пропустити", buy_no_rect, hover_no)
        elif upgrade_prompt:
            draw_button(WIN, "Прокачати", upgrade_rect, hover_upgrade)
        elif steps_left == 0:
            draw_button(WIN, "Кинути кубик", button_rect, hover_button)

        # Повідомлення по центру верхньої частини
        msg_surf = BIG_FONT.render(last_message, True, BLACK)
        msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
        WIN.blit(msg_surf, msg_rect)

        # Баланс праворуч, нижче
        draw_balance(WIN, players)

        pygame.display.update()

if __name__=="__main__":
    main()
