import pygame as pg

# Init and load sound effects
pg.mixer.init(44100, -16, 2, 4096)

control_menu = pg.mixer.Sound("sound_effects/control_menu.wav")
control_menu.set_volume(0.22)

select_menu = pg.mixer.Sound("sound_effects/select_menu.wav")
select_menu.set_volume(0.18)

start_game = pg.mixer.Sound("sound_effects/start_game.wav")
start_game.set_volume(0.3)

attack = pg.mixer.Sound("sound_effects/attack.wav")
attack.set_volume(0.08)

heal_sound = pg.mixer.Sound('sound_effects/heal_sound.wav')
heal_sound.set_volume(0.4)

slowdown_sound = pg.mixer.Sound('sound_effects/slowdown.wav')
slowdown_sound.set_volume(0.4)

slow_sound = pg.mixer.Sound('sound_effects/slow_sound.wav')
slow_sound.set_volume(0.4)

shield_sound = pg.mixer.Sound('sound_effects/shield_sound.wav')
shield_sound.set_volume(0.4)

ult_attack = pg.mixer.Sound("sound_effects/ult_attack.wav")
ult_attack.set_volume(0.08)

paused = pg.mixer.Sound("sound_effects/paused.wav")
paused.set_volume(0.1)

enemy_shoot_sound = pg.mixer.Sound('sound_effects/enemy_shot.wav')
enemy_shoot_sound.set_volume(0.15)

charge_shot = pg.mixer.Sound("sound_effects/charge_shot.wav")
charge_shot.set_volume(0.4)

stage_clear = pg.mixer.Sound("sound_effects/stage_clear.wav")
stage_clear.set_volume(0.7)

button_click_sound = pg.mixer.Sound('sound_effects/button_clicked.wav')

explosion_sound = pg.mixer.Sound('sound_effects/explosion.wav')
explosion_sound.set_volume(0.15)

enemy_explosion_sound = pg.mixer.Sound('sound_effects/enemy_explosion.wav')
enemy_explosion_sound.set_volume(0.4)

enemy_damaged_sound = pg.mixer.Sound('sound_effects/enemy_damaged.wav')
enemy_damaged_sound.set_volume(0.1)
