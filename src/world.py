import math

class World:
    
    def __init__(self, map_size):
        # Generate map tiles.
        self.map_size = map_size
        self.tiles = self.generate_world_tiles(self.map_size)
    
    def generate_world_tiles(self, map_size):
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
    
    def render(self, display, camera, window_dimensions, tile_textures):
        # Set tile size (for debug purposes).
        tile_size = 64
        
        # Keep track over the number of tiles rendered.
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
                rendered_tiles += 1
        
        # Return the number of tiles rendered.
        return rendered_tiles