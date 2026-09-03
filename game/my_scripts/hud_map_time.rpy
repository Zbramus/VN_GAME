## ============================================================================
## À COLLER DANS screens.rpy, juste après le bloc du quick_menu
## (après le "config.overlay_screens.append("quick_menu")" et les styles
## quick_button / quick_button_text, avant "## Main and Game Menu Screens")
## ============================================================================

################################################################################
## HUD — Map & Time Period
################################################################################
## Deux boutons superposés en haut à droite de l'écran :
##   - map          -> ouvre le menu de voyage (pour l'instant un écran TODO)
##   - time_period   -> affiche le créneau actuel, un clic "épingle" le tooltip
##                      de date jusqu'au prochain clic

init python:
    config.overlay_screens.append("hud_top_right")

# TIME_SLOT_NAMES (time_system.rpy) ne correspond pas 1:1 aux noms de fichiers
# que tu as poussés (ex: "Late Afternoon" -> "Afternoon_idle.png",
# "Morning" -> "Morning_mini_idle.png"). Cette table fait la conversion.
define TIME_SLOT_ICON_PREFIX = {
    "Morning": "Morning_mini",
    "Midday": "Midday",
    "Late Afternoon": "Afternoon",
    "Evening": "Evening",
    "Night": "Night",
}

# Fonds 9-slice, mesurés directement sur tes PNG (bords transparents/alpha) :
#   Tooltip_left.png (250x71, translucide) : arrondi à gauche, plat à droite
#     (le bord droit vient se glisser sous le bouton qu'il commente)
#   Frame_mini_white.png (146x35, blanc opaque) : pilule symétrique
define hud_tooltip_bg = Frame("gui/button/Tooltip_left.png", 21, 4, 4, 4, tile=False)
define hud_label_bg   = Frame("gui/button/Frame_mini_white.png", 14, 4, 14, 4, tile=False)

# Réglages de position/recouvrement — à ajuster visuellement en jeu, ce sont
# des points de départ raisonnables, pas des valeurs mesurées.
define hud_icon_size       = 71
define hud_tooltip_overlap = 12   # de combien le tooltip se glisse SOUS le bouton
define hud_label_yoffset   = 50   # décalage vertical de la pastille de nom sous l'icône


screen hud_top_right():

    zorder 90

    default map_hovering = False
    default tp_hovering  = False
    default tp_pinned    = False

    python:
        tp_icon_prefix = TIME_SLOT_ICON_PREFIX[game_time.slot_name]
        tp_date_text = "{}, {}".format(game_time.weekday_name, game_time.date.strftime("%d/%m/%Y"))

    vbox:
        xalign 1.0
        yalign 0.0
        xoffset -50
        yoffset 30
        spacing 20

        # ------------------------------------------------------------
        # Bouton Map
        # ------------------------------------------------------------
        fixed:
            xsize hud_icon_size + 260
            ysize hud_icon_size

            imagebutton:
                xalign 1.0
                idle "gui/button/quick_menu/map_idle.png"
                hover "gui/button/quick_menu/map_hover.png"
                insensitive "gui/button/quick_menu/map_insensitive.png"
                hovered SetScreenVariable("map_hovering", True)
                unhovered SetScreenVariable("map_hovering", False)
                action Show("travel_menu")

            if map_hovering:
                frame:
                    xanchor 1.0
                    xpos hud_icon_size + 260 - hud_icon_size + hud_tooltip_overlap
                    yalign 0.5
                    background hud_tooltip_bg
                    padding (24, 10, 24 + hud_tooltip_overlap, 10)

                    text _("Travel elsewhere") size 28 color "#3a2f4d" xalign 0.5 yalign 0.5

        # ------------------------------------------------------------
        # Bouton Time Period
        # ------------------------------------------------------------
        fixed:
            xsize hud_icon_size + 260
            ysize hud_icon_size + hud_label_yoffset

            imagebutton:
                xalign 1.0
                idle "gui/button/quick_menu/[tp_icon_prefix]_idle.png"
                hover "gui/button/quick_menu/[tp_icon_prefix]_hover.png"
                hovered SetScreenVariable("tp_hovering", True)
                unhovered SetScreenVariable("tp_hovering", False)
                action ToggleScreenVariable("tp_pinned")

            # Pastille de nom du créneau, toujours visible, sous l'icône
            frame:
                xalign 1.0
                yoffset hud_label_yoffset
                background hud_label_bg
                padding (18, 4, 18, 4)

                text game_time.slot_name size 22 color "#3a2f4d" xalign 0.5

            # Tooltip de date : visible au survol OU épinglé par un clic
            if tp_hovering or tp_pinned:
                frame:
                    xanchor 1.0
                    xpos hud_icon_size + 260 - hud_icon_size + hud_tooltip_overlap
                    yalign 0.0
                    ysize hud_icon_size
                    background hud_tooltip_bg
                    padding (24, 10, 24 + hud_tooltip_overlap, 10)

                    text tp_date_text size 28 color "#3a2f4d" xalign 0.5 yalign 0.5


################################################################################
## Travel Menu — PLACEHOLDER
################################################################################
## Remplace l'ancien choix "go elsewhere" du menu texte plat. Pour l'instant
## un simple panneau "TODO" en attendant la vraie carte cliquable.

screen travel_menu():

    modal True
    zorder 200

    # Fond assombri, cliquable pour fermer
    button:
        xfill True
        yfill True
        background "#000000aa"
        action Hide("travel_menu")

    frame:
        style "frame"   ## réutilise gui/frame.png, déjà en 9-slice (gui.frame_borders)
        xalign 0.5
        yalign 0.5
        xsize int(config.screen_width * 0.8)
        ysize int(config.screen_height * 0.8)

        text _("TODO") xalign 0.5 yalign 0.5 size 80 color "#3a2f4d"

        textbutton _("Fermer"):
            xalign 1.0
            yalign 0.0
            action Hide("travel_menu")
