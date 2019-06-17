import random

"""
NOTES: As this is a locally-run simulation there aren't any race conditions to consider,
but if this was deployed onto the internet with multiple users, issues might arise with the dialog list.
To be perfectly honest, I am not familiar with race conditions beyond the couple of pages about it in my coding book.

Also if given more time, I could possibly build a live version of this with node.js and mongodb.

To run the simulation locally, clone the github repo, navigate to the folder in your terminal, and type "python3 mud.py".

Thank you!
"""

class Dungeon:
    def __init__(self, numberOfPlayers=1):
        self.world = {}
        self.players = {}
        self.roomCap = 20000 # cap on the number of rooms
        self.n = 0 # size of world, scales with number of players
        self.numberOfPlayers = numberOfPlayers
        self.playerSpawn = (1,1,1)
        self.addRooms(numberOfPlayers*5)
        self.addPlayers()

    def permute(self, a):
        # takes in an array of x,y,z coordinates
        # returns a set of all the unique permutations of that array's items.
        array = a
        permutations = set()
        def __helper(a, l, r):
            if l==r:
                perm = tuple(a)
                permutations.add(perm)
            else:
                for i in range(l,r+1):
                    a[l], a[i] = a[i], a[l]
                    __helper(a, l+1, r)
                    a[l], a[i] = a[i], a[l]
            return permutations
        return __helper(array, 0, 2)

    def addRooms(self, number=1, x=None, y=None, z=None):
        # builds out the world space creating 3d coordinates in a number by number by number block
        # first generates a random boolean to declare if the room is transparent or not.
        # if it is transparent, add it to the dictionary of the world
        # solid rooms are not stored.
        if x == None or y == None or z == None:
            x = y = z = self.n # set the starting coordinate
        self.n += number # set the new set of starting coordinate each time the function is run, so it iterates where it left off.
        while x < number and len(self.world) < self.roomCap:
            coordinate = [x,y,z]
            for coord in self.permute(coordinate):
                if coord == self.playerSpawn:
                    self.world[coord] = self.Room(self.playerSpawn[0], self.playerSpawn[1], self.playerSpawn[2])
                elif random.choice([True, False]):
                    self.world[coord] = self.Room(coord[0], coord[1], coord[2])
            x+=1
            y=0
            while y < number and len(self.world) < self.roomCap:
                coordinate = [x,y,z]
                for coord in self.permute(coordinate):
                    if coord == self.playerSpawn:
                        self.world[coord] = self.Room(self.playerSpawn[0], self.playerSpawn[1], self.playerSpawn[2])
                    elif random.choice([True, False]):
                        self.world[coord] = self.Room(coord[0], coord[1], coord[2])
                y+=1
                z=0
                while z < number and len(self.world) < self.roomCap:
                    coordinate = [x,y,z]
                    for coord in self.permute(coordinate):
                        if coord == self.playerSpawn:
                            self.world[coord] = self.Room(self.playerSpawn[0], self.playerSpawn[1], self.playerSpawn[2])
                        elif random.choice([True, False]):
                            self.world[coord] = self.Room(coord[0], coord[1], coord[2])
                    z+=1
                else:
                    coordinate = [x,y,z]
                    for coord in self.permute(coordinate):
                        if coord == self.playerSpawn:
                            self.world[coord] = self.Room(self.playerSpawn[0], self.playerSpawn[1], self.playerSpawn[2])
                        elif random.choice([True, False]):
                            self.world[coord] = self.Room(coord[0], coord[1], coord[2])

    def addPlayers(self, n=1, name=None, adventurerType=None, background=None):
        for _ in range(n):

            name = input("\n\nHello, adventurer. What is thy name? \n\n") # multiple users can have the same name, which is an issue with the addTell() method
            background = input("\n\nOh cool. Where does thee hail from and praytell what is thy background? \n\n")
            adventurerType = input("\n\nIn a word, what type of adventurer are thee? \n\n")

            new_player = self.Player(self.numberOfPlayers+_, name,adventurerType,background, self.world[tuple(self.playerSpawn)])
            self.players[self.numberOfPlayers+_] = new_player # add the player to the dungeon's player dictionary
            self.world[tuple(self.playerSpawn)].players[self.numberOfPlayers+_] = new_player # add the player to the spawn-room's player dictionary

        self.numberOfPlayers+=n
        self.addRooms(n*5)

    def testMove(self, player, direction):
        test = player.move(direction)
        test = tuple(test)
        if test in self.world:
            del player.room.players[player.index] # delete the player from the room's player dictionary
            self.world[test].players[player.index] = player # change the room's player dictionary to include a reference to the player
            player.room = self.world[test] # change the player's room attribute to reference the Room object in the dungeon's world dictionary
            self.world[test].setDescription() # run setDescription() method
            print("You move " + direction + ".")
        else:
            print("There is nothing that way.")

    def whereMove(self, player):
        directions = ["north","south","east","west","up","down"]
        moves = []
        for direction in directions:
            test = player.move(direction)
            test = tuple(test)
            if test in self.world:
                moves.append(direction)
        print(moves)

    def addSays(self, content, speaker):
        for player in speaker.room.players:
            self.players[player].dialog.addNode(content, speaker)

    def addYells(self, content, speaker):
        for player in self.players:
            if self.players[player].quietMode == False:
                self.players[player].dialog.addNode(content,speaker)

    def addTell(self, content, listener, speaker):
        listener.dialog.addNode(content, speaker)

    def printDirections(self):
        print("\n\nEnter 'east', 'west', 'north', 'south', 'up', or 'down' to move in one of those directions.\nEnter 'where' to see which directions are available to move in.\nYou can type 'say' to tell the people in the same room something,\n'yell' to tell everyone in the world something,\nand 'tell' to tell something to someone whose name you know.\nType 'quiet' to toggle quiet mode on and off.\n\nEnter 'x' to leave this world.\n")

    def runGame(self):
        inp = None
        print("\nAnd so the adventure begins!")
        self.printDirections()
        while inp != "x":
            if inp == "east":
                self.testMove(self.players[1], "east")
            elif inp == "west":
                self.testMove(self.players[1], "west")
            elif inp == "north":
                self.testMove(self.players[1],"north")
            elif inp == "south":
                self.testMove(self.players[1], "south")
            elif inp == "up":
                self.testMove(self.players[1], "up")
            elif inp == "down":
                self.testMove(self.players[1], "down")
            elif inp == "where":
                self.whereMove(self.players[1])
            elif inp == "say":
                content = str(input("\n\nWhat would you like to say?\n\n"))
                self.addSays(content, self.players[1])
            elif inp == "tell":
                person_to_speak_to = str(input("\n\nWho would you like to speak to?\n\n"))
                for people in self.players:
                    if person_to_speak_to == self.players[people].name:
                        listener = self.players[people]
                content = str(input("\n\nWhat would you like to say?\n\n"))
                self.addTell(content, listener, self.players[1])
            elif inp == "yell":
                content = str(input("\n\nWhat would you like to say?\n\n"))
                self.addYells(content, self.players[1])
            elif inp == "quiet":
                self.players[1].quiet()
            elif inp == "directions":
                self.printDirections()

            print("Moves:")
            self.whereMove(self.players[1])
            print("Dialog:")
            print(self.players[1].dialog.showDialog())
            inp = str(input("\nWhat would you like to do? (Type 'directions' to see the options.)\n\n"))

    class Room:
        def __init__(self, x, y, z, description=None):
            self.x=x
            self.y=y
            self.z=z
            self.coordinate = [x,y,z]
            self.description = None
            self.players = {}
            self.items = {}
            self.monsters = {}

        def setDescription(self, userInput=None):
            room_occupants = ["In this room with you is..."]
            if self.description == None:
                self.description = input("\n\nYou are the first to arrive to this part of the dungeon. What do you see?\n\n")
            for player in self.players:
                room_occupants.append(str(self.players[player].name) + " the " + str(self.players[player].adventurerType) + " from " + str(self.players[player].background))
            print(self.coordinate, self.description, room_occupants)

    class Player:
        def __init__(self, index, name, adventurerType, background, room):
            self.index = index
            self.name = name
            self.adventurerType = adventurerType
            self.background = background
            self.friends = {}
            self.room = room
            self.dialog = self.DialogList()
            self.quietMode = False

        def move(self, direction):
            direction_lookup = {"north":[0,1,0], "south":[0,-1,0], "east":[1,0,0], "west":[-1,0,0], "up":[0,0,1], "down":[0,0,-1]}
            test = direction_lookup[direction]
            for i, item in enumerate(self.room.coordinate):
                test[i] += item
            return test

        def quiet(self):
            if self.quietMode:
                print("Quiet Mode is off.")
                self.quietMode = False
            else:
                print("Quiet Mode is on.")
                self.quietMode = True

        class DialogList:
            def __init__(self, head=None, tail=None, maxNodes=5):
                self.head = head
                self.tail = tail
                self.numberOfNodes = 0
                self.maxNodes = maxNodes

            class DialogNode:
                def __init__(self, content="", player=None):
                    self.previous = None
                    self.next = None
                    self.content = content
                    self.speaker = player

            def addNode(self, content, speaker):
                new_node = self.DialogNode(content, speaker)
                self.numberOfNodes += 1
                if self.numberOfNodes > self.maxNodes:
                    self.head = self.head.next
                    self.head.previous = None
                if self.head == None:
                    self.head = self.tail = new_node
                self.tail.next = new_node
                self.tail = new_node
                self.tail.next = None

            def showDialog(self):
                content = []
                node = self.head
                while node:
                    content.append(node.content)
                    node = node.next
                return content

    class Item:
        def __init__(self, name, description):
            self.name = name
            self.description = description

    class Monster:
        def __init__(self, name, description):
            self.name = name
            self.description = description

newDungeon = Dungeon(1)
newDungeon.runGame()
