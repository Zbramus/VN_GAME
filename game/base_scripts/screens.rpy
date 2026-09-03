################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)
    xsize 439

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_idle_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who.upper() id "who"

        text what id "what"

    if gui.use_side_image:
        add "gui/empty_side.png" xpos 328 yanchor -573 ypos 27

    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small") and gui.use_side_image:
        add SideImage() xpos 328 yanchor -573 ypos 27

## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name")
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


# ============================================================
# QUICK MENU — hamburger cliquable + dropdown
# Remplace le screen "quick_menu" par défaut de screens.rpy
# ============================================================

# ------------------------------------------------------------
# 1) FOND 9-SLICE
# ------------------------------------------------------------
# quick_menu_background.png fait 168x310px, avec un dégradé
# d'ombre transparent tout autour du rectangle violet arrondi.
define qm_border = 38

define qm_background = Frame(
    "gui/button/quick_menu/quick_menu_background.png",
    qm_border, qm_border, qm_border, qm_border,
    tile=False  # étirement lissé, adapté à un dégradé d'ombre
)

# ------------------------------------------------------------
# 2) DIMENSIONS
# ------------------------------------------------------------
# Tous les boutons du dossier (qs, ql, auto, skip, save, load,
# history, settings) font 71x71px.
define qm_button_size   = 71
define qm_grid_cols     = 2
define qm_grid_rows     = 4
define qm_grid_spacing  = 6
define qm_panel_padding = 13   # ~ (168 - 2*71) / 2, marge interne du panneau

# ------------------------------------------------------------
# 3) LE SCREEN
# ------------------------------------------------------------
screen quick_menu():

    zorder 100
    default qm_expanded = False

    # --- Ferme le dropdown si on clique ailleurs à l'écran ---
    # Placé AVANT le reste : en Ren'Py, dans un screen, les éléments
    # suivants sont dessinés par-dessus les précédents et interceptent
    # le clic en priorité. Ce catch-all doit donc être en dessous
    # (déclaré en premier) pour ne pas bloquer les clics sur le menu.
    if qm_expanded:
        button:
            xfill True
            yfill True
            background None
            action SetScreenVariable("qm_expanded", False)

    fixed:
        xalign 0.0
        yalign 0.0
        xsize max(qm_button_size, qm_grid_cols * qm_button_size + (qm_grid_cols - 1) * qm_grid_spacing + 2 * qm_panel_padding)
        ysize qm_button_size + qm_grid_rows * qm_button_size + (qm_grid_rows - 1) * qm_grid_spacing + 2 * qm_panel_padding + 6

        # --- Panneau déroulant, affiché seulement si qm_expanded ---
        if qm_expanded:
            frame:
                xpos config.screen_width-352
                ypos config.screen_height-378
                background qm_background
                padding (qm_panel_padding, qm_panel_padding, qm_panel_padding, qm_panel_padding)

                grid qm_grid_cols qm_grid_rows:
                    spacing qm_grid_spacing

                    # Ligne 1 : Quick Save / Quick Load
                    imagebutton:
                        idle "gui/button/quick_menu/qs_idle.png"
                        hover "gui/button/quick_menu/qs_hover.png"
                        action QuickSave()
                    imagebutton:
                        idle "gui/button/quick_menu/ql_idle.png"
                        hover "gui/button/quick_menu/ql_hover.png"
                        action QuickLoad()
                        sensitive FileLoadable(1)

                    # Ligne 2 : Auto-forward / Skip
                    imagebutton:
                        idle "gui/button/quick_menu/auto_idle.png"
                        hover "gui/button/quick_menu/auto_hover.png"
                        selected_idle "gui/button/quick_menu/auto_hover.png"
                        action Preference("auto-forward", "toggle")
                        selected preferences.afm_enable
                    imagebutton:
                        idle "gui/button/quick_menu/skip_idle.png"
                        hover "gui/button/quick_menu/skip_hover.png"
                        action Skip()
                        alternate Skip(fast=True, confirm=True)

                    # Ligne 3 : Save / Load (menus complets)
                    imagebutton:
                        idle "gui/button/quick_menu/save_idle.png"
                        hover "gui/button/quick_menu/save_hover.png"
                        action [ShowMenu("save"), SetScreenVariable("qm_expanded", False)]
                    imagebutton:
                        idle "gui/button/quick_menu/load_idle.png"
                        hover "gui/button/quick_menu/load_hover.png"
                        action [ShowMenu("load"), SetScreenVariable("qm_expanded", False)]

                    # Ligne 4 : Journal (history) / Préférences (settings)
                    imagebutton:
                        idle "gui/button/quick_menu/history_idle.png"
                        hover "gui/button/quick_menu/history_hover.png"
                        action [ShowMenu("history"), SetScreenVariable("qm_expanded", False)]
                    imagebutton:
                        idle "gui/button/quick_menu/settings_idle.png"
                        hover "gui/button/quick_menu/settings_hover.png"
                        action [ShowMenu("preferences"), SetScreenVariable("qm_expanded", False)]

        # --- Bouton hamburger : CLIC pour ouvrir/fermer ---
    imagebutton:
        xycenter (0.5,0.5)
        xpos config.screen_width-380
        ypos config.screen_height-85
        idle "gui/button/quick_menu/menu_idle.png"
        hover "gui/button/quick_menu/menu_hover.png"
        action ToggleScreenVariable("qm_expanded")



## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")

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
    config.overlay_screens.append("hud_bottom_left")

# TIME_SLOT_NAMES (time_system.rpy) ne correspond pas 1:1 aux noms de fichiers
# que tu as poussés (ex: "Late Afternoon" -> "Afternoon_idle.png",
# "Morning" -> "Morning_mini_idle.png"). Cette table fait la conversion.
define TIME_SLOT_ICON_PREFIX = {
    "Morning": "Morning",
    "Midday": "Midday",
    "Late Afternoon": "Afternoon",
    "Evening": "Evening",
    "Night": "Night",
}

# Fonds 9-slice, mesurés directement sur tes PNG (bords transparents/alpha) :
#   Tooltip_left.png (250x71, translucide) : arrondi à gauche, plat à droite
#     (le bord droit vient se glisser sous le bouton qu'il commente)
#   Frame_mini_white.png (146x35, blanc opaque) : pilule symétrique
define hud_tooltip_bg = Frame("gui/button/Tooltip_left.png", 25, 35, 65, 49, tile=False)
define hud_label_bg   = Frame("gui/button/Frame_mini_white.png", 13, 17, tile=False)

# Réglages de position/recouvrement — à ajuster visuellement en jeu, ce sont
# des points de départ raisonnables, pas des valeurs mesurées.
define hud_icon_size       = 71
define hud_tooltip_overlap = 12   # de combien le tooltip se glisse SOUS le bouton
define hud_label_yoffset   = 50   # décalage vertical de la pastille de nom sous l'icône
define hud_tooltip_room    = 400  # largeur dispo pour le tooltip, doit être assez large pour ne jamais couper le texte


screen hud_bottom_left():
    
    zorder 90

    default map_hovering = False
    default tp_hovering  = False
    default tp_pinned    = False

    python:
        tp_icon_prefix = TIME_SLOT_ICON_PREFIX[game_time.slot_name]
        tp_date_text = "{}, {}".format(game_time.weekday_name, game_time.date.strftime("%d/%m/%Y"))



    # ------------------------------------------------------------
    # Bouton Map
    # ------------------------------------------------------------

    # Tooltip de map : visible au survol
    if map_hovering:
        frame:
            background hud_tooltip_bg
            padding (23, 8, 40, 21)
            xycenter (0.5,0.5)
            xalign 1.0
            xpos 345
            ypos config.screen_height-145

            text _("Travel elsewhere") size 28 color "#3a2f4d" xalign 0.5 yalign 0.5 layout "nobreak" at show_hide_dissolve_full_instant_speed

    imagebutton:
        xycenter (0.5,0.5)
        xpos 345
        ypos config.screen_height-150
        idle "gui/button/quick_menu/map_idle.png"
        hover "gui/button/quick_menu/map_hover.png"
        insensitive "gui/button/quick_menu/map_insensitive.png"
        hovered SetScreenVariable("map_hovering", True)
        unhovered SetScreenVariable("map_hovering", False)
        action Show("travel_menu")

    # ------------------------------------------------------------
    # Bouton Time Period
    # ------------------------------------------------------------

    # Tooltip de date : visible au survol OU épinglé par un clic
    if tp_hovering or tp_pinned:
        frame:
            background hud_tooltip_bg
            padding (23, 8, 40, 21)
            xycenter (0.5,0.5)
            xalign 1.0
            xpos 380
            ypos config.screen_height-85

            text tp_date_text size 28 color "#3a2f4d" xalign 0.5 yalign 0.5 layout "nobreak" at show_hide_dissolve_full_instant_speed

    imagebutton:
        xycenter (0.5,0.5)
        xpos 380
        ypos config.screen_height-85
        idle "gui/button/quick_menu/%s_idle.png" % tp_icon_prefix
        hover "gui/button/quick_menu/%s_hover.png" % tp_icon_prefix
        hovered SetScreenVariable("tp_hovering", True)
        unhovered SetScreenVariable("tp_hovering", False)
        action ToggleScreenVariable("tp_pinned")

    # Pastille de nom du créneau, toujours visible, sous l'icône
    frame:
        xycenter (0.5,0.5)
        xpos 380
        ypos config.screen_height-58
        background hud_label_bg
        padding(13,0)

        text game_time.slot_name color "#3a2f4d" xalign 0.5 yalign 0.5 size 22


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


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.35

        spacing gui.navigation_spacing

        if main_menu:

            imagebutton:
                auto "gui/button/navigation/start_%s.png"
                foreground Text(_("Start"), style ="navigation_btn")
                hover_foreground Text(_("Start"), style ="navigation_btn_hover")
                action Start()

        else:

            imagebutton:
                auto "gui/button/navigation/history_%s.png"
                foreground Text(_("History"), style ="navigation_btn")
                hover_foreground Text(_("History"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("History"), style ="navigation_btn_hover")
                action ShowMenu("history")

            imagebutton:
                auto "gui/button/navigation/save_%s.png"
                foreground Text(_("Save"), style ="navigation_btn")
                hover_foreground Text(_("Save"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("Save"), style ="navigation_btn_hover")
                action ShowMenu("save")

        imagebutton:
                auto "gui/button/navigation/load_%s.png"
                foreground Text(_("Load"), style ="navigation_btn")
                hover_foreground Text(_("Load"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("Load"), style ="navigation_btn_hover")
                action ShowMenu("load")

        imagebutton:
                auto "gui/button/navigation/preferences_%s.png"
                foreground Text(_("Settings"), style ="navigation_btn")
                hover_foreground Text(_("Settings"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("Settings"), style ="navigation_btn_hover")
                action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        imagebutton:
                auto "gui/button/navigation/about_%s.png"
                foreground Text(_("About"), style ="navigation_btn")
                hover_foreground Text(_("About"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("About"), style ="navigation_btn_hover")
                action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            imagebutton:
                auto "gui/button/navigation/help_%s.png"
                foreground Text(_("Help"), style ="navigation_btn")
                hover_foreground Text(_("Help"), style ="navigation_btn_hover")
                selected_idle_foreground Text(_("Help"), style ="navigation_btn_hover")
                action ShowMenu("help")

        # if renpy.variant("pc") and main_menu:

        #     ## The quit button is banned on iOS and unnecessary on Android and
        #     ## Web.
        #     textbutton _("Quit") action Quit(confirm=not main_menu)

    vbox:
        yalign 0.95
        xpos gui.navigation_xpos
        if not main_menu:
            imagebutton:
                    auto "gui/button/navigation/mainmenu_%s.png"
                    foreground Text(_("Title"), style ="navigation_btn")
                    hover_foreground Text(_("Title"), style ="navigation_btn_hover")
                    action MainMenu()
            imagebutton:
                auto "gui/button/navigation/return_%s.png"
                foreground Text(_("Return"), style ="navigation_btn")
                hover_foreground Text(_("Return"), style ="navigation_btn_hover")
                action Return()

        if main_menu:

            if gallery.enabled:
                imagebutton:
                    auto "gui/button/navigation/gallery_%s.png"
                    foreground Text(_("Gallery"), style ="navigation_btn")
                    hover_foreground Text(_("Gallery"), style ="navigation_btn_hover")
                    selected_idle_foreground Text(_("Gallery"), style ="navigation_btn_hover")
                    action ShowMenu("auto_gallery")

            if music_room.enabled:
                imagebutton:
                    auto "gui/button/navigation/music_room_%s.png"
                    foreground Text(_("Music"), style ="navigation_btn")
                    hover_foreground Text(_("Music"), style ="navigation_btn_hover")
                    selected_idle_foreground Text(_("Music"), style ="navigation_btn_hover")
                    action ShowMenu("music_room")

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            if renpy.variant("pc"):
                imagebutton:
                    auto "gui/button/navigation/quit_%s.png"
                    foreground Text(_("Quit"), style ="navigation_btn")
                    hover_foreground Text(_("Quit"), style ="navigation_btn_hover")
                    selected_idle_foreground Text(_("Quit"), style ="navigation_btn_hover")
                    action Quit(confirm=True)

style navigation_button is gui_button
# style navigation_button_text is gui_button_text
# style navigation_button_text

style navigation_btn_hover:
    color "#fff"
    xoffset 100
    yoffset 25

style navigation_btn:
    xoffset 100
    yoffset 25
    # size 24

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    ## This empty frame darkens the main menu.

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    # else:
    #     add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    # textbutton _("Return"):
    #     style "return_button"

    #     action Return()
    hbox:
        xpos 365
        yalign 0.10
        spacing 30
        add "gui/icons/{}.png".format(title) yalign 0.5
        label title.upper()

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin -30
    right_margin 30
    top_margin 20

style game_menu_viewport:
    xsize 1150

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label_text:
    size 70
    color gui.accent_color
    kerning 10
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        frame:
            background None
            left_padding 50
            vbox:
                label "[config.name!t]"
                text _("Version [config.version!t]\n")

                ## gui.about is usually set in options.rpy.
                if gui.about:
                    text "[gui.about!t]\n"

                text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:
            xpos -150
            
            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                ypos 55
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5 xoffset 18 yoffset 15

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 0.96

                spacing gui.page_spacing

                imagebutton:
                    auto "gui/button/page_number_%s.png"
                    foreground Text(_("<"),style="pg_num_idle")
                    hover_foreground Text(_("<"),style="pg_num_hover")
                    selected_foreground Text(_("<"),style="pg_num_hover") 
                    selected_idle_foreground Text(_("<"),style="pg_num_hover") 
                    insensitive_foreground Text(_("<"),style="pg_num_insensitive") 
                    action FilePagePrevious()

                if config.has_autosave:
                    # textbutton _("{#auto_page}A") action FilePage("auto")
                    imagebutton:
                        auto "gui/button/page_number_%s.png"
                        foreground Text(_("{#auto_page}A"),style="pg_num_idle")
                        hover_foreground Text(_("{#auto_page}A"),style="pg_num_hover")
                        selected_foreground Text(_("{#auto_page}A"),style="pg_num_hover") 
                        selected_idle_foreground Text(_("{#auto_page}A"),style="pg_num_hover") 
                        action FilePage("auto")

                if config.has_quicksave:
                    # textbutton _("{#quick_page}Q") action FilePage("quick")
                    imagebutton:
                        auto "gui/button/page_number_%s.png"
                        foreground Text(_("{#quick_page}Q"),style="pg_num_idle")
                        hover_foreground Text(_("{#quick_page}Q"),style="pg_num_hover")
                        selected_foreground Text(_("{#quick_page}Q"),style="pg_num_hover") 
                        selected_idle_foreground Text(_("{#quick_page}Q"),style="pg_num_hover") 
                        action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):

                    imagebutton:
                        auto "gui/button/page_number_%s.png"
                        foreground Text(_("{}".format(page)), style="pg_num_idle")
                        hover_foreground Text(_("{}".format(page)), style="pg_num_hover")
                        selected_foreground Text(_("{}".format(page)), style="pg_num_hover")
                        selected_idle_foreground Text(_("{}".format(page)), style="pg_num_hover")
                        action FilePage(page)
                        
                imagebutton:
                    auto "gui/button/page_number_%s.png"
                    foreground Text(_(">"),style="pg_num_idle")
                    hover_foreground Text(_(">"),style="pg_num_hover")
                    selected_foreground Text(_(">"),style="pg_num_hover") 
                    selected_idle_foreground Text(_(">"),style="pg_num_hover") 
                    insensitive_foreground Text(_(">"),style="pg_num_insensitive") 
                    action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style pg_num_idle:
    yoffset 15
    xoffset 28
    color gui.interface_text_color

style pg_num_insensitive:
    yoffset 15
    xoffset 28
    color "#aaa"

style pg_num_hover:
    yoffset 15
    xoffset 28
    color "#fff"

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")
    size 30

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    xoffset 25
    yoffset 25


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 65
            yoffset 40
            hbox:
                # spacing 
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("DISPLAY")
                        imagebutton:
                            auto "gui/button/radio_%s_background.png"
                            foreground Text(_("Window"), style="custom_btn_txt")
                            hover_foreground Text(_("Window"), style="custom_btn_txt_hover")
                            action Preference("display", "window")

                        imagebutton:
                            auto "gui/button/radio_%s_background.png"
                            foreground Text(_("Fullscreen"), style="custom_btn_txt")
                            hover_foreground Text(_("Fullscreen"), style="custom_btn_txt_hover")
                            action Preference("display", "fullscreen")

                if renpy.variant("touch"):
                    vbox:
                        style_prefix "radio"
                        label _("ROLLBACK SIDE")
                        textbutton _("Disable") action Preference("rollback side", "disable")
                        textbutton _("Left") action Preference("rollback side", "left")
                        textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "radio"
                    label _("SKIP")
                    imagebutton:
                        auto "gui/button/radio_%s_background.png"
                        foreground Text(_("Unseen Text"), style="custom_btn_txt")
                        hover_foreground Text(_("Unseen Text"), style="custom_btn_txt_hover")
                        action Preference("skip", "toggle")

                    imagebutton:
                        auto "gui/button/radio_%s_background.png"
                        foreground Text(_("After Choices"), style="custom_btn_txt")
                        hover_foreground Text(_("After Choices"), style="custom_btn_txt_hover")
                        action Preference("after choices", "toggle")

                    imagebutton:
                        auto "gui/button/radio_%s_background.png"
                        foreground Text(_("Transitions"), style="custom_btn_txt")
                        hover_foreground Text(_("Transitions"), style="custom_btn_txt_hover")
                        action InvertSelected(Preference("transitions", "toggle"))
                    # textbutton _("Unseen Text") action Preference("skip", "toggle")
                    # textbutton _("After Choices") action Preference("after choices", "toggle")
                    # textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                yoffset 25
                style_prefix "slider"
                spacing 100
                box_wrap True

                vbox:
                    spacing 25
                    vbox:
                        label _("TEXT SPEED")
                        bar value Preference("text speed") style "bar"

                    vbox:
                        label _("AUTO-FORWARD TIME")
                        bar value Preference("auto-forward time") style "bar"

                vbox:
                    spacing 25
                    if config.has_music:
                        vbox:
                            label _("MUSIC VOLUME")
                            hbox:
                                bar value Preference("music volume") style "bar"

                    if config.has_sound:

                        vbox:
                            label _("SOUND VOLUME")
                            hbox:
                                bar value Preference("sound volume") style "bar"

                                if config.sample_sound:
                                    textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:

                        vbox:
                            label _("VOICE VOLUME")
                            hbox:
                                bar value Preference("voice volume") style "bar"

                                if config.sample_voice:
                                    textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:

                        imagebutton:
                            auto "gui/button/radio_%s_background.png"
                            foreground Text(_("Mute All"), style="custom_btn_txt")
                            hover_foreground Text(_("Mute All"), style="custom_btn_txt_hover")
                            action [Preference("all mute", "toggle")]


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text

style slider_label_text:
    size 30

style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style custom_btn_txt:
    xoffset 65
    yoffset 9
    size 26

style custom_btn_txt_hover:
    xoffset 65
    yoffset 8
    color "#fff"
    size 26

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 5
    kerning 10

style pref_label_text:
    yalign 1.0
    # size 30

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing 10

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 400


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("viewport"), yinitial=1.0):
        
        style_prefix "history"

        for h in _history_list:

            window:
                # if "namebox_background" in h.who_args:
                
                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        # if "color" in h.who_args:
                        #     text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    # xfill True
    xoffset -60
    ysize gui.history_height
    top_margin 40

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

# style history_label:
#     xfill True

# style history_label_text:
#     xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            yoffset 20
            spacing 23

            hbox:
                
                spacing 20
                imagebutton:
                    auto "gui/button/help_tab_%s.png"
                    foreground Text(_("Keyboard"), style="confirm_txt_idle")
                    hover_foreground Text(_("Keyboard"), style="confirm_txt_hover")
                    selected_foreground Text(_("Keyboard"), style="confirm_txt_hover")
                    action SetScreenVariable("device", "keyboard")

                imagebutton:
                    auto "gui/button/help_tab_%s.png"
                    foreground Text(_("Mouse"), style="confirm_txt_idle")
                    hover_foreground Text(_("Mouse"), style="confirm_txt_hover")
                    selected_foreground Text(_("Mouse"), style="confirm_txt_hover")
                    action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    imagebutton:
                        auto "gui/button/help_tab_%s.png"
                        foreground Text(_("Gamepad"), style="confirm_txt_idle")
                        hover_foreground Text(_("Gamepad"), style="confirm_txt_hover")
                        selected_foreground Text(_("Gamepad"), style="confirm_txt_hover")
                        action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+O"
        text _("Opens the developer console.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")


    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    imagebutton:
        auto "gui/button/help_tab_%s.png"
        foreground Text(_("Calibrate"), style="confirm_txt_idle")
        hover_foreground Text(_("Calibrate"), style="confirm_txt_hover")
        selected_foreground Text(_("Calibrate"), style="confirm_txt_hover")
        action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                # textbutton _("Yes") action yes_action
                imagebutton:
                    auto "gui/button/confirm_%s.png"
                    foreground Text(_("Yes"), style="confirm_txt_idle")
                    hover_foreground Text(_("Yes"), style="confirm_txt_hover")
                    action yes_action

                imagebutton:
                    auto "gui/button/confirm_%s.png"
                    foreground Text(_("No"), style="confirm_txt_idle")
                    hover_foreground Text(_("No"), style="confirm_txt_hover")
                    action no_action
                # textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_txt_idle:
    xalign 0.5
    yalign 0.5

style confirm_txt_hover:
    xalign 0.5
    yalign 0.5
    color "#fff"

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
