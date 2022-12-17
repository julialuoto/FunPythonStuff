# Julia Luoto
# CSCI 101 - D
# create project
# Time: 3 weeks
# resources:
# [1]“how to use pygame - Search Videos,” www.bing.com. https://www.bing.com/videos/search?q=how+to+use+pygame&view=
# detail&mid=6DF51A379427FC647C2D6DF51A379427FC647C2D&FORM=VIRE (accessed Dec. 03, 2022).
# [2]“Random Numbers in Python,” GeeksforGeeks, Aug. 01, 2016. https://www.geeksforgeeks.org/random-numbers-in-python/
# [3]“Making Games in Pygame: Asteroid Avoid - Part 2,” www.youtube.com. https://www.youtube.com/watch?v=_LBiSn7GB1s
# (accessed Nov. 20, 2022).
# [4]Flaticon, “Flaticon, the largest database of free vector icons,” Flaticon, 2013. https://www.flaticon.com/
# My old labs and assignments
# TA example from Graphics extra credit lecture

import pygame
import random
import time
import csv

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_BACKSPACE,
    K_RSHIFT
)

# initialize pygame
pygame.init()


# Player Object
class Player(pygame.sprite.Sprite):
    # creates the object player
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.image = pygame.image.load("space-ship.png")
        self.rect = self.surf.get_rect()
        self.rect.x = 50
        self.rect.y = 270
        self. health = 10
        self.speed = 4
        self.score = 0
        self.last_shot = pygame.time.get_ticks()
        self.name = ""
        self.ammo = 20
        self.reload = False
        self.wait = 0

    # handles player movement and shooting everytime it is called in the game loop
    def update(self, pressed_keys):
        time_now = pygame.time.get_ticks()
        cooldown = 300

        # shoots a laser when space is pressed
        if pressed_keys[K_SPACE] and time_now - self.last_shot > cooldown and self.ammo > 0:
            new_laser = Laser(self.rect.right, self.rect.centery + 5)
            lasers.add(new_laser)
            self.last_shot = time_now
            self.ammo -= 1

        # reloads ammo when shift is pressed and a few seconds has passed
        if pressed_keys[K_RSHIFT]:
            self.reload = True
        if self.reload:
            self.wait += 1
        if self.wait == 500:
            self.ammo = 20
            self.reload = False
            self.wait = 0

        # destroys the meteor and adds to score when laser hits the meteor
        if pygame.sprite.groupcollide(lasers, meteors, True, True):
            self.score += 1
            m = Meteor()
            meteors.add(m)

        # handles player movement
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # limits player movement to only on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 900:
            self.rect.right = 900
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600

    # sets the player name to the name given by the user
    def set_name(self, un):
        self.name = un


# Laser Object
class Laser(pygame.sprite.Sprite):
    # creates the object laser
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.image = pygame.image.load("laser.png")
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = 5

    # handles the movement of the laser
    def update(self):
        self.rect.move_ip(self.speed, 0)

        # kills the laser when it goes passed the screen
        if self.rect.left > 900:
            self.kill()

    # draws the laser to the screen
    def draw(self):
        screen.blit(self.image, self.rect)


# Meteor Object
class Meteor(pygame.sprite.Sprite):
    # creates the object meteor
    def __init__(self):
        super(Meteor, self).__init__()
        self.image = pygame.image.load("meteor.png")
        self.surf = pygame.Surface((60, 60))
        self.rect = self.surf.get_rect(center=(900 + random.randint(0, 500), random.randrange(20, 580)))

        # when players score is higher than 20 meteors will be moving faster on average
        if player.score >= 20:
            self.max_speed = 4
            self.min_speed = 2
        # at the beginning they will move slower
        else:
            self.max_speed = 3
            self.min_speed = 1.5

        self.speed = random.uniform(self.min_speed, self.max_speed)

    # handles the movement of the meteor
    def update(self, s):
        self.rect.move_ip(-self.speed, 0)

        # when the player has a score higher than 2p the meteors will be moveing faster
        if s >= 20:
            self.max_speed = 4
            self.min_speed = 2

        # when the meteor gets to the end of the screen it will reappear in the other side of the screen
        # and the player will lose health
        if self.rect.right < -50:
            self.rect.center = (900 + random.randint(0, 500), random.randrange(20, 580))
            self.speed = random.uniform(self.min_speed, self.max_speed)
            player.health -= 1

    # draws meteor to the screen
    def draw(self):
        screen.blit(self.image, self.rect)


# Scrolling background
class Background:
    # creates the object background
    def __init__(self):
        self.background = pygame.image.load("Space.png")
        self.rectBackground = self.background.get_rect()

        self.y1 = 0
        self.x1 = 0
        self.y2 = 0
        self.x2 = self.rectBackground.width

        self.speed = -0.6

    # makes the background move to the left
    def update(self):
        self.x1 += self.speed
        self.x2 += self.speed

        if self.x1 < -self.rectBackground.width:
            self.x1 = self.rectBackground.width
        if self.x2 < -self.rectBackground.width:
            self.x2 = self.rectBackground.width

    # draws two backgrounds so that it looks like a seamless scrolling
    def draw(self):
        screen.blit(self.background, (self.x1, self.y1))
        screen.blit(self.background, (self.x2, self.y2))


class Button:
    # creates an object button that takes in a lot of characteristics so that it is
    # easy to use in different places
    def __init__(self, text, width, height, pos, color, bcolor, font_size):
        self.pressed = False
        font1 = pygame.font.SysFont("Verdana", font_size)
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = bcolor
        self.text_surf = font1.render(text, True, color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    # draws the button on the screen
    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)

    # checks if the button is clicked and returns true or false
    def check_click(self):
        # gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        # recognizes if the mouse is hovered over a button
        if self.top_rect.collidepoint(mouse_pos):

            # if the mouse is clicked pressed is true
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True

            # returns true only after the mouse has been released so that the function doesn't spam true
            else:
                if self.pressed:
                    self.pressed = False
                    return True
                else:
                    return False


class Leaderboard:
    # creates the object leaderboard
    def __init__(self):
        super(Leaderboard, self).__init__()
        self.surf = pygame.Surface((60, 60))
        self.rect = self.surf.get_rect()
        self.file = "leaderboard.csv"
        self.list = self.read()

    # adds a person on to the leaderboard with a username and score
    def add(self, un, s):
        self.list.append([str(s), un])

    # writes everything in the leaderboard list into leaderboard.csv
    def write(self):
        f = open(self.file, "w")  # opens file

        # adds contents of the leaderboard list into the file with csv formatting
        for row in self.list:
            if self.list.index(row) == 0:
                f.writelines(f"{row[0]},{row[1]}")
            else:
                f.writelines(f"\n{row[0]},{row[1]}")

    # reads existing player data from the file
    def read(self):
        f = self.file
        unsorted_list = []

        # opens file as a csv file and reads it into a csv reader
        with open(f, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # takes in lines of the file and appends them into a list
            for row in csv_reader:
                s = row[0]
                un = row[1]
                unsorted_list.append([s, un])

        return unsorted_list

    # sorts the given list
    def sort(self, li):
        unsorted_list = li
        sorted_list = []

        # loops as long as there are items in the unsorted list
        while len(unsorted_list) > 0:
            high_score = 0
            high_scorer = ""

            # takes an item from the list and loops as long as there are items in the list
            for row in unsorted_list:
                s = int(row[0])
                un = row[1]

                # finds the highest score
                if s > high_score:
                    high_score = s
                    high_scorer = un

            # once highest score has been found it removes this item from the unserted list
            # and appends it into the sorted list
            unsorted_list.pop(unsorted_list.index([str(high_score), high_scorer]))
            sorted_list.append([str(high_score), high_scorer])

        return sorted_list

    # checks how many "NERD" players are in the leaderboard
    def get_nerds(self):
        nerds = 1
        for row in self.list:
            if row[1][0:4] == "NERD":
                nerds += 1
        return nerds

    # deletes duplicate names form the list and only leaves the one with a better score
    def del_duplicates(self):
        count = 0

        while len(self.list) > count:
            compare = self.list[count]  # gets a value from the leaderboard list

            # compares this value with every other value in the list
            for row in self.list:
                if count != self.list.index(row):

                    # if a matching name is found then we delete the lover scoring user
                    if row[1] == compare[1]:
                        if int(row[0]) > int(compare[0]):
                            self.list.pop(self.list.index(compare))
                        elif int(row[0]) <= int(compare[0]):
                            self.list.pop(self.list.index(row))
            count += 1

    # draws the top 15 from the leaderboard list on to the screen
    def draw(self):
        # sorts the list first and deletes duplicates
        self.list = self.sort(self.list)
        self.del_duplicates()

        # draws the titles to the screen
        f_s = pygame.font.SysFont("Verdana", 17)
        f_m = pygame.font.SysFont("Verdana", 25)

        header1 = f_m.render(f"LEADERBOARD:", True, (200, 100, 200))
        screen.blit(header1, (330, 20))
        header2 = f_m.render(f"NAME         SCORE", True, (200, 100, 200))
        screen.blit(header2, (330, 60))

        pos = 100
        count = 1

        # draws the top 15 users and their scores to the screen
        for row in self.list:
            if self.list.index(row) < 15:

                # prints the first name in different color
                if count == 1:
                    color = (100, 255, 100)
                else:
                    color = (200, 100, 200)

                # prints the rest of the names and scores
                n = f_s.render(f"{count}. {row[1]}", True, color)
                s = f_s.render(f"{row[0]}", True, color)
                screen.blit(n, (330, pos))
                screen.blit(s, (550, pos))
                pos += 30
                count += 1


# create screen
screen = pygame.display.set_mode((900, 600))

# init game objects
player = Player()

meteor1 = Meteor()
meteor2 = Meteor()
meteor3 = Meteor()

background = Background()

leaderboard = Leaderboard()

button1 = Button("START GAME", 320, 50, (300, 270), (20, 0, 20), (100, 50, 100), 40)
button2 = Button("LEADERBOARD", 320, 50, (300, 340), (20, 0, 20), (100, 50, 100), 40)
button3 = Button("Back", 80, 35, (200, 35), (20, 0, 20), (100, 50, 100), 20)

# create object groups
meteors = pygame.sprite.Group()
meteors.add(meteor1)
meteors.add(meteor2)
meteors.add(meteor3)

lasers = pygame.sprite.Group()

# text objects
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_input = pygame.font.SysFont("Verdana", 30)
font_medium = pygame.font.SysFont("Verdana", 40)

gameOver = font.render("Game Over", True, (255, 0, 0))

user_name = ""

# create pygame rects for scene 1
input_rect = pygame.Rect(300, 200, 320, 50)
anim_rect = pygame.Rect(0, 50, 50, 50)

# init scene
scene = 1

# game loop
running = True

while running:

    for event in pygame.event.get():
        # when the x is pressed
        if event.type == pygame.QUIT:
            leaderboard.del_duplicates()  # deletes dublicate names
            leaderboard.write()  # and prints leaderboard into the file leaderboard.csv
            running = False  # quits the program

        # when s=typing on the keyboard we get the username
        if event.type == pygame.KEYDOWN:
            if event.key == K_BACKSPACE:
                user_name = user_name[:-1]
            else:
                user_name += event.unicode

    if scene == 1:  # start scene
        # sets background
        screen.blit(background.background, (0, 0))

        # adds buttons
        button1.draw()
        button2.draw()
        if button1.check_click():
            scene = 2
        if button2.check_click():
            scene = 3

        # Username box
        pygame.draw.rect(screen, (20, 0, 20), input_rect)
        text_surface = font_input.render(user_name, True, (255, 255, 255))
        screen.blit(text_surface, input_rect)

        user_prompt = font_small.render("username:", True, (100, 50, 100))
        if user_name == "":
            screen.blit(user_prompt, input_rect)

        # creates a cute moving animation of the spaceship
        screen.blit(player.image, anim_rect)
        anim_rect.move_ip(2.5, 0)

        if anim_rect.left > 910:
            anim_rect.right = -20

    if scene == 2:  # Game scene

        # username
        user_name = user_name.replace(" ", "")  # removes spaces from username

        if user_name == "":  # if there is no username input then NERD is assigned to be the name
            player.set_name("NERD" + str(leaderboard.get_nerds()))
        else:  # else the username input is made the player name
            player.set_name(user_name)

        # background
        background.draw()
        background.update()

        # prints stats: health, score, and ammo on to the top of the screen
        health = font_small.render(f"Health: {player.health}", True, (255, 0, 0))
        screen.blit(health, (10, 10))

        score = font_small.render(f"score: {player.score}", True, (0, 255, 0))
        screen.blit(score, (200, 10))

        ammo = font_small.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo, (390, 10))

        # laser
        for laser in lasers:
            laser.update()
            laser.draw()

        # player movement
        screen.blit(player.image, player.rect)
        pressed = pygame.key.get_pressed()
        player.update(pressed)

        # meteors
        for meteor in meteors:
            meteor.update(player.score)
            meteor.draw()

        # adds more meteors when the player gets to score of 50
        if player.score >= 50 and len(meteors) < 4:
            meteor4 = Meteor()
            meteors.add(meteor4)
            player.health += 2

        # adds even more meteors when player gets to a score of 100
        if player.score >= 100 and 3 < len(meteors) < 5:
            meteor5 = Meteor()
            meteors.add(meteor5)
            player.health += 3

        # Game Over
        if pygame.sprite.spritecollideany(player, meteors) or player.health <= 0:
            screen.blit(gameOver, (100, 100))  # print game over

            # if the player got a score it is added to the leaderboard
            if player.score == 0:
                pass
            else:
                leaderboard.add(player.name, player.score)

            pygame.display.update()

            # reset game
            user_name = ""

            meteor1 = Meteor()
            meteor2 = Meteor()
            meteor3 = Meteor()

            meteors = pygame.sprite.Group()
            meteors.add(meteor1)
            meteors.add(meteor2)
            meteors.add(meteor3)

            player = Player()

            lasers = pygame.sprite.Group()

            time.sleep(5)

            scene = 1  # go back to start scene

    if scene == 3:  # leaderboard scene
        # draws leaderboard and background
        screen.blit(background.background, (0, 0))
        leaderboard.draw()

        # adds a button, so you can move back to start scene
        button3.draw()
        if button3.check_click():
            scene = 1

    # update the screen
    pygame.display.flip()



