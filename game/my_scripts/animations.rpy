# DO NOT MODIFY ANY CODE IN THIS FILE UNLESS YOU ARE 100% SURE WHAT YOU ARE DOING. If you aren't sure, ask in the community forums for clarification.
init python:
    if gui.use_side_image:
        gui.dialogue_xpos = 690
        gui.name_xpos = 830
    
    def getRandomDegreeAnim():
        degree = renpy.random.choice([-5,-7,-2,2,7,5])
        return degree

transform anim_hover:
    on hover:
        linear 0.25 yoffset -20 rotate getRandomDegreeAnim()

    on idle: 
        linear 0.15 yoffset 0 rotate 0

transform show_hide_dissolve_dot45:
    on show:
        alpha .0
        ease .3 alpha 0.45
    on hide:
        alpha 0.45
        ease .3 alpha .0

transform show_hide_dissolve_full:
    on show:
        alpha .0
        ease .3 alpha 1.0
    on hide:
        alpha 1.0
        ease .3 alpha .0

transform show_hide_dissolve_full_speed:
    on show:
        alpha .0
        ease .15 alpha 1.0
    on hide:
        alpha 1.0
        ease .15 alpha .0

transform show_hide_dissolve_full_instant_speed:
    on show:
        alpha .0
        ease .01 alpha 1.0
    on hide:
        alpha 1.0
        ease .01 alpha .0

transform hide_dissolve_full:
    on hide:
        ease .3 alpha .0


init python:
    class RoundRect(renpy.Displayable):
        def __init__(self, width=None, height=None, radius=0, color="#fff", **properties):
            super().__init__(**properties)

            self.width = width

            if height is None:
                height = width
            self.height = height

            self.radius = radius

            self.color = color # will look bad if not 100% opaque

        def render(self, width, height, st, at):
            if self.width is not None:
                width = self.width
            if self.height is not None:
                height = self.height
            rv = renpy.Render(width, height)
            cv = rv.canvas()
            radius = self.radius

            # sanity check
            if 2*radius > width or 2*radius > height:
                raise ValueError("radius must be smaller than half of width and height.")

            cv.circle(self.color, (radius, radius), radius) # top-left
            cv.circle(self.color, (width-radius, radius), radius) # top-right
            cv.circle(self.color, (radius, height-radius), radius) # bottom-left
            cv.circle(self.color, (width-radius, height-radius), radius) # bottom-right

            cv.rect(self.color, (radius, 0, width-2*radius, height)) # vertical rectangle
            cv.rect(self.color, (0, radius, width, height-2*radius)) # horizontal rectangle

            return rv

transform round_rect_cut(child, radius, width=None, height=None):
    AlphaMask(child, RoundRect(width, height, radius))