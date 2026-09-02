# locations.rpy
# ---------------------------------------------------------------------------
# Defines the Location class and the registry of every place characters can
# be in (real world or in-game). Events can filter on location, and
# characters track which location they are currently in.
# ---------------------------------------------------------------------------

init -10 python:

    class Location(object):
        """
        A single place in the world. Purely data for now: no behaviour,
        just enough to let events and characters reference a place
        consistently.
        """

        def __init__(self, location_id, display_name, background, description="", tags=None):
            self.location_id = location_id      # unique key, used everywhere else (e.g. MC.location)
            self.display_name = display_name    # shown to the player
            self.background = background        # image name used in `scene`/`show` statements
            self.description = description      # placeholder flavor text
            self.tags = tags or []              # e.g. ["real_world"], ["in_game"], ["indoor"]

        def __str__(self):
            return self.display_name


    def get_location(location_id):
        """Looks up a Location by id. Returns None if it doesn't exist."""
        return LOCATIONS.get(location_id)


    def current_location():
        """Shortcut for the Location object the MC is currently in."""
        return get_location(MC.location)


# Placeholder registry of locations. Add more as the map grows.
define LOCATIONS = {
    "starting_apartment": Location(
        "starting_apartment",
        "Your Apartment",
        "bg_placeholder_apartment",
        description="Placeholder - the MC's apartment in the real world.",
        tags=["real_world", "indoor"],
    ),
    "downtown_street": Location(
        "downtown_street",
        "Downtown Street",
        "bg_placeholder_street",
        description="Placeholder - a street in the MC's city.",
        tags=["real_world", "outdoor"],
    ),
    "guild_hall": Location(
        "guild_hall",
        "Guild Hall",
        "bg_placeholder_guildhall",
        description="Placeholder - the guild's headquarters inside the game.",
        tags=["in_game", "indoor"],
    ),
}