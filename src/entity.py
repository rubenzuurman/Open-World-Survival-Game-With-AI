class Entity:
    
    NEXT_ENTITY_ID = 0
    
    def __init__(self, library_id, position):
        """
        The library id specifies the id in the entity library for retrieving 
        the texture, hitboxes, and other properties. The entity id is a 
        unique id per entity.
        """
        # Set member variables.
        self.entity_id = Entity.NEXT_ENTITY_ID
        Entity.NEXT_ENTITY_ID += 1
        self.library_id = library_id
        self.position = list(position)
    
    def update(self, entities):
        pass
    
    def render(self, display, camera, window_dimensions, entity_library):
        """
        Entities are rendered relative to the middlebottom of their texture.
        """
        # Get texture.
        texture = entity_library[self.library_id][1]
        
        # Calculate screen coordinates.
        screen_x = self.position[0] + window_dimensions[0] // 2 \
            - camera[0] - texture.get_width() / 2
        screen_y = -self.position[1] + window_dimensions[1] // 2 \
            - camera[1] - texture.get_height()
        
        # Check if the texture is on screen.
        if screen_x < -texture.get_width() or screen_x > window_dimensions[0]:
            return False
        if screen_y < -texture.get_height() or screen_y > window_dimensions[1]:
            return False
        
        # Render texture.
        display.blit(texture, (screen_x, screen_y))
        return True