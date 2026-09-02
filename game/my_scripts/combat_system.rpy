# combat_system.rpy
# ---------------------------------------------------------------------------
# A Darkest Dungeon-style combat system: registers itself into the generic
# COMBAT_SYSTEMS registry (see combat.rpy) under the id "darkest_dungeon".
# Written the same way a mod would write its own combat system - this file
# never touches combat.rpy, it only calls register_combat_system().
#
# DESIGN DECISIONS BAKED INTO THIS SKELETON:
#
#   - No death, only KO: a defeated unit is marked is_ko, never removed.
#     Combat ends as soon as one side has zero non-KO units left.
#   - No fleeing mid-combat: check_combat_end() is deliberately binary
#     ("victory" / "defeat" / None). Fleeing a dungeon between fights, and
#     what happens narratively on defeat (captured, robbed, a hostage left
#     behind...), are both handled by whatever event called start_combat(),
#     not by this file.
#   - Turn order is recomputed after EVERY action, not once per round. This
#     is what lets a mid-round effect (haste, sleep, stun...) immediately
#     change who acts next, instead of only applying next round.
#   - Each formation has exactly 4 fixed slots. A slot can be empty (None)
#     - which is deliberate: empty slots are a tactical element (attacks
#     can target/skip them), not just "no unit here". Slot content is kept
#     loosely typed on purpose, as an extension point for things that
#     aren't full combatants later (a captured ally, an item...) - not
#     built out yet, just left room for.
#
# STILL OUT OF SCOPE (by design, for a later pass):
#   stats (HP, speed, ...), attacks/targeting, status effects, player input
#   UI, enemy AI, non-character slot occupants.
# ---------------------------------------------------------------------------

init -9 python:

    class CombatUnit(object):
        """
        One combatant in the fight. Wraps whatever "source" it represents
        (a GameCharacter for the player side; enemies aren't modeled yet,
        so their source is just a placeholder for now) plus state that only
        exists for the duration of this combat.
        """

        def __init__(self, source, is_player_side):
            self.source = source            # GameCharacter (player side) or TBD enemy representation
            self.is_player_side = is_player_side
            self.is_ko = False
            # HP, speed, status effects, etc. all still TBD.

        @property
        def display_name(self):
            return getattr(self.source, "display_name", str(self.source))


    class CombatFormation(object):
        """
        One side's line, exactly 4 fixed slots (index 0 = frontline). A
        slot holds either None (empty) or a CombatUnit.
        """

        SIZE = 4

        def __init__(self, slots=None):
            self.slots = slots if slots is not None else [None] * CombatFormation.SIZE

        @classmethod
        def from_sources(cls, sources, is_player_side):
            """Builds a formation from a list of up to 4 sources (e.g. GameCharacter
            instances), placed front to back. Remaining slots stay empty."""
            formation = cls()
            for i, source in enumerate(sources[:cls.SIZE]):
                formation.slots[i] = CombatUnit(source, is_player_side)
            return formation

        def units(self):
            """Every occupied slot, in slot order. Empty slots are skipped."""
            return [unit for unit in self.slots if unit is not None]


    class CombatEncounter(object):
        """Everything the combat loop needs to track for a single fight."""

        def __init__(self, player_formation, enemy_formation):
            self.player_formation = player_formation
            self.enemy_formation = enemy_formation
            self.acted_this_round = set()   # CombatUnit instances that already acted this round
            self.outcome = None             # None while ongoing, else "victory" / "defeat"


    def build_encounter(encounter_data):
        """
        encounter_data (dict, may be None) is expected to provide:
            - "party": list of GameCharacter instances entering the fight
                    (up to 4 - which recruits go in is decided by whoever
                    calls start_combat(), e.g. a team-selection screen).
                    Defaults to just [MC] if not provided.
            - "enemies": list of enemy sources (up to 4). Enemy representation
                    isn't designed yet - placeholders only for now.
        """
        encounter_data = encounter_data or {}
        party = encounter_data.get("party", [MC])
        enemies = encounter_data.get("enemies", [])

        return CombatEncounter(
            player_formation=CombatFormation.from_sources(party, is_player_side=True),
            enemy_formation=CombatFormation.from_sources(enemies, is_player_side=False),
        )


    def check_combat_end(encounter):
        """Returns "victory", "defeat", or None if the fight goes on."""
        player_up = any(not unit.is_ko for unit in encounter.player_formation.units())
        enemy_up = any(not unit.is_ko for unit in encounter.enemy_formation.units())

        if not player_up:
            return "defeat"
        if not enemy_up:
            return "victory"
        return None


    def compute_remaining_turn_order(encounter):
        """
        Every unit that hasn't acted yet this round and isn't KO'd,
        recomputed fresh every time a turn ends (not once per round) so
        mid-round speed/status changes take effect immediately.
        """
        candidates = [
            unit
            for unit in (encounter.player_formation.units() + encounter.enemy_formation.units())
            if not unit.is_ko and unit not in encounter.acted_this_round
        ]
        # candidates.sort(key=lambda u: u.speed, reverse=True)  # once speed exists
        return candidates


init -5 python:
    register_combat_system("darkest_dungeon", "combat_darkest_dungeon")


# --- Combat loop -------------------------------------------------------

label combat_darkest_dungeon(encounter_data=None):

    python:
        encounter = build_encounter(encounter_data)

    jump combat_round_loop


label combat_round_loop:

    python:
        encounter.acted_this_round = set()

    jump combat_turn_loop


label combat_turn_loop:

    python:
        remaining = compute_remaining_turn_order(encounter)
        current_unit = remaining[0] if remaining else None

    if current_unit is None:
        # Everyone eligible has acted this round - start a new one.
        jump combat_round_loop

    python:
        actor_name = current_unit.display_name

    # -- Placeholder turn resolution. Real player input / enemy AI /
    #    attacks / status effects are all still TBD - for now a unit's
    #    turn does nothing, just enough to exercise and test the loop.
    "// Placeholder turn: [actor_name] would act now."

    python:
        encounter.acted_this_round.add(current_unit)
        encounter.outcome = check_combat_end(encounter)

    if encounter.outcome is not None:
        jump combat_resolve

    jump combat_turn_loop


label combat_resolve:
    return encounter.outcome
