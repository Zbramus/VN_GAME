# mod_template.rpy
# ---------------------------------------------------------------------------
# HOW TO MOD THIS GAME
# ---------------------------------------------------------------------------
#
# This file is documentation, not a working mod. Every example below is
# commented out on purpose - copy the bits you need into your OWN .rpy
# file, don't edit this one or any base-game file.
#
# THE RULES, IN SHORT
#
#   1. Never edit a base-game .rpy file. Everything moddable goes through
#      a register_*() function instead.
#   2. Drop your own .rpy file(s) anywhere under game/ - Ren'Py finds and
#      loads every .rpy under game/ automatically, no special install step.
#      A subfolder per mod (game/mods/<your_mod_name>/...) is a friendly
#      convention, not a requirement.
#   3. Prefix every id you create (location ids, event ids, template ids,
#      minigame ids, combat system ids) with your own mod's short name,
#      e.g. "mymod_tavern", "mymod_intro_letter". This is what stops two
#      mods (or your mod and the base game) from ever colliding.
#   4. Put all your registrations inside an `init` block with a POSITIVE
#      priority (10 is a safe default - see examples below). The base
#      game's own registries are all set up at negative priorities, so
#      anything positive is guaranteed to run after they're ready.
#   5. Every register_*() function takes an `override=True` argument. Leave
#      it out (or False) unless you deliberately want to replace something
#      that's already registered - the game will log a warning instead of
#      silently overwriting it, so accidental collisions are easy to spot
#      (check the game's log.txt).
#
# ---------------------------------------------------------------------------


# init 10 python:
#
#     pass  # <- replace with whichever examples below you need


# ---------------------------------------------------------------------------
# 1. LOCATIONS
# ---------------------------------------------------------------------------
# A Location is a place the MC (or any character) can be in. `tags` is how
# the game tells the real world apart from the in-game VR world - use
# "real_world" or "in_game" (plus anything else you like, e.g. "indoor",
# "bar" - tags are free-form, events and helper functions can filter on
# them however they want).
#
# Location(location_id, display_name, background, description="", tags=None)

# init 10 python:
#
#     register_location(Location(
#         "mymod_seedy_tavern",
#         "The Rusty Anchor",
#         "bg_mymod_tavern",                 # image name, matches your `scene`/`show` assets
#         description="A dockside tavern that's seen better days.",
#         tags=["real_world", "indoor", "bar"],
#     ))


# ---------------------------------------------------------------------------
# 2. EVENTS
# ---------------------------------------------------------------------------
# A GameEvent describes WHEN it can trigger and WHERE to jump to play it.
#
# GameEvent(
#     event_id, label,
#     locations=None,      # list of location_id, or None = any location
#     slots=None,           # list of SLOT_MORNING / SLOT_MIDDAY / SLOT_LATE_AFTERNOON /
#                            #   SLOT_EVENING / SLOT_NIGHT, or None = any slot
#     condition=None,       # optional callable() -> bool for anything else (stats, flags...)
#     priority=100,         # lower number = checked/offered first
#     repeatable=False,     # False = can only ever fire once per playthrough
#     event_type="proposal",# "instant" (fires automatically) or "proposal" (player picks it from a menu)
#     menu_text=None,       # text shown in the menu for "proposal" events (defaults to the label name)
# )
#
# The label itself is a normal Ren'Py label - write whatever scene you want
# in it, it just needs to `return` at the end.

# init 10 python:
#
#     # An "instant" event: fires on its own the moment its conditions are
#     # met, no player choice involved.
#     register_event(GameEvent(
#         "mymod_letter_arrives",
#         "event_mymod_letter_arrives",
#         locations=["starting_apartment"],
#         slots=[SLOT_MORNING],
#         condition=lambda: "mymod_quest_started" in consumed_once_events,
#         priority=10,
#         repeatable=False,
#         event_type="instant",
#     ))
#
#     # A "proposal" event: shows up as a choice in the main loop's menu
#     # whenever its conditions are met.
#     register_event(GameEvent(
#         "mymod_visit_tavern",
#         "event_mymod_visit_tavern",
#         locations=["downtown_street"],
#         slots=None,
#         priority=60,
#         repeatable=True,
#         event_type="proposal",
#         menu_text="Head to the Rusty Anchor",
#     ))
#
#
# label event_mymod_letter_arrives:
#     "// Placeholder event: mymod_letter_arrives"
#     "A letter slides under the door."
#     return
#
# label event_mymod_visit_tavern:
#     "// Placeholder event: mymod_visit_tavern"
#     $ MC.location = "mymod_seedy_tavern"
#     "The MC steps into the tavern."
#     return


# ---------------------------------------------------------------------------
# 3. RECRUITABLE CHARACTERS
# ---------------------------------------------------------------------------
# You don't register a character directly - you register a TEMPLATE, which
# is just a zero-argument function that builds and returns a brand new
# GameCharacter. That's what lets the same template be recruited more than
# once (or reused across playthroughs) without every recruit sharing the
# same object.
#
# GameCharacter(display_name, real_sprite_tag, game_sprite_tag,
#               location="unknown", mood="neutral", color=None, **character_kwargs)
#
# register_character_template(template_id, factory, override=False)
#
# Once registered, call recruit_character(template_id) from anywhere (e.g.
# from inside one of your event labels) to actually add them to the roster.

# init 10 python:
#
#     def _make_mymod_dockhand():
#         return GameCharacter(
#             "Dockhand",
#             "mymod_dockhand_real",   # real_sprite_tag
#             "mymod_dockhand_hero",   # game_sprite_tag
#             location="mymod_seedy_tavern",
#             mood="neutral",
#             color="#ffcc88",
#         )
#
#     register_character_template("mymod_dockhand", _make_mymod_dockhand)
#
#
# label event_mymod_recruit_dockhand:
#     $ recruit_character("mymod_dockhand")
#     "// Placeholder event: mymod_recruit_dockhand"
#     "The dockhand joins your guild."
#     return


# ---------------------------------------------------------------------------
# 4. MINIGAMES (work sessions)
# ---------------------------------------------------------------------------
# A minigame is just a Ren'Py label, registered under an id. Assign that id
# to a character's `job_minigame` attribute (e.g. MC.job_minigame) and it
# will be called automatically by the main loop's work session hook,
# between Morning->Midday and Midday->LateAfternoon.
#
# register_minigame(minigame_id, label, override=False)

# init 10 python:
#
#     register_minigame("mymod_bartending", "minigame_mymod_bartending")
#
#
# label minigame_mymod_bartending:
#     "// Placeholder minigame: mymod_bartending"
#     "This is where the actual minigame would play out."
#     return
#
#
# label event_mymod_take_bartending_job:
#     $ MC.job_minigame = "mymod_bartending"
#     "// Placeholder event: mymod_take_bartending_job"
#     "The MC starts working as a bartender."
#     return


# ---------------------------------------------------------------------------
# 5. COMBAT SYSTEMS
# ---------------------------------------------------------------------------
# Only one combat system is active at a time. Registering a new one doesn't
# switch the game to it automatically - you also need to set
# active_combat_system, typically from inside one of your own event labels
# (e.g. when the story reaches the point your system should take over).
#
# register_combat_system(system_id, label, override=False)
# start_combat(encounter_data=None)  # call this to actually trigger a fight

# init 10 python:
#
#     register_combat_system("mymod_card_combat", "combat_mymod_card_combat")
#
#
# label combat_mymod_card_combat(encounter_data=None):
#     "// Placeholder combat system: mymod_card_combat"
#     "This is where the actual combat system would play out."
#     return
#
#
# label event_mymod_start_first_fight:
#     $ active_combat_system = "mymod_card_combat"
#     $ start_combat({"enemy": "placeholder_goblin"})
#     return


# ---------------------------------------------------------------------------
# TESTING YOUR MOD
# ---------------------------------------------------------------------------
# - Launch the game with your file in place. If any of your register_*()
#   calls collided with an existing id, you'll see a "[MOD WARNING]" line
#   in the game's log.txt - fix the id (don't just pass override=True
#   unless you actually mean to replace the base game's content).
# - "instant" events fire on their own the moment conditions are met - if
#   yours never seems to trigger, double-check locations/slots/condition.
# - "proposal" events show up in the main loop's menu - if yours is
#   missing, same checklist, plus make sure event_type="proposal".
