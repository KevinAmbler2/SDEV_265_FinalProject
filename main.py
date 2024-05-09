# Import statements
import tkinter as tk # Import tkinter modules to workspace
from tkinter import ttk, messagebox

#import PIL
#from PIL import ImageTk, Image

import random


# UNIVERSAL CONSTANTS
GAMEMODES = ["Classic","Fantasy"] # Available gamemode variations
UNIT_STRENGTH = ['1','9','8','7','6','5','4','3','2','S','F','T'] # Array holding all unit strengths (used to create player sheet rosters)
# Dictionary holding the names, strength, and quantity of units for the "Classic" gamemode variation in the format strength:[unitName,quantity]
CLASSIC_ROSTER = {'1':["Marshal",1],'9':["General",1],'8':["Colonel",2],'7':["Major",3],'6':["Captain",4],
                  '5':["Lieutenant",4],'4':["Sergeant",4],'3':["Miner",5],'2':["Scout",8],'S':["Spy",1],'F':["Flag",1],'T':["Bomb",6]}
# Dictionary holding the names, strength, and quantity of units for the "Classic" gamemode variation in the format strength:[unitName,quantity]
FANTASY_ROSTER = {'1':["Dragon",1],'9':["Mage",1],'8':["Knight",2],'7':["Beast Rider",3],'6':["Sorceress",2],
                  '5':["Elemental",2],'4':["Elf",2],'3':["Dwarf",5],'2':["Scout",4],'S':["Slayer",1],'F':["Flag",1],'T':["Trap",6]}
#print(CLASSIC_ROSTER)
#print("\n\n\n")
#print(FANTASY_ROSTER)

# Initial global values
continuationCheck = False # Checks if system should be starting a new game (False) or loading existing game (True)
sound = True # Enables(True)/disables(False) game sound (default = True)
music = True # Enables(True)/disables(False) background music (default = True)
confirmationPrompt = True # Enables(True)/disables(False) pop-up prompt after making a valid move (default = True)
activePlayer = 'R' # Tracks the current active player for display and piece control (default = 'R')
arrayDict = {} # Stores button and backend data sub-dictionaries for main board and both player sheets
selectedButton = None # Indicates which button the user has clicked on (excluding GUI/navigational buttons)
lastBG = None # Stores the previous background color of the selected button
tileContent = "" # Stores the backend data of what was positioned on the tile selected by the user
deploymentComplete = [] # Stores the identity of players that have confirmed their deployment
oldX, oldY = 0, 0 # Tracks the coordinates of the "source" tile when determining movement
unitAbility = "None" # Tracks which unit ability is in use to determine legal movement tiles


class Window(tk.Toplevel):
    def __init__(self, parent, title, type):
        super().__init__(parent)

        self.title(title)
        
        class BoardFunctionality():
            # Changes ownership of active player status
            def end_turn(player):
                global activePlayer
                if player == 'R':
                    activePlayer = 'B'
                    turnIndicator.configure(bg="blue")
                    if len(deploymentComplete) != 2:
                        for child in root.winfo_children():
                            if child.winfo_name() == "!window4":
                                child.wm_attributes('-disabled',True)
                                child.withdraw()
                            elif child.winfo_name() != "!window":
                                child.wm_attributes('-disabled',False)
                                child.deiconify()
                else:
                    activePlayer = 'R'
                    turnIndicator.configure(bg="red")
                    if len(deploymentComplete) != 2:
                        for child in root.winfo_children():
                            if child.winfo_name() == "!window5":
                                child.wm_attributes('-disabled',True)
                                child.withdraw()
                            elif child.winfo_name() != "!window":
                                child.wm_attributes('-disabled',False)
                                child.deiconify()
                if (len(deploymentComplete) == 0 or len(deploymentComplete) == 2):
                    Root.open_window(self,"Change Player", "blocker")
                    BoardFunctionality.change_visibility('tileArrayM','tileStateArrayM')

                if activePlayer in deploymentComplete and len(deploymentComplete) != 2: # If only one player has finished deployment, skip finished player's deployment step
                    BoardFunctionality.end_turn(activePlayer)
                
                BoardFunctionality.update_deployment_restrictions('tileArrayM')

                if len(deploymentComplete) == 2:
                    for child in root.winfo_children():
                        if child.winfo_name() == "!window4":
                            child.destroy()
                        elif child.winfo_name() == "!window5":
                            child.destroy()
            
            def resolve_combat(attacker,defender):
                if selectedGamemode.get() == "Classic": # Checks gamemode for correct name list
                    atkPiece = CLASSIC_ROSTER[attacker[1]][0] # Gets name of attacking piece
                    defPiece = CLASSIC_ROSTER[defender[1]][0] # Gets name of defending piece
                    # Checks if slayer/spy is attacking
                    try:
                        atkStrength = int(attacker[1])
                    except: # Slayer/spy is attacking piece
                        if defender[1] == '1': # If the defender is the dragon/marshal
                            atkStrength = 11
                            print("Marshal Assassinated")
                        else: # All other defenders
                            atkStrength = 0
                    if atkStrength == 1: # Corrects dragon/marshal strength
                        atkStrength = 10

                    # Checks if slayer/spy, trap/bomb, or flag is defending
                    try:
                        defStrength = int(defender[1])
                    except:
                        if defender[1] == 'F': # Flag is defender
                            defStrength = -1
                            print("Flag Captured")
                        elif defender[1] == 'T' and atkStrength == 3: # Trap/bomb is defender and attacker can difuse
                            defStrength = 0
                            print("Bomb Captured")
                        elif defender[1] == 'T': # Trap/bomb is defender and attacker cannot difuse
                            defStrength = 11
                            print("Bomb Triggered")
                        else: # Slayer/spy is defender
                            defStrength = 0
                    if defStrength == 1: # Corrects dragon/marshal strength
                        defStrength = 10


                    if activePlayer == 'R':
                        if atkStrength > defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While attacking, Red's %s captured Blue's %s." % (atkPiece,defPiece))
                            if attacker[-1:] == "*": return attacker
                            else: return attacker+"*"
                        elif atkStrength < defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While defending, Blue's %s captured Red's %s." % (defPiece,atkPiece))
                            if defender[-1:] == "*": return defender
                            else: return defender+"*"
                        else:
                            messagebox.showinfo(title="Attack Summary",message="In combat, both Red's %s and Blue's %s were captured." % (atkPiece,defPiece))
                            return "Empty"
                    else:
                        if atkStrength > defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While attacking, Blue's %s captured Red's %s." % (atkPiece,defPiece))
                            if attacker[-1:] == "*": return attacker
                            else: return attacker+"*"
                        elif atkStrength < defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While defending, Red's %s captured Blue's %s." % (defPiece,atkPiece))
                            if defender[-1:] == "*": return defender
                            else: return defender+"*"
                        else:
                            messagebox.showinfo(title="Attack Summary",message="In combat, both Blue's %s and Red's %s were captured." % (atkPiece,defPiece))
                            return "Empty"
                else:
                    atkPiece = FANTASY_ROSTER[attacker[1]][0]
                    defPiece = FANTASY_ROSTER[defender[1]][0]
                    # Checks if slayer/spy is attacking
                    try:
                        atkStrength = int(attacker[1])
                    except: # Slayer/spy is attacking piece
                        if defender[1] == '1': # If the defender is the dragon/marshal
                            atkStrength = 11
                            print("Dragon Slayed")
                        else: # All other defenders
                            atkStrength = 0
                    if atkStrength == 1: # Corrects dragon/marshal strength
                        atkStrength = 10

                    # Checks if slayer/spy, trap/bomb, or flag is defending
                    try:
                        defStrength = int(defender[1])
                    except:
                        if defender[1] == 'F': # Flag is defender
                            defStrength = -1
                            print("Flag Captured")
                        elif defender[1] == 'T' and atkStrength == 3: # Trap/bomb is defender and attacker can difuse
                            defStrength = 0
                            print("Trap Captured")
                        elif defender[1] == 'T': # Trap/bomb is defender and attacker cannot difuse
                            defStrength = 11
                            print("Trap Triggered")
                        else: # Slayer/spy is defender
                            defStrength = 0
                    if defStrength == 1: # Corrects dragon/marshal strength
                        defStrength = 10


                    if activePlayer == 'R':
                        if atkStrength > defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While attacking, Red's %s captured Blue's %s." % (atkPiece,defPiece))
                            if attacker[-1:] == "*": return attacker
                            else: return attacker+"*"
                        elif atkStrength < defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While defending, Blue's %s captured Red's %s." % (defPiece,atkPiece))
                            if defender[-1:] == "*": return defender
                            else: return defender+"*"
                        else:
                            messagebox.showinfo(title="Attack Summary",message="In combat, both Red's %s and Blue's %s were captured." % (atkPiece,defPiece))
                            return "Empty"
                    else:
                        if atkStrength > defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While attacking, Blue's %s captured Red's %s." % (atkPiece,defPiece))
                            if attacker[-1:] == "*": return attacker
                            else: return attacker+"*"
                        elif atkStrength < defStrength:
                            messagebox.showinfo(title="Attack Summary",message="While defending, Red's %s captured Blue's %s." % (defPiece,atkPiece))
                            if defender[-1:] == "*": return defender
                            else: return defender+"*"
                        else:
                            messagebox.showinfo(title="Attack Summary",message="In combat, both Blue's %s and Red's %s were captured." % (atkPiece,defPiece))
                            return "Empty"

            def change_visibility(tileArray,tileStateArray):
                for y in range(len(arrayDict[tileArray])):
                    for x in range(len(arrayDict[tileArray][y])):
                        curTile = arrayDict[tileStateArray][y][x]
                        if curTile[0] != activePlayer and curTile != "Empty" and curTile != "Impassible" and curTile[-1:] != "*":
                            arrayDict[tileArray][y][x].configure(text="?")
                        else:
                            arrayDict[tileArray][y][x].configure(text=curTile)
            
            def update_deployment_restrictions(tileArray):
                for y in range(len(arrayDict[tileArray])):
                    for x in range(len(arrayDict[tileArray][y])):
                        if selectedGamemode.get() == "Classic": i = 4
                        else: i = 3

                        if len(deploymentComplete) != 2:
                            if activePlayer == 'R': # Red player is deploying
                                if y < i: # Blue deployment zone (Top 3-4 rows)
                                    arrayDict[tileArray][y][x].configure(state="disabled")
                                elif y >= (len(arrayDict[tileArray])-i): # Red deployment zone (Bottom 3-4 rows)
                                    arrayDict[tileArray][y][x].configure(state="normal")
                            else: # Blue player is deploying
                                if y < i: # Blue deployment zone (Top 3-4 rows)
                                    arrayDict[tileArray][y][x].configure(state="normal")
                                elif y >= (len(arrayDict[tileArray])-i): # Red deployment zone (Bottom 3-4 rows)
                                    arrayDict[tileArray][y][x].configure(state="disabled")
                        else:
                            arrayDict[tileArray][y][x].configure(state="normal")

            def activate_unit_ability():
                global unitAbility, tileContent
                abilityButton.configure(state="disabled")
                if tileContent[-1:] != "*":
                    if selectedGamemode.get() == "Classic":
                        if tileContent[1] == '2':
                            #unitAbility = CLASSIC_ROSTER[tileContent[1]][0]
                            unitAbility = "Scout"
                            tileContent += "*"
                        elif tileContent[1] == 'S' or tileContent[1] == '3' or tileContent[1] == 'T' or tileContent[1] == 'F':
                            messagebox.showinfo(title="Passive Abilty",message="The selected unit's special rules are always active.")
                        else:
                            messagebox.showinfo(title="No Abilty",message="The selected unit has no active ability.")
                    else:
                        if tileContent[1] == 'S' or tileContent[1] == '3' or tileContent[1] == 'T' or tileContent[1] == 'F':
                            messagebox.showinfo(title="Passive Abilty",message="The selected unit's special rules are always active.")
                        else:
                            unitAbility = FANTASY_ROSTER[tileContent[1]][0]
                            tileContent += "*"
                else:
                    messagebox.showinfo(title="Abilty Depleted",message="The selected unit is revealed, and thus cannot use its ability.")

            def position_check(x,y):
                if unitAbility == "Scout":
                    if not(abs(oldX-x) > 1 and abs(oldY-y) > 1):
                        if abs(oldX-x) > 1:
                            if oldX-x > 0:
                                for tile in range(x,oldX):
                                    print("tile="+str(tile)+" oldX="+str(oldX)+" x="+str(x))
                                    if arrayDict["tileStateArrayM"][y][tile] != "Empty":
                                        return False
                                return True
                            else:
                                for tile in range(oldX,x):
                                    print("tile="+str(tile)+" oldX="+str(oldX)+" x="+str(x))
                                    if arrayDict["tileStateArrayM"][y][tile] != "Empty":
                                        return False
                                return True
                        else:
                            if oldY-y > 0:
                                for tile in range(y,oldY):
                                    print("tile="+str(tile)+" oldY="+str(oldY)+" y="+str(y))
                                    if arrayDict["tileStateArrayM"][tile][x] != "Empty":
                                        return False
                                return True
                            else:
                                for tile in range(oldY,y):
                                    print("tile="+str(tile)+" oldY="+str(oldY)+" y="+str(y))
                                    if arrayDict["tileStateArrayM"][tile][x] != "Empty":
                                        return False
                                return True
                elif unitAbility == "Elf" or unitAbility == "Sorceress" or unitAbility == "Mage":
                    return not(abs(oldX-x)+abs(oldY-y) > 4)
                elif unitAbility == "Knight" or unitAbility == "Beast Rider":
                    return not(abs(oldX-x)+abs(oldY-y) > 2)
                elif unitAbility == "Dragon":
                    if not(abs(oldX-x) > 1 and abs(oldY-y) > 1):
                        if abs(oldX-x) > 1:
                            if oldX-x > 0:
                                for tile in range(x,oldX):
                                    if arrayDict["tileStateArrayM"][y][tile] == "Empty":
                                        return False
                                return True
                            else:
                                for tile in range(oldX,x):
                                    if arrayDict["tileStateArrayM"][y][tile] == "Empty":
                                        return False
                                return True
                        else:
                            if oldY-y:
                                for tile in range(y,oldY):
                                    if arrayDict["tileStateArrayM"][tile][x] == "Empty":
                                        return False
                                return True
                            else:
                                for tile in range(oldY,y):
                                    if arrayDict["tileStateArrayM"][tile][x] == "Empty":
                                        return False
                                return True
                else: # Default standard move/attack
                    return not(abs(oldX-x)+abs(oldY-y) > 1) and not(abs(oldX-x)+abs(oldY-y) == 0)
            
            # Reads the contents of the cell background data and moves pieces as allowed by valid moves, then updates the board buttons
            def move_selection(tileArray,tileStateArray,y,x):
                global tileContent, oldX, oldY, unitAbility
                selectedTile = arrayDict[tileStateArray][y][x] # Indicates which tile is being accessed
                if selectedTile != "Impassible": # Checks that both destination and source tiles aren't impassible
                    if tileContent != "": # Runs if selected tile is second tile clicked (ie, selected tile is the destination tile)
                        if activePlayer in deploymentComplete: # If deployment is complete, follow normal movement rules and enable combat
                            if BoardFunctionality.position_check(x,y): # Checks that piece making a legal move
                                # ADD UNIT ABILITIES TO ELSE IF HERE
                                if selectedTile[0] == activePlayer: # Checks that destination tile does not contain friendly unit
                                    messagebox.showinfo(title="Invalid Selection",message="You cannot end your movement on a tile containing a friendly unit.")
                                elif selectedTile != "Empty": # Checks is destination tile contains enemy unit
                                    '''if confirmationPrompt:
                                        Root.open_window(self,"Move Confirmation",type="moveConfirm")'''
                                    BoardFunctionality.highlight_selection(tileArray,tileStateArray,y,x)
                                    arrayDict[tileStateArray][y][x] = BoardFunctionality.resolve_combat(tileContent,selectedTile)
                                    tileContent = "" # Clears storage variable to allow new source tile
                                    unitAbility == "None"
                                    BoardFunctionality.end_turn(activePlayer)
                                else: # If tile is empty
                                    BoardFunctionality.highlight_selection(tileArray,tileStateArray,y,x)
                                    arrayDict[tileStateArray][y][x] = tileContent # Assigns destination tile to original value of source tile
                                    tileContent = "" # Clears storage variable to allow new source tile
                                    unitAbility == "None"
                                    BoardFunctionality.end_turn(activePlayer)
                            else:
                                messagebox.showinfo(title="Invalid Selection",message="You must move to an adjecent orthagonal tile, or according to the selected unit's special ability.")
                        else:
                            if selectedTile[0] == activePlayer: # Checks that destination tile does not contain friendly unit
                                messagebox.showinfo(title="Invalid Selection",message="You cannot end your movement on a tile containing a friendly unit.")
                            else: # If tile is empty
                                BoardFunctionality.highlight_selection(tileArray,tileStateArray,y,x)
                                arrayDict[tileStateArray][y][x] = tileContent # Assigns destination tile to original value of source tile
                                tileContent = "" # Clears storage variable to allow new source tile
                                BoardFunctionality.end_turn(activePlayer)
                    else: # Runs if selected tile is first tile clicked (ie, selected tile is the source tile)
                        if selectedTile != "Empty": # Won't allow an empty tile to be assigned as source tile
                            if selectedTile[0] == activePlayer: # Selected unit is controlled by active player
                                if (activePlayer in deploymentComplete) and selectedTile[1] != 'T' and selectedTile[1] != 'F': # Checks if deployment is finished for active player and that piece is mobile
                                    BoardFunctionality.highlight_selection(tileArray,tileStateArray,y,x)
                                    tileContent = selectedTile # Set storage variable to source tile's value
                                    oldX,oldY = x,y
                                    arrayDict[tileStateArray][y][x] = "Empty" # Set source tile value to empty to show piece has left tile
                                    abilityButton.configure(state="normal",bg='yellow')
                                elif (activePlayer not in deploymentComplete): # Checks that player is still deploying
                                    BoardFunctionality.highlight_selection(tileArray,tileStateArray,y,x)
                                    tileContent = selectedTile # Set storage variable to source tile's value
                                    if tileStateArray[-1:] != "M": # Checks that player is placing new unit
                                        arrayDict['quantityStateArrayP%1c'%activePlayer][y] -= 1 # Reduces the quantity of selected unit left to deploy
                                        arrayDict['quantityArrayP%1c'%activePlayer][y].configure(text=str(arrayDict['quantityStateArrayP%1c'%activePlayer][y])) # Updates quantity counter
                                        if arrayDict['quantityStateArrayP%1c'%activePlayer][y] == 0:
                                            arrayDict[tileStateArray][y][x] = "Disabled" # Set source tile value to disabled to show all pieces of that type are placed
                                    else:
                                        arrayDict[tileStateArray][y][x] = "Empty" # Set source tile value to empty to show piece has left tile
                                else:
                                    messagebox.showinfo(title="Invalid Selection",message="That is not a valid piece of the active player.")
                            else:
                                messagebox.showinfo(title="Invalid Selection",message="That is not a valid piece of the active player.")
                        else:
                            messagebox.showinfo(title="Invalid Selection",message="That is not a valid piece of the active player.")
                else:
                    messagebox.showinfo(title="Invalid Selection",message="That tile is impassible terrain.")
                heldUnitTracker.configure(text=("Held Unit: "+tileContent)) # Updates value of unit tracker

            # Highlights selected cell in gold on click
            def highlight_selection(tileArray,tileStateArray,y,x):
                global selectedButton, lastBG
                button = arrayDict[tileArray][y][x]
                if selectedButton is not None:
                    selectedButton.configure(bg=lastBG)
                lastBG = button.cget("bg")
                selectedButton = button
                button.configure(bg="gold") # Updates background of tile to stay highlighted
                if arrayDict[tileStateArray][y][x] == "Disabled":
                    button.configure(state="disabled") # 

        # ??MERGE GENERATE + POPULATE??

        # Generates an empty board array based on the dimensions provided
        # arrayDict['tileArrayM'][y][x] format -> stored as yx  -> increments across
        def generate(arrayHeight, arrayWidth, useCase):
            global arrayDict

            # Expandable else if tree that determines where arrays are being created
            if useCase == "board":
                # Creates clickable tiles for the user
                arrayDict['tileArrayM'] = [[tk.Button(self,relief="groove",activebackground="gold") for x in range(arrayWidth)] for y in range(arrayHeight)]
                # Stores data on cells in background
                arrayDict['tileStateArrayM'] = [["Empty" for x in range(arrayWidth)] for y in range(arrayHeight)]
            elif useCase == "playerSheet":
                # Creates clickable tiles for the user
                arrayDict['tileArrayP%1c'%activePlayer] = [[tk.Button(self,relief="groove",activebackground="gold") for x in range(arrayWidth)] for y in range(arrayHeight)]
                # Stores data on cells in background
                arrayDict['tileStateArrayP%1c'%activePlayer] = [[(activePlayer+str(UNIT_STRENGTH[y])) for x in range(arrayWidth)] for y in range(arrayHeight)]
                # Creates additional array to display unit quantity to players (unique to player sheets)
                if selectedGamemode.get() == "Classic":
                    arrayDict['quantityStateArrayP%1c'%activePlayer] = [CLASSIC_ROSTER[UNIT_STRENGTH[y]][1] for y in range(arrayHeight)]
                else:
                    arrayDict['quantityStateArrayP%1c'%activePlayer] = [FANTASY_ROSTER[UNIT_STRENGTH[y]][1] for y in range(arrayHeight)]
                arrayDict['quantityArrayP%1c'%activePlayer] = [tk.Label(self,text=arrayDict['quantityStateArrayP%1c'%activePlayer][y]) for y in range(arrayHeight)]
                for y in range(arrayHeight):
                    arrayDict['quantityArrayP%1c'%activePlayer][y].grid(row=y,column=1,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        # Fills generated arrays with properly formatted buttons
        def format_initial_array(tileArray, tileStateArray, leftOffset=0, offsetSize=0): # leftOffset - Number of columns to offset for GUI on left of board grid
            # Section for left-side GUI widgets
            if leftOffset > 0:
                for i in range(leftOffset):
                    self.columnconfigure(i, weight= 2, minsize=offsetSize)
            
            # Creates array grid and places button within each cell
            for y in range(len(arrayDict[tileArray])):
                self.rowconfigure(y, weight= 1, minsize=50)
                for x in range(len(arrayDict[tileArray][y])):
                    self.columnconfigure(x+leftOffset, weight= 1, minsize=50)

                    # Call sub-dictionaries (children of arrayDict) of button variable names and configure appropriately, each initial assigned as str(y)+str(x)'[row-number][col-number]'
                    arrayDict[tileArray][y][x].configure(text=arrayDict[tileStateArray][y][x],
                                        command=lambda tempTA=tileArray,
                                        tempTSA=tileStateArray,tempY=y,tempX=x: 
                                        [BoardFunctionality.move_selection(tempTA,tempTSA,tempY,tempX)])

                    if tileArray[-1:] == "M": # Checks if main board is being generated
                        self.rowconfigure(y, weight= 1, minsize=75)
                        self.columnconfigure(x+leftOffset, weight= 1, minsize=75)
                        # Sets up impassible tiles in middle of board and player deployment zones based on gamemode
                        if selectedGamemode.get() == "Classic":
                            i,j = 4,5
                            #self.geometry(str(750+((leftOffset+1)*offsetSize))+"x750") # Sets size of board window based on gamemode
                            Root.set_geometry(self,750+((leftOffset+1)*offsetSize),750) # Sets size of board window based on gamemode
                        else:
                            i,j = 3,4
                            #self.geometry(str(750+((leftOffset+1)*offsetSize))+"x600") # Sets size of board window based on gamemode
                            Root.set_geometry(self,750+((leftOffset+1)*offsetSize),600) # Sets size of board window based on gamemode
                        if (y==i or y==j) and (x==2 or x==3 or x==6 or x==7):
                            arrayDict[tileStateArray][y][x] = "Impassible"
                            arrayDict[tileArray][y][x].configure(text="Impassible",bg="#13f3ee") # Temporary indicator
                        elif y < i:
                            arrayDict[tileArray][y][x].configure(bg="#a7cffa") # Temporary indicator
                        elif y >= (len(arrayDict[tileArray])-i):
                            arrayDict[tileArray][y][x].configure(bg="#ea9f9f") # Temporary indicator

                        arrayDict[tileArray][y][x].configure(state="disabled")
                        
                        # Section for right-side GUI widgets on main board
                        global rulesButton, abilityButton

                        self.columnconfigure(leftOffset+len(arrayDict[tileArray][0]), weight= 2, minsize=offsetSize)
                        RIGHTELEMENT1 = tk.Text(self,wrap='word')
                        RIGHTELEMENT1.insert(1.0,"Here's where a GUI element will go.")
                        RIGHTELEMENT1.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=0,rowspan=1)
                        RIGHTELEMENT1.configure(bg=self.cget('bg'),relief='flat',state='disabled')

                        rulesButton = tk.Button(self,text="Rules of Play",bg='green',command=lambda:[print("Rules")])
                        rulesButton.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=len(arrayDict[tileArray])-3,rowspan=1)
                        
                        abilityButton = tk.Button(self,text="Unit Ability",bg='yellow',state="disabled",command=lambda:[BoardFunctionality.activate_unit_ability()])
                        abilityButton.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=len(arrayDict[tileArray])-2,rowspan=1)

                        # Button that 
                        #startTurnButton = tk.Button(self,text="Start Turn",bg='green',command=lambda:[BoardFunctionality.end_turn(activePlayer)])
                        #startTurnButton.grid(column=leftOffset+len(arrayDict[tileArray][0]),row=len(arrayDict[tileArray])-1,rowspan=1)
                    
                    arrayDict[tileArray][y][x].grid(column=x+leftOffset,row=y,sticky=(tk.N,tk.S,tk.E,tk.W)) # Positions buttons within the window's grid
        
        # Allows user to close listed windows manually, otherwise prevents deletion of critical windows/components
        if type != "exit" and type != "invalid" and type != "options" and type != "pauseMenu":
            self.protocol("WM_DELETE_WINDOW", root.close_confirm)

        # Large and expandable else if tree determines what type of window is being built to format accordingly
        if type == "mainMenu": # UNFINISHED
            Root.set_geometry(self,300,200)
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
            Root.set_geometry(self,200,300)
            tk.Button(self,
                       text="Save options",
                       command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.LEFT)  # UNFINISHED
            tk.Button(self,
                       text="Cancel",
                       command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.RIGHT)
        

        elif type == "pauseMenu": #UNFINISHED
            Root.set_geometry(self,200,300)
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
            Root.set_geometry(self,250,100)
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
                    command=lambda: end_setup()).pack(side=tk.LEFT)
            tk.Button(self,
                    text="Back",
                    command=lambda: [mainMenu.deiconify(), self.destroy()]).pack(side=tk.RIGHT) # Unhide main menu and destroy setup page
            
            # Signals setup is complete and generates board based on chosen settings
            def end_setup():
                root.open_window("Board", "board")
                create_player_windows()
                BoardFunctionality.update_deployment_restrictions("tileArrayM")
                self.destroy() # Destroys the setup window
            
            def create_player_windows(): # Creates the initial windows for players' personal sheets
                global activePlayer
                root.open_window("Player 1", "playerSheet")
                activePlayer = 'B'
                root.open_window("Player 2", "playerSheet")
                activePlayer = 'R'
        

        elif type == "playerSheet": # Formats the players' personal sheets
            # Creates button array for units
            generate(12,1,"playerSheet")
            # Formats player sheets based on identity
            sheetHeader = ttk.Label(self)
            #self.configure(name="playerSheetP%c"%activePlayer)
            if activePlayer == 'R':
                sheetHeader.configure(text="Player Number 1")
                self.configure(background="red")
                Root.set_geometry(self,200,750,30) # Sets dimensions of window
                format_initial_array('tileArrayPR', 'tileStateArrayPR')
            elif activePlayer == 'B':
                sheetHeader.configure(text="Player Number 2")
                self.configure(background="blue")
                Root.set_geometry(self,200,750,1306) # Sets dimensions of window
                format_initial_array('tileArrayPB', 'tileStateArrayPB')
            # Creates an obvious error if player count is misinterpretted
            else:
                sheetHeader.configure(text="PLAYER SHEET ERROR")
                self.configure(background="yellow")
            sheetHeader.grid(row=0,column=2) # Positions header correctly in frame
            # HIDES ALL OTHER PLAYERS + BOARD IF NO OTHER ACTION TAKEN FIRST -> Locks up if no other windows available/open
            tk.Button(self,
                       text="Confirm Deployment",
                       command=lambda:[deploymentComplete.append(activePlayer),
                                       BoardFunctionality.end_turn(activePlayer),
                                       Root.open_window(root,"Change Player", "blocker"),
                                       BoardFunctionality.change_visibility('tileArrayM','tileStateArrayM')]).grid(row=11,column=2) # Confirms that the players units are deployed as they wish            


        elif type == "board": # Creates the main board window, where most of the interaction takes place
            global arrayDict, heldUnitTracker, turnIndicator

            # Generates correct board layout based on chosen gamemode
            if selectedGamemode.get() == "Classic":
                generate(10,10,"board")
            elif selectedGamemode.get() == "Fantasy":
                generate(8,10,"board")
            
            # Creates button to access the pause menu in the upper-lefthand corner of the main board
            pauseButton = tk.Button(self,text="Menu",command=lambda: [root.open_window("Pause Menu", "pauseMenu")])
            pauseButton.grid(column=0,row=0,sticky=(tk.N,tk.W)) # Positions button correctly in frame
            
            # Creates indicator that shows the current active player (ie the player whose turn it is)
            tk.Label(self,text="Active Player:").grid(column=0,row=1)
            turnIndicator = tk.Label(self, bg="red") # Sets the initial value of the indicator to red (red is player 1)
            turnIndicator.grid(column=0,row=2,sticky=(tk.E,tk.W), padx=5) # Positions indicator correctly in frame

            # Creates indicator that shows identity of the held unit, if any (ie the unit being moved by the active player)
            heldUnitTracker = tk.Label(self,text=("Held Unit: "+tileContent))
            heldUnitTracker.grid(column=0,row=3) # Positions indicator correctly in frame

            format_initial_array("tileArrayM","tileStateArrayM",1,150)
        

        elif type == "moveConfirm":
            Root.set_geometry(self,250,100)
            tk.Label(self,text="Confirm that this is your intended move?").pack(side=tk.TOP)
            tk.Button(self,
                    text="Confirm Move",
                    command=lambda: end_setup()).pack(side=tk.LEFT)
            tk.Button(self,
                    text="Cancel Move",
                    command=lambda: [self.destroy()]).pack(side=tk.RIGHT) # Unhide main menu and destroy setup page
            tk.Label(self,text="This setting can be disabled from the pause menu.",font=('Segoe UI',5)).pack(side=tk.BOTTOM)


        elif type == "blocker":
            self.attributes('-fullscreen',True)
            tk.Label(self,text="Pass control to other player.").pack()
            tk.Button(self,
                    text="Start Turn",
                    command=self.destroy).pack()


        elif type == "exit":
            Root.set_geometry(self,300,100)
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

# Main foundational super-class from which all windows are created and initial system actions are taken on program start
class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw() # Hide this window on creation

    def close_all(self):  # Closes all windows, including hidden
        for child in self.winfo_children():
            child.destroy()
        self.destroy()
    
    # Opens window of the type specified by argument with entered title
    def open_window(self, title, type):
        window = Window(self, title, type)
        window.resizable(False,False) # Disables ability to resize windows to maintain cohesive appearance
        if type == "exit" or type == "options" or type == "pauseMenu" or type == "blocker" or type == "moveConfirm":  # If critical window, forces user interaction
            window.grab_set()

        return window

    def close_confirm(self):  # Creates confirmation window
        self.open_window("Confirm exit?", "exit")
    
    def set_geometry(self,width,height,x=-1,y=-1): # Set position and dimensions of window
        w = width # Window width in pixels
        h = height # Window height in pixels
        # Get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen
        # Calculate x and y coordinates for window
        if x == -1: # If no specific location given, center to screen horizontally
            x = (ws/2) - (w/2)
        if y == -1: # If no specific location given, center to screen vertically
            y = (hs/2) - (h/2) - 50
        # Set the dimensions and location of window
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    '''def close_confirm(self):  # Creates confirmation window
        #confirm = messagebox.askokcancel(title="Confirm exit?",message="Save and close all windows?")
        if messagebox.askokcancel(title="Confirm exit?",message="Save and close all windows?"):
            for child in root.winfo_children(): # Closes all windows, including hidden
                child.destroy()
            root.destroy()'''
    
    # If game in progress is continued, reads info from external txt file in which save game data is stored
    def load_save(saveName):
        saveFile = open(saveName, "r") # Opens appropriate save data txt file
        for line in saveFile:
            if "playerCount" in line: # Reads [example] from save data txt file and assigns to global variable
                global playerCount
                playerCount = line[-1:]
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
