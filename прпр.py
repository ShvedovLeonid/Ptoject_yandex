import arcade
import random

# Константы
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Doodle Jump"
PLAYER_SCALE = 0.8
PLAYER_IMAGE = "player.png"


class DoodleJump(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Уровень
        self.level = 1
        self.level_up_score = 1000  # Очков для перехода на уровень 2

        # Параметры игры (уровень 1 по умолчанию)
        self.gravity = 0.4
        self.jump_speed = 18
        self.move_speed = 5
        self.platform_width = 100
        self.platform_height = 30
        self.min_gap = 80
        self.max_gap = 150

        # Позиция игрока
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 3
        self.player_velocity_y = 0
        self.player_speed_x = 0
        self.player_facing_right = True

        # Спрайты
        self.player_sprite = None
        self.all_sprites = arcade.SpriteList()

        # Платформы
        self.platforms = []
        self.highest_y = 0
        self.camera_offset_y = 0

        # Игровые переменные
        self.score = 0
        self.game_over = False

        self.setup()

    def load_high_score(self):
        """Загружает рекорд из файла"""
        try:
            with open("high_score.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

    def save_high_score(self):
        """Сохраняет рекорд в файл"""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("high_score.txt", "w") as f:
                    f.write(str(self.high_score))
            except:
                pass

    def setup_level_params(self):
        """Меняет параметры на уровень 2"""
        if self.level == 2:
            # Сложный уровень
            self.gravity = 0.5
            self.jump_speed = 17
            self.move_speed = 6
            self.platform_width = 90
            self.min_gap = 110
            self.max_gap = 170

    def setup(self):
        """Инициализация игры"""
        # Сброс параметров к уровню 1
        self.level = 1
        self.gravity = 0.4
        self.jump_speed = 18
        self.move_speed = 5
        self.platform_width = 100
        self.platform_height = 30
        self.min_gap = 80
        self.max_gap = 150

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 3
        self.player_velocity_y = 0
        self.player_speed_x = 0
        self.player_facing_right = True

        # Спрайт
        self.all_sprites.clear()
        self.player_sprite = arcade.Sprite(PLAYER_IMAGE, PLAYER_SCALE)
        self.player_sprite.center_x = self.player_x
        self.player_sprite.center_y = self.player_y
        self.all_sprites.append(self.player_sprite)

        # Сброс
        self.camera_offset_y = 0
        self.platforms.clear()
        self.highest_y = self.player_y
        self.score = 0
        self.game_over = False

        # Платформы
        self.create_initial_platforms()

    def create_initial_platforms(self):
        """Создание начальных платформ"""
        start_y = self.player_y - 50
        self.add_platform(SCREEN_WIDTH // 2, start_y)

        # Платформы ниже
        current_y = start_y - 100
        while current_y > -SCREEN_HEIGHT:
            self.add_platform(
                random.randint(50, SCREEN_WIDTH - 50),
                current_y
            )
            current_y -= random.randint(self.min_gap, self.max_gap)

        # Платформы выше
        current_y = start_y + 100
        while current_y < SCREEN_HEIGHT * 3:
            self.add_platform(
                random.randint(50, SCREEN_WIDTH - 50),
                current_y
            )
            current_y += random.randint(self.min_gap, self.max_gap)

    def add_platform(self, x, y):
        """Добавление новой платформы"""
        left = x - self.platform_width // 2
        bottom = y - self.platform_height // 2
        right = x + self.platform_width // 2
        top = y + self.platform_height // 2

        self.platforms.append({
            'left': left, 'bottom': bottom, 'right': right, 'top': top,
            'color': random.choice([
                arcade.color.GREEN, arcade.color.BLUE, arcade.color.RED,
                arcade.color.YELLOW, arcade.color.PURPLE
            ]),
            'x': x, 'y': y
        })

    def update_platforms(self):
        """Обновление платформ"""
        # Удаляем далекие платформы
        self.platforms = [
            platform for platform in self.platforms
            if platform['y'] > self.player_y - SCREEN_HEIGHT * 2
        ]

        # Генерируем новые
        if self.platforms:
            highest_platform = max(self.platforms, key=lambda p: p['y'])
            if highest_platform['y'] < self.player_y + SCREEN_HEIGHT * 2:
                current_y = highest_platform['y'] + random.randint(self.min_gap, self.max_gap)
                for _ in range(3):
                    self.add_platform(
                        random.randint(50, SCREEN_WIDTH - 50),
                        current_y
                    )
                    current_y += random.randint(self.min_gap, self.max_gap)

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Рисуем платформы
        for platform in self.platforms:
            platform_bottom = platform['bottom'] - self.camera_offset_y
            platform_top = platform['top'] - self.camera_offset_y

            if platform_top > 0 and platform_bottom < SCREEN_HEIGHT:
                arcade.draw_lrbt_rectangle_filled(
                    platform['left'],
                    platform['right'],
                    platform_bottom,
                    platform_top,
                    platform['color']
                )

                arcade.draw_lrbt_rectangle_outline(
                    platform['left'],
                    platform['right'],
                    platform_bottom,
                    platform_top,
                    arcade.color.BLACK,
                    1
                )

        # Рисуем игрока
        player_screen_y = self.player_y - self.camera_offset_y
        if -50 < player_screen_y < SCREEN_HEIGHT + 50:
            if self.player_sprite:
                self.player_sprite.center_y = player_screen_y
                self.player_sprite.center_x = self.player_x
                self.all_sprites.draw()

        # GUI
        arcade.draw_text(f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30,
                         arcade.color.BLACK, 20, bold=True)
        arcade.draw_text(f"Высота: {int(self.player_y)}", 10, SCREEN_HEIGHT - 60,
                         arcade.color.DARK_BLUE, 16)
        arcade.draw_text(f"Уровень: {self.level}", 10, SCREEN_HEIGHT - 90,
                         arcade.color.DARK_GREEN, 16)

        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH // 2 - 200,
                SCREEN_WIDTH // 2 + 200,
                SCREEN_HEIGHT // 2 - 100,
                SCREEN_HEIGHT // 2 + 100,
                arcade.color.WHITE
            )
            arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
                             arcade.color.RED, 40, anchor_x="center", bold=True)
            arcade.draw_text(f"Лучший результат: {self.high_score}",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.BLACK, 24, anchor_x="center")
            arcade.draw_text(f"Финальный счет: {self.score}",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                             arcade.color.BLACK, 24, anchor_x="center")
            arcade.draw_text(f"Уровень: {self.level}",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
                             arcade.color.BLUE, 20, anchor_x="center")
            arcade.draw_text("Нажмите R для перезапуска",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90,
                             arcade.color.BLUE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if self.game_over and key == arcade.key.R:
            self.setup()
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_speed_x = -self.move_speed
            if self.player_facing_right and self.player_sprite:
                self.player_sprite.scale_x = -abs(self.player_sprite.scale_x)
                self.player_facing_right = False

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_speed_x = self.move_speed
            if not self.player_facing_right and self.player_sprite:
                self.player_sprite.scale_x = abs(self.player_sprite.scale_x)
                self.player_facing_right = True

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.LEFT, arcade.key.RIGHT,
                   arcade.key.A, arcade.key.D):
            self.player_speed_x = 0

    def update_camera(self):
        """Обновление позиции камеры"""
        target_camera_y = self.player_y - SCREEN_HEIGHT // 3

        if target_camera_y > self.camera_offset_y:
            self.camera_offset_y = target_camera_y
        elif self.player_y < self.camera_offset_y + SCREEN_HEIGHT // 3:
            self.camera_offset_y = max(0, self.camera_offset_y - 5)

        if self.camera_offset_y < 0:
            self.camera_offset_y = 0

    def on_update(self, delta_time):
        """Главный цикл обновления"""
        if self.game_over:
            return

        # Проверка перехода на уровень 2
        if self.level == 1 and self.score >= self.level_up_score:
            self.level = 2
            self.setup_level_params()  # Меняем только если перешли на уровень 2

        # Обновляем позицию спрайта
        if self.player_sprite:
            self.player_sprite.center_x = self.player_x
            self.player_sprite.center_y = self.player_y

        # Нижняя точка
        if self.player_sprite:
            player_bottom = self.player_y - self.player_sprite.height / 2
        else:
            player_bottom = self.player_y - 30

        # Движение
        self.player_x += self.player_speed_x

        # Телепортация
        if self.player_x < 0:
            self.player_x = SCREEN_WIDTH
        elif self.player_x > SCREEN_WIDTH:
            self.player_x = 0

        # Физика
        self.player_velocity_y -= self.gravity
        self.player_y += self.player_velocity_y

        # Счет
        if self.player_y > self.highest_y:
            height_gained = self.player_y - self.highest_y
            self.highest_y = self.player_y
            self.score += int(height_gained / 5)

        # Столкновения
        if self.player_velocity_y < 0:
            for platform in self.platforms:
                if (platform['left'] < self.player_x < platform['right'] and
                        platform['bottom'] < player_bottom < platform['top'] and
                        self.player_velocity_y < 0):
                    self.player_y = platform['top'] + (self.player_y - player_bottom)
                    self.player_velocity_y = self.jump_speed
                    self.score += 10
                    break

        # Конец игры
        if self.player_y < self.camera_offset_y - 100:
            self.load_high_score()
            self.save_high_score()
            self.game_over = True

        # Обновляем платформы и камеру
        self.update_platforms()
        self.update_camera()


def main():
    """Главная функция запуска игры"""
    window = DoodleJump()
    arcade.run()


if __name__ == "__main__":
    main()