# Barcode Warriors

This is a working title, but this service is the main workhorse for the barcode
based Android ARRPG (Augented Reality RPG). This readme is a summary of the
planned features, and service details.

## Overview

Barcode Warriors is an android based mobile augmented reality RPG. The main
gameplay is hinged around the scanning of barcodes found in the world, to
explore and discovery items and treasures. During their adventures, the player
will develop their character, allowing them to take on ever more perilous
encounters, for ever more lucrative rewards.

## Features

#### Feature List:
* Scan barcodes to discover items, encounters and quests
* Geolocation, to create location based events and enhanced questing
* Character development, adding a real RPG element to the game
* Detailed quest system, giving interesting encounters, and fun rewards
* Salvage based crafting system, to obtain and build better gear
* Party system, allowing players to form teams to take on tougher encounters
* Trade system, allowing players to trade items and currency
* Many creatures to find, defeat, or capture and train
* Sponsored events, for businesses or conventions, allowing interactive
customer experiences

### Barcode Scanning
The user can use the mobile app to scan any bar code. Some barcodes will have
special pre-determined encounters, some have special meaning, and others may
have special meaning based on the type of object scanned (food/drink etc). All
other barcodes will have a random encounter assigned, which will persist for
a time until the code goes dormant (the code isn't accessed for a period of
time).

#### Barcode Types
##### Standard Code
A standard barcode, which resolves to a long number. That number is then
sent to a web based barcode database to retrieve data on the item that owns
that code. The information returned from the database is then used to determine
the type of that code. Types include:
* Consumable (food/drink)
* Equipment
* Book
* Special

Barcode Types:
* ISBN

##### User Code
User codes are unique to each individual user, and resolve to a string
containing a special prefix, and the unique ID of the user:
```
user-id:5a32d321
```

##### Event Code
Special events may be provided with special codes used to provide unique
challenges to attendees. Those codes will have an event identifier, and a long
unique code:
```
event:2dfe2d7fcc9e21g4...
```

### Geolocation
Geolocation is used to support other features. Locations can geotag themselves
as quest hubs or dungeons. Quests may require you to go to certain locations
to progress. Certain player interactions may require you to be in the same
physical location as the other player.

We may also link barcodes to geolocation information, such that one barcode
may illicit different results to people in different geographic locations.

### Character Development
As you play the game, your character not only acquires gear and wealth, but
also experience which can be used to increase the players stats, or learn new
skills and abilities.

#### Player Stats
TODO

#### Player Skills
Split into:
* Combat skills
* Lore skills
* Crafting skills

### Quest System
The quest system will have some similarities to the standard quest systems a
player might expect from MMO games. The key difference is the requirement to
travel within the real world in order to track down clues, find objects or
defeat special foes.

### Crafting System
The crafting system is similar to that found in the MMORPG fallen earth. The
player will discover items and resources while traveling the world and
defeating foes. Those items can be combined to construct useful tools and
equipment to help the player on their adventures.

### Party System
In order to take on more dangerous and powerful foes, it may be required at
times to get help. Help can be found in two ways: Implicit and Explicit groups.
Implicit groups are ad-hoc "world" events where all players in a given area
are all involved in events that happen. This can include both boss fights, as
well as social settings (a virtual tavern, allowing chat and trade).
Explicit groups allow friends to form an adventuring party. Parties allow more
options for interaction with group mates, and allow additional synergies which
help the group overcome the most challenging scenarios.

### Trade System
Like the party system, players in the same location are able to interact with
each other in order to barter and trade goods.

### Creatures/Opponents
Dependent on setting.

### Special Events
Special events, as have been mentioned above, are special scenarios linked to
specific geographic locations. This can be public locations, such as libraries
and social hubs, and can also be linked to larger events, such as comic book
and gaming conventions.

While at a special event, special encounters may happen, one-time quests, and
special challenges only found at the event. For example, at a convention each
vendor may be provided with a special challenge bar code. If you visit each
booth, and defeat all the challenges, you may be entitled to win real world
prizes.
