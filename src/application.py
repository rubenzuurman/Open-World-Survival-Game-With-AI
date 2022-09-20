import entity
import renderer
import world

def main():
    # Create world.
    w = world.World(map_size=200)
    
    # Start renderer.
    renderer.start(world=w, window_dimensions=(1920, 1080))

if __name__ == "__main__":
    main()