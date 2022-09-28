import math
import os
import pickle
import random as rnd

import pygame

from entity import Entity, Player

"""
How to implement structures with entrances:
    - New list in world called structures.
    - Structures have structure_id, structure_name, texture_filename, 
        entrance_hitbox, collision_hitboxes. Structures also have their own 
        world specified by an id.
    - When a structure is added, a destination world id must be specified for 
        its entrance, this is the world the entrance leads to.
    - When a structure is added, its collision hitboxes are added to the 
        collision_hitboxes list, and its entrance is added to the entrances 
        list.
    - Question: how is the destination world specified?
        - Choose ground type
        - Add list of entity tuples with entity id, position (can be none for 
            random). (this will probably require me to separate the types of 
            entities in the future to make sure the dynamic entities can move.)
        - Add list of structures with structure id, position, destination.
    Maybe another world class with different generate functions, or add 
        arguments to this world class.
"""

class World:
    
    def __init__(self, world_name, map_size, load_existing=False):
        # Set world name (used for saving).
        self.world_name = world_name
        
        # Check if the world name is valid.
        self.verify_world_name(world_name)
        
        # Set map size.
        self.map_size = map_size
        
        # Check if the map size is not negative or zero.
        if not map_size >= 1:
            raise ValueError("Map size must be greater than or equal to 1.")
        if not isinstance(map_size, int):
            raise TypeError("Map size must be an integer.")
        
        # Load existing world or generate new world.
        if load_existing:
            result = self.deserialize("saves", world_name)
            if not result:
                raise Exception("An error occured while loading the world.")
        else:
            result = self.generate(map_size=map_size, num_of_entities=10)
            if not result:
                raise Exception("An error occured while generating the world.")
    
    def verify_world_name(self, world_name):
        # Check if the world name is a string.
        if not isinstance(world_name, str):
            raise ValueError("World name must be a string.")
        
        # Check if the world name is longer than 0 characters but no longer 
        # than 250 characters.
        if not (len(world_name) > 0 and len(world_name) <= 250):
            raise ValueError("World name must contain at least 1 character " \
                "and at most 250.")
        
        # Check if the world name only contains alphabetical characters and 
        # numbers.
        if not world_name.isalnum():
            raise ValueError("World name can only contain alphabetical " \
                "characters and numbers.")
        
        # Check if the world name start with an alphabetical character.
        if not world_name[0].isalpha():
            raise ValueError("World name must start with an alphabetical " \
                "character.")
    
    def add_entity(self, entity):
        # Determine position in the list for correct rendering (top to bottom).
        entity_added = False
        for index, e in enumerate(self.entities):
            if entity.position[1] > e.position[1]:
                self.entities.insert(index, entity)
                entity_added = True
                break
        
        # Add entity to the end of the list if it's the bottom most entity.
        if not entity_added:
            self.entities.append(entity)
    
    def generate(self, map_size, num_of_entities):
        """
        Generates tiles, entities, and a player.
        """
        try:
            # Generate map tiles.
            self.tiles = self.generate_world_tiles(map_size)
            
            # Generate static entities.
            self.entities = self.generate_world_entities(map_size, \
                tile_size=64, num_of_entities=num_of_entities)
            
            # Create player.
            self.player = Player(position=(0, 0), name="Harry")
            
            return True
        except Exception as e:
            print(f"Generating of the world with name '{self.world_name}' " \
                f"failed: {e}.")
            return False
    
    def generate_world_tiles(self, map_size):
        """
        Generates 2d tiles list of size map_size by map_size.
        """
        # Initialize tile list.
        tiles = []
        
        # Add tile rows based on latitude.
        for latitude in range(0, map_size):
            # Sine based sample method.
            sample = math.sin(math.pi * latitude / map_size)
            
            # Saw tooth sample method (currently used).
            half_map_size = map_size / 2
            sample = 1 - (abs(latitude - half_map_size) / half_map_size)
            
            # Snow biome.
            if sample < 0.2:
                row = [2] * map_size
                tiles.append(row)
            # Tropical biome.
            elif sample < 0.8:
                row = [1] * map_size
                tiles.append(row)
            # Sand biome.
            else:
                row = [0] * map_size
                tiles.append(row)
        
        # Return tiles.
        return tiles
    
    def generate_world_entities(self, map_size, tile_size, \
        num_of_entities=100):
        """
        Generates entities list of size num_of_entities based on tile ids.
        """
        # Initialize entities list.
        entities = []
        
        # Generate unique random positions.
        positions = []
        for _ in range(num_of_entities):
            if map_size <= 3:
                rand_min = 0
                rand_max = tile_size * map_size
            else:
                rand_min = tile_size * 1
                rand_max = (map_size - 1) * tile_size
            x = rnd.randint(rand_min, rand_max)
            y = rnd.randint(rand_min, rand_max)
            while (x, y) in positions:
                x = rnd.randint(rand_min, rand_max)
                y = rnd.randint(rand_min, rand_max)
            positions.append((x, y))
        
        # Determine vegetation type and spawn vegetation.
        for position in positions:
            # Adjust position so (0, 0) is at the center of the world.
            position_shifted = [0, 0]
            position_shifted[0] = position[0] - (map_size / 2 * tile_size)
            position_shifted[1] = position[1] - (map_size / 2 * tile_size)
            
            # Get tile id of the base tile.
            map_x = int(position[0] / tile_size)
            map_y = int(position[1] / tile_size)
            # Increment tile position y if able to, this ensures correct 
            # entities on the tiles. The last couple rows are snow anyway so 
            # this won't produce weird things.
            if map_y < len(self.tiles) - 1:
                map_y += 1
            tile_id = self.tiles[map_y][map_x]
            
            # Snow biome.
            if tile_id == 2:
                entity = Entity(1, position_shifted)
            # Tropical biome.
            elif tile_id == 1:
                entity = Entity(2, position_shifted)
            # Sand biome.
            elif tile_id == 0:
                entity = Entity(0, position_shifted)
            
            # Add entity to list.
            # Determine position in the list for correct rendering (top to bottom).
            entity_added = False
            for index, e in enumerate(entities):
                if entity.position[1] > e.position[1]:
                    entities.insert(index, entity)
                    entity_added = True
                    break
            
            # Add entity to the end of the list if it's the bottom most entity.
            if not entity_added:
                entities.append(entity)
        
        # Return entities.
        return entities
    
    def update_entities(self, delta_time):
        # Update player.
        self.player.update(delta_time)
    
    def render_tiles(self, display, camera, window_dimensions, tile_textures):
        # Set tile size (for debug purposes).
        tile_size = 64
        render_outlines = False
        
        # Keep track of the number of tiles rendered.
        rendered_tiles = 0
        
        # Render tiles.
        for index, row in enumerate(self.tiles):
            tile_y = -tile_size * (index - self.map_size // 2) \
                + window_dimensions[1] // 2 - camera[1]
            if tile_y < -tile_size or tile_y > window_dimensions[1]:
                continue
            for index2, tile_id in enumerate(row):
                tile_x = tile_size * (index2 - self.map_size // 2) \
                    + window_dimensions[0] // 2 - camera[0]
                if tile_x < -tile_size or tile_x > window_dimensions[0]:
                    continue
                display.blit(tile_textures[tile_id][1], (tile_x, tile_y))
                if render_outlines:
                    pygame.draw.rect(display, (0, 0, 0), \
                        (tile_x, tile_y, tile_size, tile_size), 1)
                rendered_tiles += 1
        
        # Return the number of tiles rendered.
        return rendered_tiles
    
    def render_entities(self, display, camera, window_dimensions, \
        entity_library):
        # Keep track of the number of entities rendered.
        rendered_entities = 0
        
        # Construct list of moveable entities.
        moveable_entities = [self.player]
        
        # Render entities.
        for entity in self.entities:
            # Check if a moveable entity needs to be rendered.
            success = False
            if not len(moveable_entities) == 0 \
                and moveable_entities[0].position[1] > entity.position[1]:
                success = moveable_entities[0].render(display, camera, \
                    window_dimensions, entity_library)
                del moveable_entities[0]
            if success:
                rendered_entities += 1
            
            # Render entity.
            success = entity.render(display, camera, window_dimensions, \
                entity_library)
            if success:
                rendered_entities += 1
        
        # Render remaining moveable entities that are below all static entities.
        for entity in moveable_entities:
            entity.render(display, camera, window_dimensions, entity_library)
        
        # Return the number of entities rendered.
        return rendered_entities
    
    def serialize(self, path):
        # Create save folder if it does not yet exist.
        save_folder = os.path.join(path, self.world_name)
        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)
        
        # Pickle the world.
        with open(os.path.join(save_folder, "save.pickle"), "wb") as file:
            pickle.dump(self, file)
    
    def deserialize(self, path, world_name):
        # Construct save path.
        save_folder = os.path.join(path, world_name)
        save_path = os.path.join(save_folder, "save.pickle")
        
        # Check if the save exists.
        if not os.path.exists(save_path):
            print(f"No save file exists for world with name '{world_name}'.")
            return False
        
        try:
            # Load the world.
            with open(save_path, "rb") as file:
                loaded_world = pickle.load(file)
        
            # Set member variables.
            self.world_name = world_name
            self.map_size = loaded_world.map_size
            self.tiles = loaded_world.tiles
            self.entities = loaded_world.entities
            self.player = loaded_world.player
            return True
        except Exception as e:
            print(f"Loading of save with name '{world_name}' failed: {e}.")
            return False