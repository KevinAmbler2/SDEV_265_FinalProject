# Import statements
import tkinter as tk
from tkinter import ttk

#import PIL
#from PIL import ImageTk, Image

import random


# UNIVERSAL CONSTANTS
GAMEMODES = ["Classic","Fantasy"]

# Initial global values
continuationCheck = False
gamemode = "Classic"
sound = True
music = True
confirmationPrompt = True
activePlayerColor = 'red'


'''class BoardGeneration():
    # Generates an empty board based on the dimensions provided
    def generate(boardHeight, boardWidth):
        global boardTileArray
        boardTileArray = [[i] * boardWidth for i in range(boardHeight)]'''


class Window(tk.Toplevel):
    def __init__(self, parent, title, type):
        super().__init__(parent)

        self.geometry("300x100")
        self.title(title)

        if type != "exit" and type != "invalid" and type != "options" and type != "pauseMenu":
            self.protocol("WM_DELETE_WINDOW", root.close_confirm)


        if type == "mainMenu": # UNFINISHED
            self.geometry("300x200")
            tk.Button(self,
                       text="Play Game",
                       command=lambda: [root.open_window("Game Setup", "setup"), self.withdraw()]).pack(side=tk.TOP, pady=5)
            tk.Button(self,
                       text="Continue",
                       command=lambda: [changeContinueCheck(), root.open_window("Game Load", "setup"), self.withdraw()]).pack(pady=5)
            tk.Button(self,
                       text="Options",
                       command=lambda: [root.open_window("Options", "options"), self.withdraw()]).pack(pady=5)
            tk.Button(self,
                       text="Exit",
                       command=root.close_confirm).pack(side=tk.BOTTOM, pady=5)
            
            def changeContinueCheck():
                global continuationCheck
                continuationCheck = True


        elif type == "options":  # UNFINISHED
            tk.Button(self,
                       text="Save options",
                       command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.LEFT)  # UNFINISHED
            tk.Button(self,
                       text="Cancel",
                       command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.RIGHT)
        

        elif type == "pauseMenu": #UNFINISHED
            self.geometry("200x300")
            tk.Button(self,
                       text="Return",
                       command=lambda: [self.destroy()]).pack(side=tk.TOP, pady=5)
            # UNFINISHED SAVE AND LOAD FUNCTION
            tk.Button(self,
                       text="Save",
                       command=lambda: [self.destroy()]).pack(pady=5)
            tk.Button(self,
                       text="Load",
                       command=lambda: [changeContinueCheck(), root.open_window("Game Load", "setup"), self.destroy()]).pack(pady=5)
            tk.Label(self,text="Options").pack(pady=5)
            # UNFINISHED RADIO BUTTONS TO ENABLE SOUND/MUSIC/CONFIRMATION PROMPT
            tk.Button(self,
                       text="Main Menu",
                       command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.BOTTOM, pady=5)


        elif type == "setup": # UNFINISHED
            # This is kinda a stupid way to do things lol, but it works in theory
            # Save data needs to be saved in a way that allows program to differeniate sections of info
            '''if continuationCheck == True:
                savedPlayerCount = open("savedata.txt", "r")
                numPlayersEntry.insert(savedPlayerCount)
            else:
                numPlayersEntry.insert(0, "Enter the number of players, "+str(MIN_PLAYERS)+"-"+str(MAX_PLAYERS))
                tk.Button(self,
                        text="Continue",
                        command=lambda: addPlayers()).pack(side=tk.LEFT)  # UNFINISHED
                tk.Button(self,
                        text="Back",
                        command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.RIGHT) # Hide menu and destroy setup page'''
            
            global selectedGamemode
            selectedGamemode = tk.StringVar()
            selectedGamemode.set("Classic") # Set default gamemode
            tk.OptionMenu(self,selectedGamemode,*GAMEMODES).pack(side=tk.TOP) # Create dropdown menu for gamemode
            tk.Button(self,
                    text="Continue",
                    command=lambda: endSetup()).pack(side=tk.LEFT)
            tk.Button(self,
                    text="Back",
                    command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.RIGHT) # Unhide menu and destroy setup page
            
            # Signals setup is complete and generates board based on chosen settings
            def endSetup():
                root.open_window("Board", "board")
                createPlayerWindows()
                self.destroy()
            
            def createPlayerWindows(): # Creates the initial windows for players' personal sheets
                global curPlayer
                curPlayer = 1
                root.open_window("Player 1", "playerSheet")
                curPlayer = 2
                root.open_window("Player 2", "playerSheet")
        

        elif type == "playerSheet": # Formats the players' personal sheets
            self.geometry("200x400")
            # Formats player sheets based on indentity
            if curPlayer == 1:
                ttk.Label(self,text="Player Number 1").pack()
                self.configure(background="red")
            elif curPlayer == 2:
                ttk.Label(self,text="Player Number 2").pack()
                self.configure(background="blue")
            # Creates an obvious error if player count is misinterpretted
            else:
                ttk.Label(self,text="PLAYER SHEET ERROR").pack()
                self.configure(background="yellow")
            # HIDES ALL OTHER PLAYERS + BOARD IF NO OTHER ACTION TAKEN FIRST -> Locks up if no other windows available/open
            ttk.Button(self,
                       text="Close this window",
                       command=self.destroy).pack(side=tk.RIGHT)
            

        elif type == "board": # Creates the main board window, where most of the interaction takes place
            leftOffset = 1 # Number of columns to offset for GUI on left of board grid
            '''rightOffset = 1 # Number of columns to offset for GUI on right of board grid'''
            offsetSize = 150 # Size of offset cells for both sides

            # Generates an empty board array based on the dimensions provided
            # boardTileArray[y][x] format -> stored as yx  -> increments across
            def generate(boardWidth, boardHeight):
                #global boardTileArray
                global boardButtonArray
                #boardTileArray = [[int(str(y)+str(x)) for x in range(boardWidth)] for y in range(boardHeight)]
                boardButtonArray = [[tk.Button(self) for x in range(boardWidth)] for y in range(boardHeight)]
                #self.geometry(str((boardWidth*75)+((leftOffset+rightOffset)*offsetSize))+"x"+str((boardHeight*75)))
                self.geometry(str((boardWidth*75)+((leftOffset+1)*offsetSize))+"x"+str((boardHeight*75)))

            if selectedGamemode.get() == "Classic":
                generate(10,10)
            elif selectedGamemode.get() == "Fantasy":
                generate(8,10)
            
            # Section for left-side GUI widgets
            if leftOffset > 0:
                for i in range(leftOffset):
                    self.columnconfigure(i, weight= 2, minsize=offsetSize)

            tk.Button(self,text="Menu",command=lambda: [root.open_window("Pause Menu", "pauseMenu")]).grid(column=0,row=0,sticky=(tk.N,tk.W))
            
            tk.Label(self,text="Active Player:").grid(column=0,row=1)
            turnIndicator = tk.Label(self, bg=activePlayerColor)
            turnIndicator.grid(column=0,row=2,sticky=(tk.E,tk.W), padx=5)

            # Section for main board grid
            #for y in range(len(boardTileArray)): # Creates board grid and places button within each cell
            for y in range(len(boardButtonArray)):
                self.rowconfigure(y, weight= 1, minsize=75)
                #for x in range(len(boardTileArray[y])):
                for x in range(len(boardButtonArray[y])):
                    self.columnconfigure(x+leftOffset, weight= 1, minsize=75)
                    #tk.Button(self,text=str(boardTileArray[y][x])).grid(column=x+leftOffset,row=y,sticky=(tk.N,tk.S,tk.E,tk.W))
                    buttonEditor = boardButtonArray[y][x]
                    buttonEditor.configure(text=str(y)+str(x))
                    buttonEditor.grid(column=x+leftOffset,row=y,sticky=(tk.N,tk.S,tk.E,tk.W))

            # Section for right-side GUI widgets
            '''self.columnconfigure(leftOffset+len(boardTileArray[0]), weight= 2, minsize=offsetSize)
            RIGHTELEMENT1 = tk.Text(self,wrap='word')
            RIGHTELEMENT1.insert(1.0,"Here's where a GUI element will go.")
            RIGHTELEMENT1.grid(column=leftOffset+len(boardTileArray[0]),row=0,rowspan=1)
            RIGHTELEMENT1.configure(bg=self.cget('bg'),relief='flat',state='disabled')

            endTurnButton = tk.Button(self,text="End Turn",bg='yellow')
            endTurnButton.grid(column=leftOffset+len(boardTileArray[0]),row=9,rowspan=1)'''


        elif type == "exit":
            # If close is confirmed, calls close_all function
            # Save functionality -> UNDER DEVELOPMENT
            tk.Label(self,text="Are you sure you want to close?").pack()
            tk.Button(self,
                       text="Save and close all windows",
                       command=root.close_all).pack(side=tk.LEFT)
            # If close is not confirmed, closes confirmation window
            tk.Button(self,
                       text="Back",
                       command=self.destroy).pack(side=tk.RIGHT)


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()

    def close_all(self):  # Closes all windows, including hidden
        for child in self.winfo_children():
            child.destroy()
        self.destroy()

    def open_window(self, title, type):
        window = Window(self, title, type)
        window.resizable(False,False)
        if type == "exit" or type == "options" or type == "pauseMenu":  # If exit confirmation window, forces user interaction
            window.grab_set()

        return window

    def close_confirm(self):  # Creates confirmation window
        self.open_window("Confirm exit?", "exit")
    
    def load_save(saveName):
        saveFile = open(saveName, "r")
        for line in saveFile:
            if "playerCount" in line:
                global playerCount
                playerCount = line.strip("playerCount= ")
                continue
    
    # def hideNonActivePlayer(self, playerTurn):
    #    for child in self.winfo_children():
    #        if child.

    # def create_bg(window):  # Function to create banner on each window
    #     backing = Frame(window, padx=10, pady=10)
    #     backing.grid(column=0, row=0, sticky="N W E S")
    #     return backing


# Creates and hides the initial Tk() entity
if __name__ == "__main__":
    root = Root()

    mainMenu = root.open_window("Main Menu", "mainMenu")

    root.mainloop()
