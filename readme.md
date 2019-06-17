Server Engineering Candidate Programming Challenge 2

Estimated time required:
3-4 hours
Suggested language:
PHP
Challenge description:

MULTIUSER DUNGEON
You are an adventurer in a virtual world made up of unit rooms where each room is either transparent or solid. You can move in any of these 6 directions: north, south, east, west, up, down. Each move is considered to take exactly one room and you can move only through transparent rooms.

When in a room, you can see a description of the room and anything or anyone else in that room. Other adventurers also live in this world and from time to time, you will bump into them.

You can interact with other people by typing "say <dialog>" into a command prompt.
This will send a chat message to everyone in the room you are in. You can alternatively choose to type "tell <person_name> <dialog>".  Moreover, you can type "yell <dialog>" to yell across the entire world. Other commands include "<direction>" to move around, such as "north", "west". 

Commands should be flexible enough to extend to more innovative commands at a later time like, "pickup <item>", "fight <person>" or "put <item> <item>", but these commands need not be implemented.

How you display this world is entirely up to you. Text based display with a command prompt to input commands would probably be the default approach. A web API based approach with commands taking the form of API calls like /say/hello is also OK.

THINGS TO CONSIDER
Please Consider any race conditions that might arise with many users in the same room at once (100+). Whether or not you implement the solution to these race conditions, please address them in comments with how you would solve them. Some further thoughts to include are what kinds of problems can you foresee as the number of users in your virtual world scales up? What about if you start interacting with multiple monsters at once?

WORLD DATA FORMAT
Input can be however you want to describe the world, the only
restriction is that it should be both flexible and scalable.

NOTES
The test is not time limited and you can send it back as soon as you finish it. But obviously, the sooner the better.

When you're done please send me either a link to a live version of this world on a website that you host, or if you are doing this on a local machine, please send me instructions of how to deploy your simulation. Please send along anything else you may want to add (test files, etc.)

We will mainly look at your approach to the problem, your algorithm, code clarity,
and the design choices made.
What to submit:

Source code
