# combat.rpy
# ---------------------------------------------------------------------------
# Registry of combat systems. Only one is "active" at a time; start_combat()
# always dispatches to whichever system is currently active. A mod can
# therefore add a brand new combat system and switch the whole game over to
# it just by changing active_combat_system, without touching this file or
# main_loop.rpy.
#
# No real combat system is designed yet - this file just puts the plug-n-
# play socket in place.
# ---------------------------------------------------------------------------

init -11 python:
    COMBAT_SYSTEMS = {}


init -10 python:

    def register_combat_system(system_id, label, override=False):
        """`label` is the name of a Ren'Py label that plays out an encounter."""
        return _register(COMBAT_SYSTEMS, system_id, label, "combat system", override)

    def start_combat(encounter_data=None):
        """Call this to trigger combat; dispatches to the active combat system."""
        label = COMBAT_SYSTEMS.get(active_combat_system, COMBAT_SYSTEMS["none"])
        renpy.call(label, encounter_data)


init -9 python:
    # Built-in fallback: always present, does nothing. Used until a real
    # combat system is designed and registered.
    register_combat_system("none", "combat_none")


# Which registered combat system is currently in effect. Player/mod state,
# so it's a `default` rather than part of the init-time registry above.
default active_combat_system = "none"


label combat_none(encounter_data=None):
    return
