from ExifEditor import ExifEditor


class Pytag:

    def __init__(self):
        print("It seems to work")
        self.exif_editor = ExifEditor("UserComment")


app = Pytag()
