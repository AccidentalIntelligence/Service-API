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

##### User Code
User codes are unique to each individual user, and resolve to a string
containing a special prefix, and the unique ID of the user:
```
user-id:5a32d321
```

### Geolocation
Geolocation is used to support other features. Locations can geotag themselves
as quest hubs or dungeons. Quests may require you to go to certain locations
to progress. Certain player interactions may require you to be in the same
physical location as the other player.

### Character Development
As you play the game, your character not only acquires gear and wealth, but
also experience which can be used to increase the players stats, or learn new
skills and abilities.

#### Player Stats
TODO

#### Player Skills
TODO

### Quest System
TODO

### Crafting System
TODO

### Party System
TODO

### Trade System
TODO

### Creatures/Opponents
TODO

### Special Events
TODO
