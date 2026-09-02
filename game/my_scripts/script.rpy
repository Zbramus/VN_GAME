# script.rpy
# ---------------------------------------------------------------------------
# Entry point of the game.
# ---------------------------------------------------------------------------

label start:

    python:
        MC.display_name = "Whatever the player typed"
        MC.mood = "neutral"
        MC.location = "starting_apartment"
        active_combat_system = "darkest_dungeon"

    jump main_loop
