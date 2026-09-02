# minigames.rpy
# ---------------------------------------------------------------------------
# Registry of "work session" mini-games - the compressed sessions played
# between Morning->Midday and Midday->LateAfternoon, standing in for the
# MC's (or a recruit's) job. See MC.job_minigame (characters.rpy) and
# run_work_session() (main_loop.rpy).
#
# No real minigame is designed yet - this file just puts the plug-n-play
# socket in place so the base game and mods can register one later without
# touching main_loop.rpy.
# ---------------------------------------------------------------------------

init -11 python:
    MINIGAMES = {}


init -10 python:

    def register_minigame(minigame_id, label, override=False):
        """`label` is the name of a Ren'Py label that plays out the minigame."""
        return _register(MINIGAMES, minigame_id, label, "minigame", override)


init -9 python:
    # Built-in fallback: always present, does nothing. Used whenever a
    # character has no job, or an unregistered minigame id is requested.
    register_minigame("none", "minigame_none")


label minigame_none:
    return
