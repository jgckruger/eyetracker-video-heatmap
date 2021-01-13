from .greyheatmapper import GreyHeatMapper
from PIL import Image

class PILGreyHeatmapper(GreyHeatMapper):
    def __init__(self, point_diameter, point_strength):
        super().__init__(point_diameter, point_strength)

    def heatmap(self, width, height, points):
        heat = Image.new('L', (width, height), color=255)

        dot = (Image.open('./assets/450pxdot.png').copy()
                    .resize((self.point_diameter, self.point_diameter), resample=Image.ANTIALIAS))
        dot = self._img_to_opacity(dot, self.point_strength)

        for x, y in points:
            x, y = int(x - self.point_diameter/2), int(y - self.point_diameter/2)
            heat.paste(dot, (x, y), dot)

        return heat

    @staticmethod
    def _img_to_opacity(img, opacity):
        img = img.copy()
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        img.putalpha(alpha)
        return img