from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = 'files/ticket.png'
FONT_PATH = 'files/3966.ttf'
FONT_SIZE = 15
FONT_COLOR = (0, 0, 0, 255)
OFFSET_DATA_DEPARTURE = ((320, 261))
OFFSET_DEPARTURE_CITY = ((43, 194))
OFFSET_ARRIVAL_CITY = ((43, 261))
OFFSET_NAME = ((43, 126))


def create_ticket(context):
    departure_city = context['departure_city_full_name']
    data_departure = context['date_departure']
    arrival_city = context['arrival_city']
    name = context['name']
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    fnt = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(base)
    draw.text(OFFSET_DEPARTURE_CITY, departure_city, font=fnt, fill=FONT_COLOR)
    draw.text(OFFSET_ARRIVAL_CITY, arrival_city, font=fnt, fill=FONT_COLOR)
    draw.text(OFFSET_DATA_DEPARTURE, data_departure, font=fnt, fill=FONT_COLOR)
    draw.text(OFFSET_NAME, name, font=fnt, fill=FONT_COLOR)
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file
