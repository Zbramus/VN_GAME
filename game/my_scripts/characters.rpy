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
#
# CHARACTER_TEMPLATES holds factories for recruitable characters (content,
# registered at init time by the base game and by mods). `roster` is the
# actual list of recruited GameCharacter instances - that's player state,
# so it's a `default` store variable instead.
# ---------------------------------------------------------------------------

init -11 python:
    CHARACTER_TEMPLATES = {}


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

            self.job_minigame = "none"  # id into MINIGAMES, see minigames.rpy / main_loop.rpy

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
            is currently in (real world = human look, VR game = race/class
            look), based on the current location's tags, then appends mood.
            """
            location = get_location(self.location)
            in_vr = location is not None and "in_game" in location.tags
            base_tag = self.game_sprite_tag if in_vr else self.real_sprite_tag
            return "{} {}".format(base_tag, self.mood)


    def register_character_template(template_id, factory, override=False):
        """
        `factory` is a zero-argument callable returning a new GameCharacter
        instance. Using a factory (rather than a ready-made instance) means
        every recruit gets their own independent object, instead of every
        recruit sharing the same one.
        """
        return _register(CHARACTER_TEMPLATES, template_id, factory, "character template", override)


    def recruit_character(template_id):
        """Creates a new character from a registered template and adds it to the roster."""
        factory = CHARACTER_TEMPLATES.get(template_id)
        if factory is None:
            renpy.log("[MOD ERROR] Unknown character template: {}".format(template_id))
            return None
        character = factory()
        roster.append(character)
        return character


# The main character. Name/sprites placeholders - to be wired up to the
# character creation screen already in the project.
default MC = GameCharacter(
    "Main Character",
    "mc_real",   # real_sprite_tag
    "mc_hero",   # game_sprite_tag
    location="starting_apartment",
    mood="neutral",
    color="#c8ffc8",
)

# Recruited party members (not counting MC). Empty at game start - filled
# via recruit_character() as the story progresses.
default roster = []
