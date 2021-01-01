import json
import random
from PIL import Image, ImageDraw, ImageFont

with open('data.json') as f:
    data = json.load(f)


def get_text_size_box(width, font, full_text, spacing):
    split = []
    x = 0
    y = 0

    for text in full_text.splitlines():
        lines = []
        line = []
        for word in text:
            new_line = ''.join(line + [word])
            size = font.getsize(new_line)
            text_height = size[1]
            if size[0] <= width:
                x = max(x, size[0])
                line.append(word)
            else:
                lines.append(line)
                line = [word]

        if line:
            lines.append(line)

        split.append([''.join(line) for line in lines if line])
        y += text_height * len(split[-1]) + spacing

    return ((x, y), text_height, split)


class ImageTextDraw(ImageDraw.ImageDraw):

    def text_box(self, coordinates, full_text, box_width, color=None, font=ImageFont.load_default(), spacing=0, align='top'):
        # Adapted from https://gist.github.com/turicas/1455973
        x, y = coordinates

        size, text_height, lines = get_text_size_box(box_width, font, full_text, spacing)
        total_height = len(lines) * spacing + sum(text_height for nl in lines for _ in nl)

        if align == 'top':
            y = 0
        elif align == 'center':
            y = (self.im.size[1] - total_height) / 2
            # centralise text
        elif align == 'bottom':
            y = self.im.size[1] - total_height
        else:
            raise ValueError(f'Invalid align fed into ImageTextDraw.text_box(), expecting top, center or bottom, recieved {align}')

        for nl in lines:
            for index, line in enumerate(nl):
                self.text((x, y), line, font=font, fill=color)
                y += text_height

            y += spacing

        return (x, y + size[1])
        # returns the x and y value right below the last text


for name in data:
    w, h = data[name]
    colors = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new('RGB', (w, h), colors)
    draw = ImageTextDraw(img)
    draw.text_box((2, 0), name, w, color=tuple(255 - i for i in colors), align='center')

    img.save(f'export/{name}.png')
    print(name)
