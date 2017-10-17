hex_colors = {
    'w': '0x49D8F5',  # Water
    'f': '0x035200',  # Forest
    'g': '0x32C832',  # Grass
    'r': '0x725029',  # Road
    'mark': '0xff0000'
}
colors = {
    'w': (73, 216, 245),  # Water
    'f': (3, 82, 0),  # Forest
    'g': (50, 200, 50),  # Grass
    'r': (114, 80, 41),  # Road
    'mark': (255, 0, 0)
}
#  known_colors = [col for col in colors.values()]


def col_to_char(col):
    for k, v in colors.items():
        if v == col:
            return k
    # default return road
    return 'r'


class StaticMap:
    def __init__(self):
        self.point_one = None
        self.point_two = None
        self.init_location()
        self.url = None
        self.init_map()

    def style(self, feature, color):
        return '&style=feature:' + feature +\
            '|element:geometry.fill|color:' + hex_colors[color]

    def init_map(self):
        map_url = 'https://maps.googleapis.com/maps/api/staticmap?'
        map_size = '&zoom=14&size=640x640&maptype=roadmap'

        label_style = '&style=feature:all|element:labels|visibility:off'
        landscape_style = self.style('landscape', 'g')
        poi_style = self.style('poi', 'f')
        road_style = self.style('road', 'r')
        water_style = self.style('water', 'w')
        transit_style = self.style('transit', 'f')
        map_style = label_style + landscape_style + \
            poi_style + road_style + water_style + transit_style

        tiny_mark = 'https://i.imgur.com/RZKxQ0H.png'
        mark_from = '&markers=icon:' + tiny_mark + '|' + self.point_one + '%'
        mark_to = '&markers=icon:' + tiny_mark + '|' + self.point_two + '%'
        api_key = '&key=AIzaSyBGPMQimnM2hqZeu4oLayKLk0mW1EYKRcY'

        self.url = map_url + map_size + map_style + mark_from + mark_to + api_key

    def init_location(self, test=False):
        if test:
            self.city = 'trondheim'
            self.point_one = 'ila+brannstasjon+trondheim'
            self.point_two = 'st+olavs+trondheim'
        city = input('city/country: ')
        city = city.replace(' ', '+')

        point_one = input('Point one: ')
        self.point_one = point_one.replace(' ', '+') + '+' + city

        point_two = input('Point two: ')
        self.point_two = point_two.replace(' ', '+') + '+' + city

    def get(self):
        print(self.url)
        return self.url

    def name(self):
        return self.point_one[:10] + "-" + self.point_two[:10]
