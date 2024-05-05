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
activePlayer = 'red'
arrayDict = {}
selectedButton = None
lastBG = None


class Window(tk.Toplevel):
    def __init__(self, parent, title, type):
        super().__init__(parent)

        self.geometry("300x100")
        self.title(title)
        
        class BoardFunctionality():
            # Changes ownership of active player status
            def endTurn(player):
                global activePlayer
                if player == "red":
                    activePlayer = "blue"
                else:
                    activePlayer = "red"
                turnIndicator.configure(bg=activePlayer)

            # Highlights selected cell in gold on click
            def highlightSelection(button):
                global selectedButton, lastBG
                if selectedButton is not None:
                    selectedButton.config(bg=lastBG)
                lastBG = button.cget("bg")
                selectedButton = button
                button.config(bg="gold")

        # ??MERGE GENERATE + POPULATE??

        # Generates an empty board array based on the dimensions provided
        # arrayDict['tileArrayB'][y][x] format -> stored as yx  -> increments across
        def generate(arrayWidth, arrayHeight, useCase):
            global arrayDict
            if useCase == "board":
                arrayDict['tileArrayB'] = [[tk.Button(self,relief="groove",activebackground="gold") for x in range(arrayHeight)] for y in range(arrayWidth)] # Creates clickable tiles for the user
                arrayDict['tileStateArrayB'] = [["Empty" for x in range(arrayHeight)] for y in range(arrayWidth)] # Stores data on cells in background
                #self.geometry(str((arrayHeight*75)+((leftOffset+1)*offsetSize))+"x"+str((arrayWidth*75))) # Sets size of board window based on gamemode
            elif useCase == "playerSheet":
                # Creates clickable tiles for the user
                arrayDict['tileArrayP%1d'%curPlayer] = [[tk.Button(self,relief="groove",activebackground="gold") for x in range(arrayHeight)] for y in range(arrayWidth)]
                # Stores data on cells in background
                arrayDict['tileStateArrayP%1d'%curPlayer] = [["Empty" for x in range(arrayHeight)] for y in range(arrayWidth)]
        
        # Fills generated arrays with buttons
        def populateInitialArrayButtons(tileArray, tileStateArray, leftOffset, offsetSize): # leftOffset - Number of columns to offset for GUI on left of board grid
            # Section for left-side GUI widgets
            if leftOffset > 0:
                for i in range(leftOffset):
                    self.columnconfigure(i, weight= 2, minsize=offsetSize)

            for y in range(len(arrayDict[tileArray])): # Creates array grid and places button within each cell
                self.rowconfigure(y, weight= 1, minsize=50)
                for x in range(len(arrayDict[tileArray][y])):
                    self.columnconfigure(x+leftOffset, weight= 1, minsize=50)

                    # Call sub-dictionaries (children of arrayDict) of button variable names and configure appropriately, each initial assigned as '[row-number][col-number]'
                    arrayDict[tileArray][y][x].configure(text=str(y)+str(x),command=lambda button=arrayDict[tileArray][y][x]: BoardFunctionality.highlightSelection(button))

                    if tileArray.strip("tileArray") == "B": # Checks if main board is being generated
                        self.rowconfigure(y, weight= 1, minsize=75)
                        self.columnconfigure(x+leftOffset, weight= 1, minsize=75)
                        # Sets up impassible tiles in middle of board based on gamemode
                        if selectedGamemode.get() == "Classic":
                            j,k = 4,5
                            self.geometry(str(750+((leftOffset+1)*offsetSize))+"x750") # Sets size of board window based on gamemode
                        else:
                            j,k = 3,4
                            self.geometry(str(750+((leftOffset+1)*offsetSize))+"x600") # Sets size of board window based on gamemode
                        if (y==j or y==k) and (x==2 or x==3 or x==6 or x==7):
                            arrayDict[tileStateArray][y][x] = "Impassible"
                            arrayDict[tileArray][y][x].configure(text="X",bg="#13f3ee") # Temporary indicator
                        
                        # Section for right-side GUI widgets on main board
                        self.columnconfigure(leftOffset+len(arrayDict[tileArray][0]), weight= 2, minsize=offsetSize)
                        RIGHTELEMENT1 = tk.Text(self,wrap='word')
                        RIGHTELEMENT1.insert(1.0,"Here's where a GUI element will go.")
                        RIGHTELEMENT1.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=0,rowspan=1)
                        RIGHTELEMENT1.configure(bg=self.cget('bg'),relief='flat',state='disabled')

                        endTurnButton = tk.Button(self,text="End Turn",bg='yellow',command=lambda:[BoardFunctionality.endTurn(activePlayer)])
                        endTurnButton.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=len(arrayDict[tileArray])-1,rowspan=1)
                    
                    arrayDict[tileArray][y][x].grid(column=x+leftOffset,row=y,sticky=(tk.N,tk.S,tk.E,tk.W))

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
            self.geometry("200x750")
            # Creates button array for units
            generate(12,1,"playerSheet")
            # Formats player sheets based on indentity
            if curPlayer == 1:
                ttk.Label(self,text="Player Number 1").grid(row=0,column=1)
                self.configure(background="red")
                populateInitialArrayButtons('tileArrayP1', 'tileStateArrayP1',0,0)
            elif curPlayer == 2:
                ttk.Label(self,text='Player Number 2').grid(row=0,column=1)
                self.configure(background="blue")
                populateInitialArrayButtons('tileArrayP2', 'tileStateArrayP2',0,0)
            # Creates an obvious error if player count is misinterpretted
            else:
                ttk.Label(self,text="PLAYER SHEET ERROR").grid(row=0,column=0)
                self.configure(background="yellow")
            # HIDES ALL OTHER PLAYERS + BOARD IF NO OTHER ACTION TAKEN FIRST -> Locks up if no other windows available/open
            ttk.Button(self,
                       text="Close this window",
                       command=self.destroy).grid(row=2,column=1)
            

        elif type == "board": # Creates the main board window, where most of the interaction takes place
            global arrayDict

            if selectedGamemode.get() == "Classic":
                generate(10,10,"board")
            elif selectedGamemode.get() == "Fantasy":
                generate(8,10,"board")

            pauseButton = tk.Button(self,text="Menu",command=lambda: [root.open_window("Pause Menu", "pauseMenu")])
            pauseButton.grid(column=0,row=0,sticky=(tk.N,tk.W))
            
            tk.Label(self,text="Active Player:").grid(column=0,row=1)
            turnIndicator = tk.Label(self, bg=activePlayer)
            turnIndicator.grid(column=0,row=2,sticky=(tk.E,tk.W), padx=5)

            populateInitialArrayButtons("tileArrayB","tileStateArrayB",1,150)


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
