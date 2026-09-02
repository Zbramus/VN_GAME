# main_loop.rpy
# ---------------------------------------------------------------------------
# The central game loop.
#
# Each pass:
#   1. Ask events.rpy for the best-matching available event.
#   2. If there is one, mark it as fired and call its label.
#   3. Jump back to the top and repeat.
#
# Nothing here advances time on its own - that only happens when an event
# (typically "free_time", see events.rpy) explicitly calls advance_time().
# That's what lets several events chain within the same time slot before
# the player/story decides to move on.
# ---------------------------------------------------------------------------

init python:

	def mark_event_fired(event):
        fired_this_slot_events.add(event.event_id)
        if not event.repeatable:
            consumed_once_events.add(event.event_id)

    def advance_time():
        """
        Ends the current time slot: advances the calendar and clears the
        per-slot event tracking so the next slot's events become available.
        Call this from an event label or a player choice.
        """
        game_time.advance_slot()
        fired_this_slot_events.clear()


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
