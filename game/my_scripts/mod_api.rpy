# mod_api.rpy
# ---------------------------------------------------------------------------
# Generic registration helper shared by every content registry in the game
# (locations, events, character templates, minigames, combat systems...).
#
# Mods should never edit the base game's files directly. Instead, a mod
# drops its own .rpy file(s) anywhere under game/ (game/mods/<mod_name>/ is
# the recommended convention - not required, Ren'Py loads any .rpy under
# game/ automatically) and calls the relevant register_*() function from
# its own init python block.
# ---------------------------------------------------------------------------

init -12 python:

    def _register(registry, key, value, kind, override=False):
        """
        Adds `value` to `registry` under `key`. Warns instead of silently
        overwriting when the key already exists, unless override=True is
        explicitly passed - this is what protects against two mods (or a
        mod and the base game) accidentally colliding on the same id.
        """
        if key in registry and not override:
            renpy.log(
                "[MOD WARNING] {} '{}' is already registered and was NOT "
                "overridden. Pass override=True if this is intentional.".format(kind, key)
            )
            return False
        registry[key] = value
        return True
