# Log

## 23-09-2022
*14.43* Added issue #1 about lag when rendering worlds with many tiles.
*15.17* Added `load_existing` parameter to the world init function, if this parameter is equal to true it will try to load an existing world with the specified world name, if it is equal to false it will generate a new world using the map size specified.
*16.03* Added checks to the world name to make sure it starts with an alphabetical character, only contains alphanumerical characters, is a string, and contains at least 1 character and at most 250. Also added exception handling to loading of the world.
*16.06* Added checks to verify that the map size is an integer greater than or equal to 1.
*17.17* Added exception handling to the world generation.

## 22-09-2022
*12.42* Added a sheet of character textures animations, also added folders of separate images of these characters (these are only local right now to prevent cluttering the repo).
*17.39* Added player to the world, the camera can also be unlocked from/locked to the player by pressing the spacebar.

## 21-09-2022
*15.10* Added more textures for pine trees, added `sources.txt` file to `textures/` folder, added `scale` property to entity files.
*15.34* Entities are now inserted into the entities list by y coordinate, this ensures that the entities are rendered from top to bottom.

## 20-09-2022
*20.48* Added jungle trees and pine trees, added jungle trees, pine trees, and cacti to world generation.