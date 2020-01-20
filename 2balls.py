import pygame
import time
import random

# setup
pygame.init()

screen_width = 1280
screen_height = 720

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

class Ball(object):
	def __init__(self, vel, x, y, radius, x_vel):
		# direction starts off randomly
		self.x_vel = vel * x_vel
		self.x_start = x_vel
		self.y_vel = vel * random.choice((-1, 1))
		self.vel = vel
		self.x = x
		self.y = y
		self.radius = radius

	def bounce(self):
		pygame.mixer.music.load('bounce.wav')
		pygame.mixer.music.play(0)

	def dead(self):
		pygame.mixer.music.load('dead.wav')
		pygame.mixer.music.play(0)

	def run(self):
		# move the ball
		self.x += self.x_vel
		self.y += self.y_vel
		if self.x - self.radius < 0: 											# if hitting the left side
			global r_score
			r_score += 1
			self.dead()
			reset_balls()
		elif self.x + self.radius > screen_width: 								# if hitting the right side
			global l_score
			l_score += 1
			self.dead()
			reset_balls()

		if self.y - self.radius < 0 or self.y + self.radius > screen_height:								# when hitting the top or bottom
			self.y_vel *= -1
			self.bounce()

		if self.x + self.x_vel > lpaddle.x and self.x + self.x_vel  < lpaddle.x + lpaddle.width:			# hitting the left paddle
			if self.y + self.y_vel > lpaddle.y and self.y + self.y_vel < lpaddle.y + lpaddle.height:
				self.x_vel *= -1
				self.bounce()
				self.speed()

		if self.x + self.x_vel > rpaddle.x and self.x + self.x_vel  < rpaddle.x + rpaddle.width:			# hitting the right paddle
			if self.y + self.y_vel > rpaddle.y and self.y + self.y_vel < rpaddle.y + rpaddle.height:
				self.x_vel *= -1
				self.bounce()
				self.speed()

	def draw(self):
		pygame.draw.circle(win, (255, 255, 255), (round(self.x), round(self.y)), self.radius)

	def speed(self):
		if self.x_vel > 0:
			self.x_vel += random.random() # this is random just because there is 2 balls
		else:
			self.x_vel -= random.random()
		if self.y_vel > 0:
			self.y_vel += random.random()
		else:
			self.y_vel -= random.random()

class Paddle(object):
	def __init__(self, x, y, height, vel):
		self.height = height
		self.width = 20
		self.x = x
		self.y = y
		self.vel = vel

	def draw(self):
		pygame.draw.rect(win, (128, 128, 255), (self.x, self.y, self.width, self.height))

def text_objects(text, font):
	textSurface = font.render(text, True, (200, 200, 200))
	return textSurface, textSurface.get_rect()

def display_score(text):
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = (round(screen_width * 0.5), round(screen_height * 0.2))
	win.blit(TextSurf, TextRect)

def redrawGameWindow():
	win.fill((50, 50, 50))
	pygame.draw.rect(win, (128, 128, 255), (0, 0, screen_width, 5))
	pygame.draw.rect(win, (128, 128, 255), (0, screen_height - 5, screen_width, 5))
	pygame.draw.rect(win, (255, 0, 0), (0, 0, 5, screen_height))
	pygame.draw.rect(win, (255, 0, 0), (screen_width - 5, 0, 5, screen_height))
	ball1.draw()
	ball2.draw()
	lpaddle.draw()
	rpaddle.draw()
	display_score(f"{str(l_score)} : {str(r_score)}")
	pygame.display.update()


l_score = 0
r_score = 0

ball1 = Ball(5, round(screen_width*0.5), round(screen_height*0.5), screen_height//50, -1)
ball2 = Ball(5, round(screen_width*0.5), round(screen_height*0.5), screen_height//50, 1)
lpaddle = Paddle(round(screen_width*0.05), round(screen_height*0.25), round(screen_height*0.2), 10)
rpaddle = Paddle(round(screen_width*0.95), round(screen_height*0.25), round(screen_height*0.2), 10)


def reset_balls():
	time.sleep(1)
	ball1.x = round(screen_width*0.5)
	ball1.y = round(screen_height*0.5)
	ball1.x_vel = ball1.vel * ball1.x_start
	ball1.y_vel = ball1.vel * random.choice((-1, 1))
	ball2.x = round(screen_width*0.5)
	ball2.y = round(screen_height*0.5)
	ball2.x_vel = ball2.vel * ball2.x_start
	ball2.y_vel = ball2.vel * random.choice((-1, 1))


run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_q] and lpaddle.y - lpaddle.vel > 0:
		lpaddle.y -= lpaddle.vel
	if keys[pygame.K_a] and lpaddle.y + lpaddle.vel + lpaddle.height < screen_height:
		lpaddle.y += lpaddle.vel

	if keys[pygame.K_o] and rpaddle.y - rpaddle.vel > 0:
		rpaddle.y -= rpaddle.vel
	if keys[pygame.K_l] and rpaddle.y + rpaddle.vel + rpaddle.height < screen_height:
		rpaddle.y += rpaddle.vel

	ball1.run()
	ball2.run()


	redrawGameWindow()

pygame.quit()
