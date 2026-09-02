init -25:
    
    # -------------------------------
    # Display options
    # -------------------------------

    define gui.use_side_image = False

    # -------------------------------
    # Gallery options
    # -------------------------------
    
    # Enables or disables the gallery button in the title screen.
    define gallery.enabled = False

    # Define the gallery items. See documentation for default format
    define gallery.items = []

    # If True, gallery items unlock based on variables rather than RenPy's default seen-image tracking. See documentation for format
    define gallery.variable_mode = False

    # If enabled, gallery items containing multiple images will only unlock when all images in the entry have been seen.
    define gallery.strict_multiple = False

    # -------------------------------
    # Music Room options
    # -------------------------------

    define music_room.enabled = False

    # If True, all tracks will be unlocked by default. If false, tracks will appear only once they are heard by the player. 
    define music_room.unlocked = True

    # ---- ! IMPORTANT ! ----
    # If you enable variable_mode, you MUST disable unlocked as well, and vice-versa. Otherwise it will be buggy and unexpected behavior will occur.
    # ---- ! IMPORTANT ! ----
    
    # If True, gallery items unlock based on variables. See documentation for format.
    define music_room.variable_mode = False
    define music_room.tracks = []