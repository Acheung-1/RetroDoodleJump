"""
Main runner for the doodle jump game
Basically, we keep on drawing and moving objects in doodle jump 
in order to make them appear as they would in a normal game.
For example, when jumping, we are just moving everything else
around on the main canvas which is set in position.
"""

# Imports
import tkinter as tk
import time
from jumpObject import jumpObject
import random


def main():
    # Running the game loop
    game().mainloop()
    return

# Object which contains the whole game
class game(tk.Tk):
    def __init__(self):
        """
        Init file with default settings, starts the window
        """
        super().__init__()
        # Canvas size
        self.width, self.height = 400, 800
        
        # Level
        self.level = 1
        
        # Score
        self.curScore = 0
        self.curMaxScore = 0
        self.topScore = 0

        # Starting canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.menu_text('start')
        self.objectsToDelete = []

        # Player starting position
        self.halfSize = 10
        self.px = self.width//2
        self.py = self.height - 100 - self.halfSize

        # Jumping key values
        # Speed of jumping
        self.jumpSize = 20
        self.jumpHeight = self.halfSize
        self.fallHeight = -self.jumpHeight
        
        # Is movement happening?
        # Previous action
        self.prevActionJump = False
        # Did we just win?
        self.gotWin = False
            
        # Buttons
        self.canvas.bind('<Button-1>', self.start_game)
        self.canvas.bind_all('<Left>', self.moveSide)
        self.canvas.bind_all('<Right>', self.moveSide)
        self.canvas.bind_all('<space>', self.jump)
        self.canvas.bind_all('<Escape>', self.closeGame)
        self.canvas.bind_all('<r>', self.restart_game)
        
    def menu_text(self, RestartType: str):
        self.gameOn = False
        self.falling = False
        self.jumping = False
        try:
            self.canvas.delete(self.playerRect)
        except:
            pass
        self.canvas.delete('all')
        self.canvas.create_text(200,300, font=('freemono', 32, 'bold'),text='Retro Doodle Jump')
        if RestartType == 'start':
            self.canvas.create_text(200, 400, text='Click to start')
        elif RestartType == 'restart':
            self.canvas.create_text(200, 400, text=f'You lost on Level {self.level}')
            self.level = 1
        elif RestartType == 'win':
            self.canvas.create_text(200, 400, text=f'You beat Level {self.level}')
            if self.gotWin:
                self.gotWin = False
                self.updateLevel(1)
        self.canvas.create_text(200, 450, text=f'Click to play Level {self.level}')
        self.canvas.create_text(200, 550, text=f'Your score: {self.curMaxScore}')
        self.canvas.create_text(200, 600, text=f'Highscore: {self.topScore}')
        self.canvas.pack()
        return
    
    def start_game(self, event):
        """
        Starting the game actual game
        Putting a the player rectangle and platforms down
        """
        if self.gameOn == False:
            self.canvas.delete('all')
            self.createPlayerRectangle()
            self.create_platforms()
            self.gameOn = True
            self.reset_counters()
        return
        
    def restart_game(self, event):
        """
        Restart the game actual game
        Putting a the player rectangle and platforms down
        """
        self.canvas.delete('all')
        self.level = 1
        self.createPlayerRectangle()
        self.create_platforms()
        self.gameOn = True
        self.reset_counters()
        self.curScore = 0
        return

    def createPlayerRectangle(self):
        """
        Creates the player rectangle
        """
        self.playerRect = self.canvas.create_rectangle(self.px - self.halfSize,
            self.py - self.halfSize, self.px + self.halfSize, self.py + self.halfSize,
            fill='blue')
        return

    def moveSide(self, event):
        """
        Moving the player to the side based on the key we use
        """
        if not self.gameOn:
            return
        if not self.falling and not self.jumping:
            self.prevActionJump = False
        self.canvas.delete(self.playerRect)
        x = event.keysym
        if x == 'Left':
            if not self.checkLeftCollisions():
                self.px = max(self.px - self.halfSize, self.halfSize)
        elif x == 'Right':
            if not self.checkRightCollisions():
                self.px = min(self.px + self.halfSize, self.width - self.halfSize)
        self.createPlayerRectangle()
        self.gravityCheck()
        return

    def jump(self, event):
        """
        Processing the jumping action
        We basically make self.jumpSize many minijumps
        Between each minijump we have a short break to make it appear
        like one jump. It's laggy but that can be adjusted by adding more
        shorter jumps and shortening the sleep time
        At the end of a jump, we run gravityCheck
        """
        self.prevActionJump = True
        if not self.gameOn:
            return
        if self.jumping or self.falling:
            # We cannot jump if we are already in the air
            return
        self.jumping = True
        jumpCount = 0
        while self.jumping:
            # Moving all the objects
            self.moveEveryone(self.jumpHeight)
            jumpCount += 1
            # Checking if we made enough jumps or if there is a collision
            if jumpCount >= self.jumpSize or self.checkBottomCollisions():
                self.jumping = False
            self.timeStep()
        self.gravityCheck()
        return

    def gravityCheck(self):
        """
        Trying to mimic gravity
        Basically if the player is not on top of an object, they
        keep falling further down
        """
        if self.falling:
            return
        self.falling = True
        while not self.checkTopCollisions() and not self.jumping:
            self.timeStep()
            self.moveEveryone(self.fallHeight)
        self.timeStep()
        self.falling = False
        return

    def moveEveryone(self, y):
        """
        Function which moves everything around the player
        This way it creates the illusion that the player is going up when
        everything is going down
        """
        for j in self.objects:
            j.move(0, y)
        self.curScore += y * (1+ .2*(self.level - 1))
        return
        
        
    def randx(self):
        """
        Generates x coordinates based on level
        """
        # Initially, 16 coordinates on Level 1
        x = [0,50,100,150,200,250,300,350,0,50,100,150,200,250,300,350]
        
        # For every one level above Level 1, add 16 more x coordinates based on the width of the game screen (0 to 350 at 50 unit increments)
        curr = self.level
        while curr > 1:
            i = 1
            while i < 3:
                x = x + [0,50,100,150,200,250,300,350]
                i += 1
            curr -= 1
        return x
        
    def randy(self):
        """
        Generates y coordinates based on level
        """
        # Initially 16 coordinates on Level 1
        y = [0,50,100,150,200,250,300,350,400,450,500,550,600,-50,-100,-150]
        
        # For every one level above Level 1, add 16 more y coordinates that are higher and higher (Higher platforms have smaller y value). Need to find the current minimum in the y array to add more negative values (50 units apart)
        curr = self.level
        while curr > 1:
            miny = min(y)
            for i in range(1,17):
                y.append(miny+(-50)*i)
            curr -= 1
        
        return y

    def create_platforms(self):
        """
        Function to add starting platforms
        Get x and y coordinates using randx and randy, shuffle and pop out coordinates
        """
        self.objects=[]
        x = self.randx()
        y = self.randy()
        random.shuffle(x)
        random.shuffle(y)
        # Find lowest y value (highest platform)
        miny = min(y)
        
        for i in range(0,len(x)-1):
            # Pop out x and y coordinates after shuffling
            a = x.pop()
            b = y.pop()
            
            # Use random number to decide what type of platform will be made
            c = random.randint(0,10)
            # Normal platform (~64%) (skinny in height)
            if c > 3:
                self.objects.append(jumpObject(a,b,a+50,b+10, self.canvas, 'Platform','Brown'))
            # Power up (~9% chance) (small block)
            elif c == 3:
                self.objects.append(jumpObject(a,b,a+20,b+20, self.canvas, 'PowerUp'))
            # Enemy (~27%) (square block)
            else:
                self.objects.append(jumpObject(a,b,a+50,b+50, self.canvas, 'Enemy'))
        
        
        # Adding Floor (covers width of game screen)
        self.objects.append(jumpObject(0,self.height - 100,self.width, self.height, self.canvas, 'Floor', 'black','Yes'))
        # Second floor to prevent falling through when reseting
        self.objects.append(jumpObject(0,self.height - 50,self.width, self.height, self.canvas, 'Floor', 'black','Yes'))
        
        # Adding Goal (find highest y coordinate and make it 50 units higher)
        self.objects.append(jumpObject(150,miny-50,200, miny, self.canvas, 'Goal', 'Black','No'))
        return

    def getPlayerBbox(self):
        """
        Helper function for objects
        """
        return [self.px - self.halfSize, self.py - self.halfSize, self.px + self.halfSize, self.py + self.halfSize]


    # --------------------- Collisions -----------------------
    # The functions below check for collisions
    # Also checking if we collided with an enemy
    def checkTopCollisions(self):
        # Return true if there is a top collision
        for j in self.objects:
            if j.checkTopCollision(self.getPlayerBbox()):
                # If Enemy: if there is a collision on top of an enemy block, if this platform has not been touched before, increase score and update that it has been touched (This prevents touching the same block multiple times to get points). If the previous action was a jump, increase the number of times the block has been touched. If the platform has been touched twice, increase score and delete this platform.
                if j.isEnemy():
                    if j.notTouchPlat():
                        self.curScore += 100 * (1+ .2*(self.level - 1))
                        j.updatePlat()
                    if self.prevActionJump:
                        j.updateTimesTouch(1)
                    if j.timesTouched() == 2:
                        self.curScore += 150 * (1+ .2*(self.level - 1))
                        self.deleteObject(j)
                elif j.isPowerup():
                # If PowerUp: if there is a collision on top of a powerup, if this platform has not been touched before, increase score, increase jumpSize by 5, and update that it has been touched (This prevents touching the same block multiple times to get points).
                    if j.notTouchPlat():
                        self.curScore += 200 * (1+ .2*(self.level - 1))
                        self.jumpSize += 5
                        j.updatePlat()
                else:
                # If normal platform: if there is a collision on top of an enemy block, increase score and update that it has been touched (This prevents touching the same block multiple times to get points).
                    if j.notTouchPlat():
                        self.curScore += 50 * (1+ .2*(self.level - 1))
                        j.updatePlat()
                # If Goal: if there is a collision on top of a goal, update that it has been touched. If it has been touched, win the game.
                if j.isGoal():
                    j.updateTimesTouch(1)
                    if j.timesTouched() == 1:
                        self.winGame()
                return True
        return False

    # If colliding with an enemy from the bottom, end the game
    def checkBottomCollisions(self):
        for j in self.objects:
            if j.checkBottomCollision(self.getPlayerBbox()):
                if j.isEnemy():
                    self.endGame()
                return True
        return False
    
    # If colliding with an enemy from the left, end the game
    def checkLeftCollisions(self):
        for j in self.objects:
            if j.checkLeftCollision(self.getPlayerBbox()):
                if j.isEnemy():
                    self.endGame()
                return True
        return False
    
    # If colliding with an enemy from the right, end the game
    def checkRightCollisions(self):
        for j in self.objects:
            if j.checkRightCollision(self.getPlayerBbox()):
                if j.isEnemy():
                    self.endGame()
                return True
        return False

    def timeStep(self):
        """
        The time between each minijump (both up and down)
        If we are falling, they are faster than when jumping up
        """
        # Deleting the objects in the list of objects to delete
        if len(self.objectsToDelete)!=0:
            for j in self.objectsToDelete:
                try:
                    self.objects.remove(j)
                    j.delete()
                except:
                    pass
            self.objectsToDelete = []
        self.update()


        if self.falling:
            time.sleep(.02)
        elif self.jumping:
            time.sleep(.05)
        self.update()
        self.curMaxScore = max(self.curMaxScore, self.curScore)
        self.topScore = max(self.curScore, self.topScore)
        return

    # Game will end
    def endGame(self):
        self.menu_text('restart')
        return
    
    # Win the game
    def winGame(self):
        self.gotWin = True
        self.menu_text('win')
        return

    # Close game
    def closeGame(self, event):
        self.destroy()
        return

    # Append jumpObject to be deleted
    def deleteObject(self, obj: jumpObject):
        self.objectsToDelete.append(obj)
        self.gravityCheck()
        return
    
    # Update level by 1
    def updateLevel(self, add):
        self.level += add
        return

    # Resets jump size to default and curMaxScore to 0
    def reset_counters(self):
        self.jumpSize = 20
        self.curMaxScore = 0
        return

if __name__=='__main__':
    main()
