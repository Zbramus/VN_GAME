# time_system.rpy
# ---------------------------------------------------------------------------
# Tracks the in-game calendar (date) and the current time-of-day slot.
# The day is split into 5 slots. Advancing past the last slot rolls the
# date forward to the next day and resets the slot back to Morning.
# ---------------------------------------------------------------------------

init -10 python:
    import datetime

    # Ordered list of time slots for a single day.
    TIME_SLOT_NAMES = ["Morning", "Midday", "Late Afternoon", "Evening", "Night"]

    # Convenience index constants, e.g. SLOT_MORNING == 0
    SLOT_MORNING, SLOT_MIDDAY, SLOT_LATE_AFTERNOON, SLOT_EVENING, SLOT_NIGHT = range(len(TIME_SLOT_NAMES))

    class GameTime(object):
        """
        Holds the current in-game date and time-of-day slot.
        Uses a plain datetime.date internally, which is safe to save/rollback.
        """

        def __init__(self, year, month, day, slot_index=0):
            self.date = datetime.date(year, month, day)
            self.slot_index = slot_index

        @property
        def slot_name(self):
            return TIME_SLOT_NAMES[self.slot_index]

        @property
        def weekday_name(self):
            return self.date.strftime("%A")

        def advance_slot(self):
            """
            Moves to the next time slot. If we were on the last slot of the
            day (Night), wraps back to Morning and moves the date forward
            by one day.
            """
            self.slot_index += 1
            if self.slot_index >= len(TIME_SLOT_NAMES):
                self.slot_index = 0
                self.date += datetime.timedelta(days=1)

        def __str__(self):
            return "{} {} - {}".format(self.weekday_name, self.date.isoformat(), self.slot_name)


# The story begins on Saturday, July 4th 2026, in the morning.
default game_time = GameTime(2026, 7, 4, SLOT_MORNING)