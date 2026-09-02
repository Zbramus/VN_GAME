# main_loop.rpy
# ---------------------------------------------------------------------------
# The central game loop.
#
# Each pass:
#   1. Check for an "instant" event - if one matches, it fires automatically
#      (no player choice), then we loop back and check again.
#   2. Otherwise, collect every available "proposal" event and let the
#      player pick one from a menu.
#
# Nothing advances time on its own - only an explicit call to advance_time()
# (from an event label or a menu choice, e.g. "wait") ends the current slot.
# That's what lets several events chain within the same time slot before
# the player/story decides to move on.
# ---------------------------------------------------------------------------

init python:

    def mark_event_fired(event):
        fired_this_slot_events.add(event.event_id)
        if not event.repeatable:
            consumed_once_events.add(event.event_id)

    def run_work_session(leaving_slot):
        """
        Placeholder for the compressed "work session" mini-game that happens
        between Morning->Midday and Midday->LateAfternoon (if the MC has a
        job). Design TBD - currently a no-op.
        """
        pass

    def advance_time():
        """
        Ends the current time slot: advances the calendar, clears the
        per-slot event tracking, and triggers the work session placeholder
        when relevant. Call this from an event label or a player choice.
        """
        leaving_slot = game_time.slot_index
        game_time.advance_slot()
        fired_this_slot_events.clear()

        if leaving_slot in (SLOT_MORNING, SLOT_MIDDAY):
            run_work_session(leaving_slot)


label main_loop:

    python:
        instant_event = get_instant_event()

    if instant_event is not None:
        $ mark_event_fired(instant_event)
        call expression instant_event.label from _call_expr_main_loop_instant
        jump main_loop

    python:
        proposal_events = get_proposal_events()

    if not proposal_events:
        # Safety net: nothing to propose, force time forward.
        $ advance_time()
        jump main_loop

    python:
        menu_items = [(event.menu_text, event) for event in proposal_events]
        chosen_event = renpy.display_menu(menu_items)
        mark_event_fired(chosen_event)

    call expression chosen_event.label from _call_expr_main_loop_proposal
    jump main_loop