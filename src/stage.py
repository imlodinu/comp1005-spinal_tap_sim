# stage.py
# Lodinu Kalugalage
#
# Description: This file contains the Stage related class which is used to represent
# the stage in the scene.


class StageDescriptor:
    width = None  # Width of the stage
    height = None  # Height of the stage
    backdrop = None  # Backdrop image (path to image prefixed with 'file://', colour, or None for no backdrop)

    # Constructor for a `StageDescriptor`
    def __init__(self, width=0.0, height=0.0, backdrop=None):
        self.width = width
        self.height = height
        self.backdrop = backdrop
