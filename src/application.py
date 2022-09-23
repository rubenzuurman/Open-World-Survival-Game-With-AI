import entity
import renderer
import world

def main():
    # Create world.
    w = world.World(world_name="world1", map_size=500, load_existing=False)
    
    # Start renderer.
    renderer.start(world=w, window_dimensions=(1920, 1080))

if __name__ == "__main__":
    main()