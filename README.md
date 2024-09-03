# Planetary War

Planetary war is an Earth-scale multiplayer online game inspired by Risk.

It is a fun project for me to learn some more web stuff, and it will totally break (in spite of the intrinsic rate limiting) the moment someone builds a bot for it.

## The game
Take a model of earth, project a hex map onto it.  

New players are randomly assigned a team, and randomly assigned a vacant hex, and given 3 infantry units on their hex.

On each "turn", a player can 
- Invade (or attempt to invade) as many neighbouring hexes as they like
- Move their troops to different hexes so long as there is a contiguous path of allied territory
- (late in the roadmap) upgrade their units
- (late in the roadmap) sail - this will need to be mechaniched, probably a distance limited by the number of hexes controlled?
- spawn and place new units

A turn must take less than 30 seconds of real time
A player can take their turn whenever they like in real time, but not if their previous turn ended within the last hour.

## balance and making it interesting and stuff
Battles will be random, but influenced by the number of attacker/defenders

Players starting locations will need to be algorigthmed out a little bit - they should have at least one enemy within a few turns' striking distance.  Later on, I might need to make it so that newbies don't spawn next to giants, and also might need to manually spawn some people on different continents

(later in the roadmap) it might be fun to incorporate some natural geography - attrition in harsh environments, additional resource growth in hospitable environments or maybe for controlling major cities?


## Architecture and stuff
- Flask backend
- Start with SQLite and see how we go
- Front end will be suprisingly simple I think - bootstrap, Openlayers for handling the mapping

