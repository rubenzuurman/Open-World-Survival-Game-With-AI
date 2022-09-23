import json
import math
import os
import random as rnd
import time

import pygame

def load_tiles():
    # Initialize textures dict and file list.
    tile_textures = {}
    tiles_filenames = os.listdir("res/tiles/")
    
    # Load files into dict.
    for filename in tiles_filenames:
        tile_id, tile_name = filename.split(".")[0].split("_")
        texture = pygame.image.load(f"res/tiles/{filename}").convert_alpha()
        tile_textures[int(tile_id)] = [tile_name, texture]
    
    # Return dict.
    return tile_textures

def load_entities():
    # Initialize entities dict and file list.
    entity_library = {}
    entities_filenames = os.listdir("res/entities/")
    
    # Load files into dict.
    for filename in entities_filenames:
        # Skip non-entity files.
        if not filename.endswith(".entity"):
            continue
        
        # Load entity properties.
        with open(f"res/entities/{filename}", "r") as file:
            properties = json.loads(file.read())
        
        # Load entity id and name.
        entity_id   = properties["entity_id"]
        entity_name = properties["entity_name"]
        
        # Load entity texture.
        entity_texture_filename = properties["texture_filename"]
        entity_texture = \
            pygame.image.load(f"res/entities/{entity_texture_filename}")\
            .convert_alpha()
        
        # Scale texture.
        entity_scale = properties["scale"]
        entity_texture = pygame.transform.scale(entity_texture, \
            (entity_texture.get_width() * entity_scale, \
                entity_texture.get_height() * entity_scale))
        
        # Set entity library entry.
        entity_library[entity_id] = [entity_name, entity_texture]
    
    # Return dict.
    return entity_library

def render_text(display, text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, False, color)
    display.blit(text_surface, position)

def start(world, window_dimensions):
    # Initialize pygame.
    pygame.init()
    pygame.font.init()
    
    # Initialize font.
    font = pygame.font.SysFont("Courier New", 16)
    
    # Create display.
    display = pygame.display.set_mode(window_dimensions, \
        flags=pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Game - Version 0.0.3")
    window_middle = (window_dimensions[0] // 2, window_dimensions[1] // 2)
    
    # Load tiles.
    tile_textures = load_tiles()
    
    # Load entities.
    entity_library = load_entities()
    
    # Create clock.
    clock = pygame.time.Clock()
    fps = 60
    
    # Initialize camera position and velocity (in pixels per frame).
    camera = [0, 0]
    camera_velocity = 10
    
    # Initialize camera control keys [w, a, s, d, lshift].
    move_keys_pressed = [False, False, False, False, False]
    
    # Time keeping variable for world update.
    last_update = 0
    
    # Start main loop.
    running = True
    while running:
        # Handle events.
        for event in pygame.event.get():
            # Detect quit event.
            if event.type == pygame.QUIT:
                running = False
            
            # Detect keypresses.
            if event.type == pygame.KEYDOWN:
                # Detect escape keypress.
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_w:
                    move_keys_pressed[0] = True
                if event.key == pygame.K_a:
                    move_keys_pressed[1] = True
                if event.key == pygame.K_s:
                    move_keys_pressed[2] = True
                if event.key == pygame.K_d:
                    move_keys_pressed[3] = True
                
                if event.key == pygame.K_LSHIFT:
                    move_keys_pressed[4] = True
            
            # Detect keyreleases.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_keys_pressed[0] = False
                if event.key == pygame.K_a:
                    move_keys_pressed[1] = False
                if event.key == pygame.K_s:
                    move_keys_pressed[2] = False
                if event.key == pygame.K_d:
                    move_keys_pressed[3] = False
                
                if event.key == pygame.K_LSHIFT:
                    move_keys_pressed[4] = False
                
                if event.key == pygame.K_SPACE:
                    world.player.camera_locked = not world.player.camera_locked
        
        # Check if the camera is locked to the player.
        if world.player.camera_locked:
            # Get player velocity from input.
            player_velocity = 200
            player_vel_x = 0
            player_vel_y = 0
            if move_keys_pressed[0]:
                player_vel_y += player_velocity
            if move_keys_pressed[1]:
                player_vel_x -= player_velocity
            if move_keys_pressed[2]:
                player_vel_y -= player_velocity
            if move_keys_pressed[3]:
                player_vel_x += player_velocity
            
            # Set player velocity.
            world.player.set_velocity([player_vel_x, player_vel_y])
            
            # Set camera position to player position.
            camera = [world.player.position[0], -world.player.position[1]]
        else:
            # Update camera position.
            camera_velocity_x = 0
            camera_velocity_y = 0
            if move_keys_pressed[0]:
                camera_velocity_y -= camera_velocity
            if move_keys_pressed[1]:
                camera_velocity_x -= camera_velocity
            if move_keys_pressed[2]:
                camera_velocity_y += camera_velocity
            if move_keys_pressed[3]:
                camera_velocity_x += camera_velocity
            
            if move_keys_pressed[4]:
                camera[0] += camera_velocity_x * 4
                camera[1] += camera_velocity_y * 4
            else:
                camera[0] += camera_velocity_x
                camera[1] += camera_velocity_y
        
        # Calculate delta time.
        current_time = time.time_ns()
        if last_update == 0:
            last_update = current_time
            continue
        delta_time = (current_time - last_update) * 1e-9
        last_update = current_time
        
        # Update world.
        world.update_entities(delta_time)
        
        # Fill display with black.
        display.fill((0, 0, 0))
        
        # Render world.
        rendered_tiles = world.render_tiles(display, camera, \
            window_dimensions, tile_textures)
        loaded_tiles = world.map_size * world.map_size
        rendered_entities = world.render_entities(display, camera, \
            window_dimensions, entity_library)
        loaded_entities = len(world.entities)
        
        # Render debug text.
        render_text(display, f"Rendered tiles: {rendered_tiles}" \
            f"/{loaded_tiles}", (10, 10), font)
        render_text(display, f"Rendered entities: {rendered_entities}" \
            f"/{loaded_entities}", (10, 30), font)
        
        # Update display.
        pygame.display.flip()
        
        # Tick clock.
        clock.tick(fps)
    
    # Quit pygame.
    pygame.quit()
    
    # Save world.
    world.serialize("saves")