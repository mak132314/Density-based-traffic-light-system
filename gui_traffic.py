import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog 
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer 
from PIL import Image
from ultralytics import YOLO
from PyQt5.QtCore import Qt
import time

class ImageUploaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = YOLO("yolov8n.pt")
        self.setWindowTitle("Image Uploader and Resizer")
        self.num_cars = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        # Labels for uploaded images
        self.top_image_label = QLabel(self)
        self.top_image_label.setAlignment(Qt.AlignCenter)
        self.top_image_label.setGeometry(210, 50, 200, 200)

        self.left_image_label = QLabel(self)
        self.left_image_label.setAlignment(Qt.AlignCenter)
        self.left_image_label.setGeometry(10, 270, 200, 200)

        self.right_image_label = QLabel(self)
        self.right_image_label.setAlignment(Qt.AlignCenter)
        self.right_image_label.setGeometry(450, 270, 200, 200)

        self.bottom_image_label = QLabel(self)
        self.bottom_image_label.setAlignment(Qt.AlignCenter)
        self.bottom_image_label.setGeometry(210, 510, 200, 200)

        # Buttons to upload images
        self.top_button = QPushButton("Upload Top Image", self)
        self.top_button.clicked.connect(lambda: self.upload_image("top"))
        self.top_button.setGeometry(230, 10, 200, 30)

        self.left_button = QPushButton("Upload Left Image", self)
        self.left_button.clicked.connect(lambda: self.upload_image("left"))
        self.left_button.setGeometry(30, 260, 200, 30)

        self.right_button = QPushButton("Upload Right Image", self)
        self.right_button.clicked.connect(lambda: self.upload_image("right"))
        self.right_button.setGeometry(470, 260, 200, 30)

        self.bottom_button = QPushButton("Upload Bottom Image", self)
        self.bottom_button.clicked.connect(lambda: self.upload_image("bottom"))
        self.bottom_button.setGeometry(230, 500, 200, 30)

        # Run button
        self.run_button = QPushButton("Run", self)
        self.run_button.setGeometry(560, 20, 100, 60)
        self.run_button.setStyleSheet("background-color: lightblue")
        self.run_button.clicked.connect(self.sort_num_cars)

        # Green buttons
        self.green_button1 = QPushButton(self)
        self.green_button1.setGeometry(550+200+230, 160-90, 30, 30)
        self.green_button1.setStyleSheet("background-color: gray")

        self.green_button2 = QPushButton(self)
        self.green_button2.setGeometry(300+200+230, 350-90, 30, 30)
        self.green_button2.setStyleSheet("background-color: gray")

        self.green_button3 = QPushButton(self)
        self.green_button3.setGeometry(800+200+230, 350-90, 30, 30)
        self.green_button3.setStyleSheet("background-color: gray")

        self.green_button4 = QPushButton(self)
        self.green_button4.setGeometry(550+200+230, 540-90, 30, 30)
        self.green_button4.setStyleSheet("background-color: gray")

        self.green_buttons = {"top": self.green_button1, "left": self.green_button2, "right": self.green_button3, "bottom": self.green_button4}

        # Red buttons
        self.red_button1 = QPushButton(self)
        self.red_button1.setGeometry(550+200+230, 200-90, 30, 30)
        self.red_button1.setStyleSheet("background-color: gray")

        self.red_button2 = QPushButton(self)
        self.red_button2.setGeometry(340+200+230, 350-90, 30, 30)
        self.red_button2.setStyleSheet("background-color: gray")

        self.red_button3 = QPushButton(self)
        self.red_button3.setGeometry(760+200+230, 350-90, 30, 30)
        self.red_button3.setStyleSheet("background-color: gray")

        self.red_button4 = QPushButton(self)
        self.red_button4.setGeometry(550+200+230, 500-90, 30, 30)
        self.red_button4.setStyleSheet("background-color: gray")

        self.red_buttons = {"top": self.red_button1, "left": self.red_button2, "right": self.red_button3, "bottom": self.red_button4}

        # Dictionary to store uploaded images
        self.images = {"top": None, "left": None, "right": None, "bottom": None}

        # Draw black roads
        self.draw_black_roads()

    def upload_image(self, direction):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image files (*.jpg *.png)")
        if file_path:
            results = self.model(file_path)
            
            image = Image.open(file_path)
            image = image.resize((200, 200))
            q_image = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            if direction == "top":
                self.images["top"] = pixmap
                self.top_image_label.setPixmap(pixmap)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.data[0][-1])
                        if self.model.names[class_id] in ['car', 'bus', 'truck']:
                            self.num_cars['top'] += 1
            elif direction == "left":
                self.images["left"] = pixmap
                self.left_image_label.setPixmap(pixmap)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.data[0][-1])
                        if self.model.names[class_id] in ['car', 'bus', 'truck']:
                            self.num_cars['left'] += 1
            elif direction == "right":
                self.images["right"] = pixmap
                self.right_image_label.setPixmap(pixmap)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.data[0][-1])
                        if self.model.names[class_id] in ['car', 'bus', 'truck']:
                            self.num_cars['right'] += 1
            elif direction == "bottom":
                self.images["bottom"] = pixmap
                self.bottom_image_label.setPixmap(pixmap)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.data[0][-1])
                        if self.model.names[class_id] in ['car', 'bus', 'truck']:
                            self.num_cars['bottom'] += 1

    def sort_num_cars(self):
        sorted_cars = dict(sorted(self.num_cars.items(), key=lambda item: item[1], reverse=True))

        self.change_buttons_color(sorted_cars)

    def change_buttons_color(self, sorted_cars):
        sorted_cars_keys = list(sorted_cars.keys())
        num_buttons = len(sorted_cars_keys)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_button_color)
        self.current_index = 0
        self.sorted_cars_keys = sorted_cars_keys
        self.sorted_cars = sorted_cars
        self.timer.start(3000)  # Change color every 1 second

    # def update_button_color(self):
    #     if self.current_index < len(self.sorted_cars_keys):
    #         button_key = self.sorted_cars_keys[self.current_index]
    #         current_button_green = self.green_buttons[button_key]
    #         current_button_green.setStyleSheet("background-color: green")
            
    #         if self.current_index != 0:
    #             previous_button_key = self.sorted_cars_keys[self.current_index-1]
    #             previos_button = self.red_buttons[previous_button_key]
    #             previos_button.setStyleSheet("background-color: red")
    #         self.current_index += 1
    #     else:
    #         self.timer.stop()
    #         self.red_buttons[self.sorted_cars_keys[-1]].setStyleSheet("background-color: red")
    def update_button_color(self):
        if self.current_index < len(self.sorted_cars_keys):
            button_key = self.sorted_cars_keys[self.current_index]
            
            # Current green button turns green
            current_button_green = self.green_buttons[button_key]
            current_button_green.setStyleSheet("background-color: green")
            
            # Current red button turns red
            # current_button_red = self.red_buttons[button_key]
            # current_button_red.setStyleSheet("background-color: red")
            for key in self.red_buttons:
                if key != button_key:
                    self.red_buttons[key].setStyleSheet("background-color: red")
                else:
                    self.red_buttons[key].setStyleSheet("background-color: gray")
            if self.current_index != 0:
                # Previous green button turns gray
                previous_button_key = self.sorted_cars_keys[self.current_index-1]
                previous_button_green = self.green_buttons[previous_button_key]
                previous_button_green.setStyleSheet("background-color: gray")
                previous_button_red = self.red_buttons[previous_button_key]
                previous_button_red.setStyleSheet("background-color: red")
                # All other red buttons remain red, previous red button should stay red
                # for key in self.red_buttons:
                #     if key != button_key:
                #         self.red_buttons[key].setStyleSheet("background-color: red")
                        
            self.current_index += 1
        else:
            # When the last button is reached, stop the timer and reset colors
            self.timer.stop()
            for key in self.green_buttons:
                self.green_buttons[key].setStyleSheet("background-color: gray")
            for key in self.red_buttons:
                self.red_buttons[key].setStyleSheet("background-color: gray")

    def draw_black_roads(self):
        # Create horizontal road
        self.horizontal_road = QLabel(self)
        self.horizontal_road.setGeometry(380+200+230, 350-90, 370, 30)
        self.horizontal_road.setStyleSheet("background-color: black")

        # Create vertical road
        self.vertical_road = QLabel(self)
        self.vertical_road.setGeometry(550+200+230, 240-90, 30, 250)
        self.vertical_road.setStyleSheet("background-color: black")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploaderApp()
    window.setGeometry(200, 200, 1500, 800)
    window.show()
    sys.exit(app.exec_())
