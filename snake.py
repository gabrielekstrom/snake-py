# snake-py - a simple terminal implementation of the classic snake game in Python.
# Copyright (c) 2023 Gabriel Ekström. All rights reserved.

import curses
import time
import random

class Game:
    def __init__(self) -> None:
        # VARNING - Om spelplanen är större än konsollen kraschar programmet och vi får ett error från curses.addstr()
        self.width = 10
        self.height = 10

        self.score = 0

        self.snake = Snake(self) # Skapa en ny instans av klassen Snake och skicka med en pointer till den aktuella klassen Game. Detta krävs eftersom Snake behöver komma åt Game:s lokala variabler.
        
        self.food = []
        self.place_food()

    # Funktion för att printa spelplanen och övrig information till konsollen
    def print(self, screen):
        screen.clear() # Rensa konsollen

        screen.addstr(0, 0, f"Current score: {self.score}")

        offset = 1

        # Loopa genom alla rader och kolumner i spelplanen
        for y in range(self.height):
            row = ""
            for x in range(self.width):

                if [x, y] in self.snake.body:
                    row += " s "
                elif [x, y] == self.snake.head:
                    row += " # "
                elif [x, y] == self.food:
                    row += " % "
                else:
                    row += " . "

            screen.addstr(y+offset, 0, row)
        
        screen.refresh()

    # Placera ut en matbit på en slumpmässig position på spelplanen
    def place_food(self):
            x = random.randrange(0, self.width-1)
            y = random.randrange(0, self.height-1)

            self.food = [x, y]

            # Kontrollera om maten hamnade under ormen
            if self.food == self.snake.head or self.food in self.snake.body:
                # Kör funktionen igen
                self.place_food()
    
    # Kontrollerar om den givna koordinaten ligger på spelplanen
    def is_outside_map(self, coordinate):
        if coordinate[0] > self.width-1:
            return True
        
        elif coordinate[0] < 0:
            return True
        
        elif coordinate[1] > self.height-1:
            return True
        
        elif coordinate[1] < 0:
            return True
        
        else:
            return False

class Snake:
    def __init__(self, game) -> None:
        self.body = [[1, 1], [2, 1], [3, 1]] # Sätt ormens kropps startposition
        self.head = [4, 1] # Sätt ormens huvuds startposition
        self.direction = "r"
        self.isAlive = True

        self.game = game # Spara en lokal pointer till Game så att vi kommer åt dess lokala variabler

    def set_direction(self, newDirection):
        # Kontrollera om den nya riktningen är ogiltig, alltså om den hade krockat med den nuvarande riktningen
        if newDirection == "u" and self.direction == "d":
            return
        elif newDirection == "d" and self.direction == "u":
            return
        elif newDirection == "l" and self.direction == "r":
            return
        elif newDirection == "r" and self.direction == "l":
            return
        else:
            self.direction = newDirection

    def move(self):
        # Lägg till huvudets gamla position i kroppens lista
        self.body.append([self.head[0], self.head[1]]) # OBS - om vi inte refererar till det exakta värdet så skapar Python i stället en "pointer" till self.head vilket skapar problem när vi vill lägga huvudets gamla koordinat i den nya kroppens lista.

        # Kontrollera om ormens huvud är på matens position
        if self.head == self.game.food:
            hasEaten = True
        else:
            hasEaten = False

        # Beräkna huvudets nya koordinater
        match self.direction:
            case "u": # Upp
                self.head[0] = self.head[0]
                self.head[1] = self.head[1] - 1
            case "d": # Ner
                self.head[0] = self.head[0]
                self.head[1] = self.head[1] + 1
            case "l": # Vänster
                self.head[0] = self.head[0] - 1
                self.head[1] = self.head[1]
            case "r": # Höger
                self.head[0] = self.head[0] + 1
                self.head[1] = self.head[1]

        if hasEaten:
            # Ormen har ätit och vi behöver generera en ny matbit
            self.game.place_food()
            # Öka poängen
            self.game.score += 1
        else:
            # Om ormen inte ätit ska vi ta bort första koordinaten i listan (svansen) så att ormen inte växer
            self.body.pop(0)

        # Kolla om ormens huvud ligger i listan med kroppens koordinater. Detta innebär i sådana fall att huvudet krockat med kroppen.
        if self.head in self.body:
            self.isAlive = False

        # Kolla om ormens huvud ligger utanför spelplanen
        if self.game.is_outside_map(self.head):
            self.isAlive = False

def main(screen):
    game = Game()

    screen.timeout(0) # Stäng av delay vid inhämtandet av knappytryckningar
    curses.curs_set(0) # Göm textmarkören i konsollen
    
    # Huvudspelloop
    while True:
        # Spara den senaste knapptryckningen
        key = screen.getch()
        # Kolla så att det faktiskt trycktes ner en knapp (https://docs.python.org/3/library/curses.html#curses.window.getch)
        if key != -1:
            # Konvertera knapptryckningen till en giltig riktning
            if key == curses.KEY_UP or key == ord("w"):
                direction = "u"
                game.snake.set_direction(direction)
            elif key == curses.KEY_DOWN or key == ord("s"):
                direction = "d"
                game.snake.set_direction(direction)
            elif key == curses.KEY_LEFT or key == ord("a"):
                direction = "l"
                game.snake.set_direction(direction)
            elif key == curses.KEY_RIGHT or key == ord("d"):
                direction = "r"
                game.snake.set_direction(direction)

        # Flytta ormen
        game.snake.move()

        # Kolla om spelet är över
        if game.snake.isAlive == False:
            break

        # Visa spelplanen
        game.print(screen)

        time.sleep(.6) # Bestämmer spelets hastighet

    # Skriv ut game over och vänta, stäng sedan programmet
    screen.clear()
    screen.addstr(0, 0, "Game over!")
    screen.addstr(1, 0, f"Your score was: {game.score}")
    screen.refresh()
    time.sleep(5)

curses.wrapper(main)