import pygame
pygame.init()

form_width = 600
form_height = 600
form = pygame.display.set_mode((form_width, form_height))
brick_img = pygame.image.load('brick.png').convert_alpha()
enemy_img = pygame.image.load('enemi.png').convert_alpha()

level = ['---------------',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '-             -',
		 '---------------'
		 ]

class Player():
	def __init__(self, form, x, y):
		self.form = form
		self.img = [ pygame.image.load('1.png').convert_alpha(),
					 pygame.image.load('1_d.png').convert_alpha(),
					 pygame.image.load('1_l.png').convert_alpha(),
					 pygame.image.load('1_r.png').convert_alpha()
					 ]
		self.hitbox = self.img[0].get_rect()
		self.x = x
		self.y = y
		self.speed = 1
		# Сторона: 0 - вверх, 1 - вниз, 3 - влево, 4 вправо
		self.side = 0

	def draw(self):
		self.form.blit(self.img[self.side], (self.hitbox.center))

	def control(self, up, down, left, right):
		if up:
			self.hitbox.y -= self.speed
			self.side = 0
		elif down:
			self.hitbox.y += self.speed
			self.side = 1
		elif left:
			self.hitbox.x -= self.speed
			self.side = 2
		elif right:
			self.hitbox.x += self.speed
			self.side = 3


class Wall():
	# Класс блока
	def __init__(self, form, x, y, width, height, type):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.form = form
		if type == '-':
			self.img = pygame.image.load('brick.png').convert_alpha()
		self.hitbox = pygame.Rect((x, y, width, height))

	def draw(self):
		self.form.blit(self.img, (self.hitbox.x, self.hitbox.y))


class Bullet():
	# Класс пули
	def __init__(self, form, x, y, side):
		self.form = form
		self.img = [ pygame.image.load('bullet_up.png').convert_alpha(),
					 pygame.image.load('bullet_down.png').convert_alpha(),
					 pygame.image.load('bullet_left.png').convert_alpha(),
					 pygame.image.load('bullet_right.png').convert_alpha()
					 ]
		self.hitbox = self.img[0].get_rect()
		self.x = x
		self.y = y
		self.speed = 1
		self.side = side

	def move(self):
		# Прорисовка и передвижение пули
		# Сторона (side): 0 - вверх, 1 - вниз, 3 - влево, 4 вправо
		if self.side == 0:
			self.hitbox.y -= self.speed
		if self.side == 1:
			self.hitbox.y += self.speed
		if self.side == 2:
			self.hitbox.x -= self.speed
		if self.side == 3:
			self.hitbox.x += self.speed

		self.form.blit(self.img[self.side], (self.hitbox.center))


def level_generation():
	# Генерация уровня
	global brick_img, form, bloks
	x = 0
	y = 0
	# Перебираем строчку
	for row in level:
		# Перебираем символы в строчке
		for col in row:
			# Если символ '-' то создаем блок и добавляем в список
			if col == '-':
				form.blit(brick_img, (x, y))
				bloks.append(Wall(form, x, y, 40, 40, '-'))
			x += 40
		x = 0
		y += 40

def level_draw():
	# Отрисовка уровня
	global bloks
	# Перебираем все блоки по одному и отрисовываем их
	for blok in bloks:
		blok.draw()

# Создание игрока
hero = Player(form, 80, 80)
# Первоначальные настройки
up, down, left, right, bullet_start = False, False, False, False, False
# Список пуль
bullets = []
# Список блоков
bloks = []

# Генерация уорвня
level_generation()
play = True
while play:
	form.fill((0, 0, 0))
	# Отрисовка блоков
	level_draw()
	# Управление игроком
	hero.control(up, down, left, right)
	# Отрисовка игрока
	hero.draw()
	form.blit(enemy_img,(300,300))


	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			play = False

		if i.type == pygame.KEYDOWN:
			if i.key == pygame.K_UP:
				up = True
			if i.key == pygame.K_DOWN:
				down = True
			if i.key == pygame.K_LEFT:
				left = True
			if i.key == pygame.K_RIGHT:
				right = True
			if i.key == pygame.K_SPACE:
				bullets.append(Bullet(form, hero.hitbox.center[0], hero.hitbox.center[1], hero.side))


		if i.type == pygame.KEYUP:
			if i.key == pygame.K_UP:
				up = False
			if i.key == pygame.K_DOWN:
				down = False
			if i.key == pygame.K_LEFT:
				left = False
			if i.key == pygame.K_RIGHT:
				right = False


	for bullet in bullets:
		bullet.move()

	pygame.display.update()
	pygame.time.delay(5)
