# ============================================================
# QUICK MENU — hamburger cliquable + dropdown
# Remplace le screen "quick_menu" par défaut de screens.rpy
# Basé sur les assets réels de game/gui/button/quick_menu/
# ============================================================

# ------------------------------------------------------------
# 1) FOND 9-SLICE
# ------------------------------------------------------------
# quick_menu_background.png fait 168x310px, avec un dégradé
# d'ombre transparent tout autour du rectangle violet arrondi.
#
# Mesuré directement sur ton PNG (scan du canal alpha) :
#   - largeur du flou d'ombre sur les bords plats : 13-14px
#   - les 4 coins arrondis sont symétriques et ont besoin de
#     36-37px pour être entièrement contenus (rayon + flou compris)
# -> la bordure du Frame doit donc faire AU MOINS 37px sur
#    chaque côté pour ne rien déformer. Je mets 38 par sécurité.
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
# ATTENTION : je n'ai pas trouvé d'asset "hamburger" (☰) dans
# game/gui/button/quick_menu/ sur le repo — seuls les 8 boutons
# du menu + le fond y sont. Il faudra soit :
#   a) ajouter hamburger_idle.png / hamburger_hover.png dans ce
#      dossier (mêmes conventions que le reste : idle/hover), soit
#   b) me dire le nom exact si tu l'as mis ailleurs.
# Le code ci-dessous suppose l'option (a).

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
        xalign 1.0
        yalign 1.0
        xsize max(qm_button_size, qm_grid_cols * qm_button_size + (qm_grid_cols - 1) * qm_grid_spacing + 2 * qm_panel_padding)
        ysize qm_button_size + qm_grid_rows * qm_button_size + (qm_grid_rows - 1) * qm_grid_spacing + 2 * qm_panel_padding + 6

        # --- Panneau déroulant, affiché seulement si qm_expanded ---
        if qm_expanded:
            frame:
                xalign 1.0
                yalign 0.0
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
                        selected preferences.auto_forward
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
            xalign 1.0
            yalign 1.0
            idle "gui/button/quick_menu/menu_idle.png"
            hover "gui/button/quick_menu/menu_hover.png"
            action ToggleScreenVariable("qm_expanded")
