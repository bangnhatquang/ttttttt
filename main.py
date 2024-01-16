from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.camera import Camera
import cv2
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import time
import imutils
from kivy.graphics import Color, Line
Builder.load_string('''
<CameraApp>:
    orientation: 'vertical'
    padding:10
    spacing:10
    Image:
        id: img_display
        size_hint: 1, 0.7

    MDRaisedButton:
        text: "Open Camera"
        pos_hint: {'center_x': 0.5}
        on_press: root.open_camera()
    MDRaisedButton:
        text: "CHỤP"
        pos_hint: {'center_x': 0.5}
        on_press: root.save_image()    
    MDList:
        id:resultbox
''')

class CameraApp(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.img_display = self.ids.img_display
        self.capture = None

    def save_image(self):
    #Lưu ảnh khi bấm nút Save
         ret, frame = self.capture.read()

         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         height, width = gray_frame.shape[:2]
         h = int(height / 210)
         w = int(width / 297)
         k = h
         if h > w: k = w
         y = int(210 * k)  # chiều ngắn
         x = int(297 * k)  # chiều dài
         image = cv2.rectangle(gray_frame, (0, 0), (x , y ), (255, 0, 0), 2)
         Cropped_img = cv2.cvtColor(frame[0:y, 0:x], cv2.COLOR_BGR2GRAY)

         timenow = time.strftime("%Y%m%d_%H%M%S")
         cv2.imwrite("C:\\Users\\QUANG\\Desktop\\myimage_{}.png".format(timenow), Cropped_img)
         #self.capture = None # THOÁT
         #self.capture = cv2.VideoCapture(0)

    def open_camera(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
    def update(self, dt):
        ret, frame = self.capture.read()


        if ret:
            # Convert the frame to texture


            #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame=frame
            height, width = gray_frame.shape[:2]
            h = int(height / 210)
            w = int(width / 297)
            k = h
            if h > w: k = w
            start_point = (0, 0)
            end_point = (60, 60)
            y = int(210 * k)  # chiều ngắn
            x = int(297 * k)  # chiều dài
            image = cv2.rectangle(gray_frame, start_point, end_point, (255, 0, 0), 2)
            image = cv2.rectangle(gray_frame, start_point, end_point, (255, 0, 0), 2)  # điểm trên, bên trái
            image = cv2.rectangle(gray_frame, (0, 0 + y), (60, y - 60), (255, 0, 0), 2)  # điểm dưới, bên trái
            image = cv2.rectangle(gray_frame, (0 + x, 0), (x - 60, 60), (255, 0, 0), 2)  # điểm trên, bên phải
            image = cv2.rectangle(gray_frame, (0 + x, 0 + y), (x - 60, y - 60), (255, 0, 0), 2)  # điểm dưới, bên phải

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            # Finding contours in threshold image
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            rectangles = []
            for contour in cnts:
                bounding_rect = cv2.boundingRect(contour)
                color = (0, 255, 0)  # vẽ màu xanh mã RGB
                thickness = 3  # nét vẽ
                if cv2.contourArea(contour) > 100:
                    x, y, width, height = bounding_rect
                    total_white_points = cv2.countNonZero(thresh[y:y + height, x:x + width]) / cv2.contourArea(contour)

                    if total_white_points > 1:
                        cv2.rectangle(image, bounding_rect, color, thickness)
                    rectangles.append(bounding_rect)  # lấy tọa độ

            img_buf = cv2.flip(gray_frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(img_buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_display.texture = texture
            with self.img_display.canvas:
                Color(1, 0, 0)  # Set color to red
                #Line(rectangle=(0, 0, 20, 20))
               #Line(rectangle=(0, self.img_display.height - 20, 20, self.img_display.height))





class MainApp(MDApp):
    def build(self):
        return CameraApp()

if __name__ == '__main__':
    MainApp().run()

class CLASS_CAMERA:
    def abcDE(self):
        print("abc() is called!")
