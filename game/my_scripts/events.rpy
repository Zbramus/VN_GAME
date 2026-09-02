# events.rpy
# ---------------------------------------------------------------------------
# Defines the event system used by the main day loop (see main_loop.rpy).
#
# A GameEvent describes WHEN it is allowed to trigger (location, time slot,
# arbitrary condition) and WHERE to jump to play it out (a Ren'Py label).
#
# event_type distinguishes:
#   - "instant": fires automatically, no player choice involved.
#   - "proposal": added to the menu the main loop offers the player.
# ---------------------------------------------------------------------------

init -9 python:

    class GameEvent(object):

        def __init__(self, event_id, label, locations=None, slots=None, condition=None,
                     priority=100, repeatable=False, event_type="proposal", menu_text=None):

            self.event_id = event_id
            self.label = label
            self.locations = locations
            self.slots = slots
            self.condition = condition
            self.priority = priority
            self.repeatable = repeatable
            self.event_type = event_type        # "instant" or "proposal"
            self.menu_text = menu_text or label  # fallback if not provided

        def is_available(self):
            # One-shot events that already fired are permanently excluded.
            if not self.repeatable and self.event_id in consumed_once_events:
                return False

            # Anything already played during the current slot is skipped,
            # so a repeatable event can't loop forever within one slot.
            if self.event_id in fired_this_slot_events:
                return False

            if self.locations is not None and MC.location not in self.locations:
                return False

            if self.slots is not None and game_time.slot_index not in self.slots:
                return False

            if self.condition is not None and not self.condition():
                return False

            return True

    def get_instant_event():
        """Returns the best-matching available "instant" event, or None."""
        candidates = [e for e in EVENTS if e.event_type == "instant" and e.is_available()]
        if not candidates:
            return None
        candidates.sort(key=lambda e: e.priority)
        return candidates[0]

    def get_proposal_events():
        """Returns every available "proposal" event, sorted by priority."""
        candidates = [e for e in EVENTS if e.event_type == "proposal" and e.is_available()]
        candidates.sort(key=lambda e: e.priority)
        return candidates


# Tracks one-shot events that have already been played (ever), and events
# already played during the current time slot (reset on advance_time()).
default consumed_once_events = set()
default fired_this_slot_events = set()


init -5 python:
    # Placeholder event registry. Add real events here as they get written.
    EVENTS = [

        GameEvent(
            "intro_wake_up",
            "event_intro_wake_up",
            locations=["starting_apartment"],
            slots=[SLOT_MORNING],
            priority=0,
            repeatable=False,
            event_type="instant",
        ),

        GameEvent(
            "street_random_encounter",
            "event_street_random_encounter",
            locations=["downtown_street"],
            slots=None,
            condition=lambda: MC.fatigue < 5,
            priority=50,
            repeatable=True,
            event_type="proposal",
            menu_text="Look around downtown",
        ),

        # Always-available fallback so the player always has at least one
        # choice. Keep this last / lowest priority.
        GameEvent(
            "wait",
            "event_wait",
            locations=None,
            slots=None,
            priority=9999,
            repeatable=True,
            event_type="proposal",
            menu_text="Wait until the next part of the day",
        ),
    ]


# --- Placeholder event labels ----------------------------------------------

label event_intro_wake_up:
    "// Placeholder event: intro_wake_up"
    "This is where the wake-up / opening scene will go."
    return

label event_street_random_encounter:
    "// Placeholder event: street_random_encounter"
    "This is where a random street encounter would go."
    return

label event_wait:
    $ advance_time()
    return