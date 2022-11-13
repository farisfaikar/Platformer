import pygame
import src.codes.config as conf
from src.codes.tile import Tile
from src.codes.player import Player
from src.codes.enemy import Enemy
from src.codes.shooter import Shooter
from src.codes.bullet import Bullet
from src.codes.trap import Trap
from src.codes.particles import ParticleEffect


class Level:
    def __init__(self, screen, state):
        self.display_surface = screen
        self.level_num = state
        self.font = pygame.font.Font(conf.chary_font, 20)

        # level setup
        level_data = self.import_level()
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # player spawn pos
        self.spawn_pos = ()

        self.bullets = pygame.sprite.Group()
        self.static_time = 0
        self.triggered = False
        self.is_restart = False

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return 'exit'
        return ''

    def run(self):
        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # trap
        self.traps.update(self.world_shift)
        self.check_trap_collisions()
        self.traps.draw(self.display_surface)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # enemy
        self.enemies.update(self.world_shift)
        self.check_enemy_collisions()
        self.enemy_collision_reverse()
        self.enemies.draw(self.display_surface)

        # shooter
        self.shooters.update(self.world_shift)
        self.check_shooter_collisions()
        self.shooter_collision_reverse()
        self.shooters.draw(self.display_surface)

        # bullet
        self.fire_bullets()
        self.bullets.update(self.world_shift)
        self.bullets.draw(self.display_surface)

        # invisible
        self.invisibles.update(self.world_shift)

        # check death
        self.check_death()
        return True if self.is_restart else False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def import_level(self):
        path = f"src/levels/{self.level_num}.txt"
        with open(path) as file:
            data = file.readlines()
        f_data = []
        for _, line in enumerate(data):
            f_data.append(line.rstrip())
        return f_data

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.shooters = pygame.sprite.Group()
        self.invisibles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * conf.tile_size
                y = row_index * conf.tile_size

                if cell == 'X':
                    tile = Tile((x, y), conf.tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    self.spawn_pos = (x, y)
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)
                if cell == 'E':
                    enemy_sprite = Enemy((x, y), conf.tile_size)
                    self.enemies.add(enemy_sprite)
                if cell == 'S':
                    shooter_sprite = Shooter((x, y), conf.tile_size)
                    self.shooters.add(shooter_sprite)
                if cell == 'I':
                    invisible_sprite = Tile((x, y), conf.tile_size)
                    self.invisibles.add(invisible_sprite)
                if cell == 'T':
                    trap_sprite = Trap((x, y), conf.tile_size)
                    self.traps.add(trap_sprite)
                if cell == 'L':
                    # Place lava tile
                    pass
                if cell == 'F':
                    # trigger next level
                    pass

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < conf.screen_width / 2.25 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > conf.screen_width - (conf.screen_width / 2.25) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_enemy_collisions(self):
        player = self.player.sprite

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and player.direction.y >= 0:
                    player.direction.y = -15
                    enemy.kill()
                else:
                    self.is_restart = True

    def check_shooter_collisions(self):
        player = self.player.sprite

        for shooter in self.shooters.sprites():
            if shooter.rect.colliderect(player.rect):
                shooter_center = shooter.rect.centery
                shooter_top = shooter.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if shooter_top < player_bottom < shooter_center and player.direction.y >= 0:
                    player.direction.y = -15
                    shooter.kill()
                else:
                    self.is_restart = True

    def check_trap_collisions(self):
        player = self.player.sprite

        for trap in self.traps.sprites():
            if trap.rect.colliderect(player.rect):
                self.is_restart = True

    def check_death(self):
        if self.player.sprite.rect.top > conf.screen_height:
            self.is_restart = True

    def enemy_collision_reverse(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.invisibles, False):
                enemy.reverse()

    def shooter_collision_reverse(self):
        for shooter in self.shooters.sprites():
            if pygame.sprite.spritecollide(shooter, self.invisibles, False):
                shooter.reverse()

    def fire_bullets(self):
        curr_time = pygame.time.get_ticks() // 1000 % 3
        if curr_time == 1 and not self.triggered:
            for shooter in self.shooters.sprites():
                x = shooter.rect.x
                y = shooter.rect.y
                bullet_sprite = Bullet((x, y), conf.tile_size)
                self.bullets.add(bullet_sprite)
            self.triggered = True
        elif curr_time == 2:
            self.triggered = False
