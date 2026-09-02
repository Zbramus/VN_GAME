# Instant CG and BG Gallery by Leon: https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=22465 

init python:
    #list the CG gallery images here:
    gallery_thumbnails = []

    gal_rows = 3
    gal_cols = 2

    #Thumbnail size in pixels:
    thumbnail_x = 328
    thumbnail_y = 185
    
    gal_cells = gal_rows * gal_cols    
    g_cg = Gallery()

    if gallery.variable_mode:
        # Variable mode: items are dicts like {"image": "name", "variable": "var_name"}
        # or {"image": ["img1", "img2"], "variable": "var_name"}
        for gal_item in gallery.items:
            images = gal_item["image"]
            variable = gal_item["variable"]

            if isinstance(images, list):
                gallery_thumbnails.append(images[0])
                g_cg.button(images[0] + " butt")
                g_cg.condition(variable)
                for img in images:
                    g_cg.image(img)
            else:
                gallery_thumbnails.append(images)
                g_cg.button(images + " butt")
                g_cg.condition(variable)
                g_cg.image(images)

    else:
        # Standard mode: items are strings or lists of strings, unlocked by seen-image tracking
        for gal_item in gallery.items:
            if (isinstance(gal_item, list)):
                gallery_thumbnails.append(gal_item[0])
                g_cg.button(gal_item[0] + " butt")

                if gallery.strict_multiple:
                    g_cg.unlock_image(*gal_item)
                
                else:
                    for item in gal_item:
                        g_cg.unlock_image(item)

            else:
                gallery_thumbnails.append(gal_item)
                g_cg.button(gal_item + " butt")
                g_cg.unlock_image(gal_item)
            
    g_cg.transition = fade
    
init +1 python:
    #Here we create the thumbnails. 
    for gal_item in gallery_thumbnails:
        renpy.image(gal_item + " butt", Transform(gal_item, xysize=(thumbnail_x, thumbnail_y), fit="contain"))
        
screen auto_gallery:
    tag menu
    default cg_page = 0
    use game_menu(_("Gallery")):
        $ current_num = cg_page + 1

        fixed:
            xpos -170

            if (len(gallery_thumbnails)>gal_cells):
                text "Page {}".format(current_num):
                    ypos 55
                    xalign 0.5
                    style "page_label_text"

            frame background None:
                xalign 0.5
                yalign 0.5
                grid gal_rows gal_cols:
                    xalign 0.5
                    yalign 0.5
                    spacing gui.slot_spacing

                    $ i = 0
                    $ next_cg_page = cg_page + 1
                    $ prev_cg_page = cg_page -1            
                    if next_cg_page > (len(gallery_thumbnails) - 1) // gal_cells:
                        $ next_cg_page = 0

                    elif prev_cg_page == -1:
                        $ prev_cg_page = 0

                    for gal_item in gallery_thumbnails:
                        $ i += 1
                        if i <= (cg_page+1)*gal_cells and i>cg_page*gal_cells:
                            add g_cg.make_button(gal_item + " butt", gal_item + " butt","gui/gallery/locked.png", xalign=0.5, yalign=0.5, idle_border=None, background=None, bottom_margin=24)
                    for j in range(i, (cg_page+1)*gal_cells): #we need this to fully fill the grid
                        null

                if (len(gallery_thumbnails)>gal_cells):
                    $ pages = (len(gallery_thumbnails) + gal_cells - 1) // gal_cells

                    hbox:
                        style_prefix "page"

                        xalign 0.5
                        yalign 0.96

                        spacing gui.page_spacing

                        imagebutton:
                            auto "gui/gallery/page_number_%s.png"
                            foreground Text(_("<"),style="pg_num_idle")
                            hover_foreground Text(_("<"),style="pg_num_hover") 
                            insensitive_foreground Text(_("<"),style="pg_num_insensitive")
                            action [SetScreenVariable('cg_page', prev_cg_page)]
                            sensitive cg_page != 0

                        for num in range(pages):
                            $display_num = num + 1
                            imagebutton:
                                auto "gui/gallery/page_number_%s.png"
                                foreground Text(_("{}".format(display_num)), style="pg_num_idle")
                                hover_foreground Text(_("{}".format(display_num)), style="pg_num_hover")
                                action [SetScreenVariable('cg_page', num)]

                        imagebutton:
                            auto "gui/gallery/page_number_%s.png"
                            foreground Text(_(">"),style="pg_num_idle")
                            hover_foreground Text(_(">"),style="pg_num_hover")
                            insensitive_foreground Text(_(">"),style="pg_num_insensitive")
                            action [SetScreenVariable('cg_page', next_cg_page)]
                            sensitive cg_page != pages-1