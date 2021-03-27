from store import turret, camera

turret_1 = turret()
camera_1 = camera(0)

if __name__ == "__main__":
    try:
        camera_1.start_video(turret_1)

    except KeyboardInterrupt:
        turret_1.cleanup()