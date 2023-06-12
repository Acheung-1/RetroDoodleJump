import tkinter as tk
import time

class jumpObject():
    """
    Class of non-player objects such as platforms, floors and enemies
    """
    def __init__(self, x1, y1, x2, y2, canvas: tk.Canvas, colType, color=None, 
            touch: bool=False,timesTouch = 0):
        """
        Initializing the object
        Id is set by the tkinter canvas
        colType is the type of the object
        """
        self.canvas = canvas
        
        # x1 = left. x2 = right. y1 = top. y2 = bottom.
        self.x1, self.x2, self.y1, self.y2= x1, x2, y1, y2
        
        # Default is false, platform has not been touched yet
        self.touch = touch
        
        # Number of times platform has been touched
        self.timesTouch = timesTouch
       
        # Collision type
        self.colType = colType
        
        # Color of enemy and powerup
        if colType == 'Enemy':
            color = 'red'
        if colType == 'PowerUp':
            color = 'Green'
        
        # Creating the rectangle
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        return

    # Moving the rectanglar box
    def move(self, x,y):
        """
        Function to move an object in an x,y direction
        Used mainly to help with jumping
        """
        self.canvas.move(self.id, x,y)
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y
        return

    # Returns true if we collide with the player in bbox
    # I.E. player is on top of the bbox
    def checkTopCollision(self, playerBbox):
        self.time = time.time()
        return ( (playerBbox[3] == self.y1) and (playerBbox[0] < self.x2) and (playerBbox[2] > self.x1))

    # Returns true if we collide with the player in bbox
    # I.E. player is on top of the bbox
    def checkBottomCollision(self, playerBbox):
        return ( (playerBbox[1] == self.y2) and (playerBbox[0] < self.x2) and (playerBbox[2] > self.x1))

    # Returns whether we are colliding on left side
    def checkLeftCollision(self, playerBbox):
        return (playerBbox[0] == self.x2) and (playerBbox[1] < self.y2) and (playerBbox[3] > self.y1)

    # Returns whether we are colliding on right side
    def checkRightCollision(self, playerBbox):
        return (playerBbox[2] == self.x1) and (playerBbox[1] < self.y2) and (playerBbox[3] > self.y1)

    # True if platform is an enemy
    def isEnemy(self):
        return self.colType == 'Enemy'
    
    # True if platfrom is a powerup
    def isPowerup(self):
        return self.colType == 'PowerUp'
    
    # True if platform is Goal
    def isGoal(self):
        return self.colType == 'Goal'

    # True if platform has not been touched
    def notTouchPlat(self):
        return not self.touch

    # Update that platform has been touched
    def updatePlat(self):
        self.touch = True
        return
    
    # Add number of times platform has been touched
    def updateTimesTouch(self, add):
        self.timesTouch += add
        return

    # Delete from canvas
    def delete(self):
        self.canvas.delete(self.id)
        return

    # Return how many times platform has been touched
    def timesTouched(self):
        return self.timesTouch
