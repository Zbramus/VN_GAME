# characters.rpy
# ---------------------------------------------------------------------------
# GameCharacter wraps a standard Ren'Py Character so that a single variable
# (e.g. MC) can be used BOTH as a dialogue speaker:
#
#     MC "Hello, guys!"
#
# AND as a regular Python object carrying game data:
#
#     MC.location
#     MC.stats["charisma"]
#
# This works because Ren'Py dialogue statements just need the name on the
# left to be callable - it does not have to be a "real" Character object.
# ---------------------------------------------------------------------------

init -10 python:

class GameCharacter(object):

    def __init__(self, display_name, real_sprite_tag, game_sprite_tag,
                 location="unknown", mood="neutral", color=None, **character_kwargs):

        self.display_name = display_name
        self.real_sprite_tag = real_sprite_tag   # human appearance, shown in the real world
        self.game_sprite_tag = game_sprite_tag   # race/class appearance, shown in the VR game
        self.location = location

        self._mood = mood  # backing field for the "mood" property

        self.stats = {
            "strength": 0,
            "agility": 0,
            "intellect": 0,
            "charisma": 0,
            "resolve": 0,
        }
        self.fatigue = 0

        self._character = Character(display_name, color=color, **character_kwargs)

    def __call__(self, what, **kwargs):
        self._character(what, **kwargs)

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value):
        # Any validation/side effect goes here later if needed.
        self._mood = value

    @property
    def sprite(self):
        """
        Picks the right base sprite depending on which world the character
        is currently in (real world = human look, VR game = race/class look),
        then appends the current mood.
        """
        world = get_location(self.location).world if self.location in LOCATIONS else "real"
        base_tag = self.game_sprite_tag if world == "vr" else self.real_sprite_tag
        return "{} {}".format(base_tag, self.mood)


# The main character. Name/race/class placeholders - to be wired up to the
# character creation screen already in the project.
default MC = GameCharacter(
    "Main Character",
    "mc",
    race="Human",
    char_class="Adventurer",
    location="starting_apartment",
    mood="neutral",
    color="#c8ffc8",
)
