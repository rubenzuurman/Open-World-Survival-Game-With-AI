import math
import random as rnd

import pygame

from entity import Entity

class World:
    
    def __init__(self, map_size):
        # Set map size.
        self.map_size = map_size
        
        # Generate map tiles.
        self.tiles = self.generate_world_tiles(map_size)
        
        # Generate entities.
        self.entities = self.generate_world_entities(map_size, tile_size=64, \
            number=200)
    
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
    
    def generate_world_tiles(self, map_size):
        """
        Generates 2d tiles list of size map_size by map_size.
        """
        # Initialize tile list.
        tiles = []
        
        # Add tile rows based on latitude.
        for latitude in range(1, map_size):
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
    
    def generate_world_entities(self, map_size, tile_size, number=100):
        """
        Generates entities list of size number based on tile ids.
        """
        # Initialize entities list.
        entities = []
        
        # Generate unique random positions.
        positions = []
        for _ in range(number):
            x = rnd.randint(tile_size * 2, (map_size - 2) * tile_size)
            y = rnd.randint(tile_size * 2, (map_size - 2) * tile_size)
            while (x, y) in positions:
                x = rnd.randint(tile_size * 2, (map_size - 2) * tile_size)
                y = rnd.randint(tile_size * 2, (map_size - 2) * tile_size)
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
        
        pygame.draw.circle(display, (0, 255, 100), \
            (window_dimensions[0] / 2, window_dimensions[1] / 2), 20)
        
        # Return the number of tiles rendered.
        return rendered_tiles
    
    def render_entities(self, display, camera, window_dimensions, \
        entity_library):
        # Keep track of the number of entities rendered.
        rendered_entities = 0
        
        # Render entities.
        for entity in self.entities:
            success = entity.render(display, camera, window_dimensions, \
                entity_library)
            if success:
                rendered_entities += 1
        
        # Return the number of entities rendered.
        return rendered_entities