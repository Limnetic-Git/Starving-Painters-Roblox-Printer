import pygame
import pyautogui
import time
import pyperclip
from read_picture import image_to_hex_array, get_most_common_hex_color
from masks import create_masks, optimize_masks

points_coor = {
    "colors": [1100, 950],
    "pencil": [620, 950],
    "hex": [1100, 870],
    "hex_close": [1375, 550],
    "first_pixel": [627, 235],
    "fill": [720, 950],
    }

class Printer:
    def __init__(self, image_path, intensity_of_color_compression):
        self.OFFSET = 21.5
        self.IMG_PATH = image_path
        self.INTENSITY_OF_COLOR_COMPRESSION = intensity_of_color_compression
        
        self.current_color = None
        self.run = True
        self.original_image_array = image_to_hex_array(self.IMG_PATH)
        self.masks, self.colors_on_picture = create_masks(self.original_image_array)
        
        if self.INTENSITY_OF_COLOR_COMPRESSION != 0:
            self.masks, self.colors_on_picture = optimize_masks(self.masks,
                                                                                           self.colors_on_picture,
                                                                                           self.INTENSITY_OF_COLOR_COMPRESSION)

        self.most_common_color = get_most_common_hex_color(self.masks, self.colors_on_picture)
        self.colors_on_picture.remove(self.most_common_color)
        del self.masks[self.most_common_color]
    
    def start_drawing(self):
        time.sleep(3)
        self.draw()
    
    def draw(self):
        self.global_fill(self.most_common_color)
        for i in range(len(self.colors_on_picture)):
            self.current_color = self.colors_on_picture[i]
            self.change_color(self.current_color)
            for x in range(32):
                for y in range(32):
                    if self.masks[self.current_color][x][y] != None:
                         current_x = points_coor["first_pixel"][0] + (y * self.OFFSET)
                         current_y = points_coor["first_pixel"][1] + (x * self.OFFSET)
                         self.move_to([current_x, current_y])
                         self.click()
        self.run = False
    
    def click(self):
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')

    def global_fill(self, color):
         self.change_color(color)
         route = ["fill", "first_pixel", "pencil"]
         for point in route:
             self.move_to(points_coor[point])
             self.click()

    def move_to(self, cords):
        pyautogui.moveTo(cords[0], cords[1], duration=0.0001)
        
    def change_color(self, color):
         route = ["colors", "hex", "hex_close"]
         for point in route:
             self.move_to(points_coor[point])
             self.click()
             if point == "hex":
                pyperclip.copy(color)
                pyautogui.hotkey('ctrl', 'v')

def draw_preview(x_to_draw, y_to_draw):
    pixel_size = 12
    estimated_drawing_time = 360.4
    #CHANGE COLOR TIME:  1.025
    #CHANGE BG: 2
    #DRAW 1 PIXEL: 0.35
    
    picture = eval(str(printer.masks[printer.colors_on_picture[0]].copy()))
    for color in printer.colors_on_picture:
        for x in range(32):
            for y in range(32):
                if printer.masks[color][x][y] != None:
                    picture[x][y] = printer.masks[color][x][y]
    for x in range(32):
        for y in range(32):
            if picture[y][x] != None:
                pygame.draw.rect(sc, picture[y][x], (x_to_draw + (x * pixel_size), y_to_draw + (y * pixel_size), pixel_size, pixel_size))
            else:
                pygame.draw.rect(sc, printer.most_common_color, (x_to_draw + (x * pixel_size), y_to_draw + (y * pixel_size), pixel_size, pixel_size))
                estimated_drawing_time -= 0.376
    for _ in range(len(printer.colors_on_picture)):
        estimated_drawing_time += 1.025
    print(f'Оценочное время рисовaния: {estimated_drawing_time} секунды')
    print(f'~{estimated_drawing_time / 60} минуты')
    
FPS = 60
pygame.init()

WIN_WIDTH, WIN_HEIGHT = 405, 405
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

printer = Printer('pictures/test.png', 85) # here is it

draw_preview(10, 10)
while True:
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit(0)
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                if printer.run:
                    printer.start_drawing()

    pygame.display.update()