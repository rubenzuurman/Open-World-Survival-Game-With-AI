# Open-World-Survival-Game-With-AI

## Description
This is just some personal project.<br />
Trello: [Open World Survival Game With AI](https://trello.com/b/LxoKPeSf/open-world-survival-game-with-ai)

## Tiles
The `res/tiles/` folder should contain tiles of the form `<id>_<name>.png`. The world generation currently uses the following id mappings:
    
| Tile ID | Tile Name |
|---------|-----------|
| 0       | Sand      |
| 1       | Grass     |
| 2       | Snow      |

## Entities
The `res/entities/` folder should contain files named `<anything>.entity` containing the entity properties. Such a file contains entity properties, currently:

    - Entity ID
    - Entity name
    - Texture filename
    - Scale (the factor with which the texture should be scaled)
    - Hitbox(es) for when other entities move (in the future)
    - Hitbox(es) for when tools are used in the vicinity (in the furture)
    - Suitable tools for harvesting this entity (in the future)

The folder then also contains a folder named `textures/` containing the texture files referenced by the entity files. The application currently uses the following ids:

| Entity Library ID | Entity Name |
|-------------------|-------------|
| 0                 | Cactus      |
| 1                 | Pine Tree   |
| 2                 | Jungle Tree |