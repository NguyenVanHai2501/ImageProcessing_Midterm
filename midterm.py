import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import imutils 
from PIL import ImageTk, Image, ImageDraw,ImageFont

stacked_array = []
# Tạo một cửa sổ và gọi lớp ImageDisplay để hiển thị ảnh
root = tk.Tk()
app = None

# Tạo một label để hiển thị ảnh
image_label_original = tk.Label(root)
image_label_original.pack()

# Tạo một label để hiển thị tên ảnh
text_label_original = tk.Label(root)
text_label_original.pack()
def changeContourColor(image, contour, change):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Khởi tạo contour mask zero
    mask = np.zeros(gray.shape, np.uint8)

    # Vẽ contour trên back ground mask zero
    cv2.drawContours(mask,[contour],0,255,-1)

    # dùng hàm cv2.findNoneZero() lấy ra toàn bộ các points có giá trị khác 0 là các điểm ở trong contour
    pixelpoints = cv2.findNonZero(mask)

    # chuyển ảnh từ BGR sang HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # lăp qua tất cả điểm ở trong contour, lấy màu của điểm đó (dạng HSV) rồi thay đổi 1 chút.(change)
    for point in pixelpoints:
        h, s, v = hsv[point[0][1], point[0][0]]
        hsv[point[0][1], point[0][0]] = np.clip([h,s,v + change], 0, 255)
    
    # chuyển ảnh về dạng BRG rồi return lại ảnh
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def changeAllBlack(image, color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Xác định ngưỡng màu để phân đoạn
    lower = np.array([0, 0, 0])  # giá trị ngưỡng thấp cho H, S, V
    upper = np.array([250, 255, 100])  # giá trị ngưỡng cao cho H, S, V
    mask = cv2.inRange(hsv, lower, upper)  # tạo mặt nạ

    # Áp dụng mặt nạ để lấy vật thể và đổi màu sắc
    result = image.copy()
    result[mask != 0] = color  # đổi màu thành màu xám
    return result

def result(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)
    return image

def result1(image, color):
    image = changeAllBlack(image, color)
    cv2.putText(image, 'Result: All blacks are dimmed', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, 'This image changed black to blue', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return image

def changeSize(image):
    # Lấy kích thước ảnh gốc
    (height, width,_) = image.shape
    
    # Kích thước mới
    if height > width:
        new_height = 500
        new_width = int(width * (new_height/height))
    else: 
        new_width = 600
        new_height = int(height * (new_width/width))
    image = cv2.resize(image,(new_width, new_height))
    
    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(color_coverted))
    return photo

class ImageDisplay:
    def __init__(self, master, images):
        self.master = master
        self.images = images
        self.current_index = 0

        # Tạo một label để hiển thị ảnh
        self.image_label = tk.Label(master)
        self.image_label.pack()

        # Tạo một label để hiển thị tên ảnh
        self.text_label = tk.Label(master)
        self.text_label.pack()
        
        # Tạo một button để chuyển đổi ảnh
        self.button = tk.Button(master, text="View", command=self.change_image)
        self.button.pack()
        
        # Hiển thị ảnh đầu tiên trong danh sách
        # self.show_image()
    def setNewImages(self, images):
        self.images = stacked_array
        self.current_index = 0
        self.button.config(text= "view")

    def show_image(self):
        if self.current_index == 0:
            self.current_index = self.current_index + 1
        photo = changeSize(self.images[self.current_index])
        text = "Level "
        if self.current_index >= 4:
            text = "Result Of Level "
            self.text_label.config(text=text + str((self.current_index % 4) + 1))
            self.button.config(text="Next Result")
        else: 
            self.text_label.config(text=text + str(self.current_index))
            self.button.config(text="Next Level")
        self.text_label.place(x = 950, y = (650 - photo.height())/2 - 40)
        self.image_label.config(image=photo)
        self.image_label.place(x= 50 + photo.width() ,y = (650 - photo.height())/2 - 10)
        self.image_label.image = photo
    
    def change_image(self):
        # Chuyển đổi đến ảnh tiếp theo trong danh sách
        self.current_index = (self.current_index + 1) % len(self.images)
        self.show_image()

def loadOriginalImage():
    # Hiển thị hộp thoại mở tệp tin
    file_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    # Kiểm tra xem người dùng có chọn ảnh hay không
    if file_path:
        # Đọc ảnh từ đường dẫn được chọn
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Làm mịn ảnh để loại bỏ nhiễu
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        # Tìm vật thể trong ảnh bằng phương pháp Canny edge detection
        edges = cv2.Canny(blur, 0, 100)

        # Tìm các vật thể liên thông trong ảnh
        contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        if len(contours) != 0:

            # Sắp xếp các contour theo diện tích giảm dần:
            area_cnt = [cv2.contourArea(cnt) for cnt in contours]
            area_sort = np.argsort(area_cnt)[::-1]

            cnt1 = contours[area_sort[0]]
            cnt2 = contours[area_sort[1]]
            
            img1 = changeAllBlack(image.copy(), (35,35,35))
            img2 = changeContourColor(image.copy(), cnt1, 30)
            img3 = changeContourColor(image.copy(), cnt2, -30)
            img_result1 = result1(img1.copy(), (255,0,0))
            img_result2 = result(img2.copy(), cnt1)
            img_result3 = result(img3.copy(), cnt2)

            # Convert images to arrays
            img = np.array(image.copy())
            img1 = np.array(img1)
            img2 = np.array(img2)
            img3 = np.array(img3)
            img_result1 = np.array(img_result1)
            img_result2 = np.array(img_result2)
            img_result3 = np.array(img_result3)
            # Stack arrays into one array
            global stacked_array
            stacked_array = [img, img1, img2, img3, img_result1, img_result2, img_result3]
            doShow()

def doShow():
    if len(stacked_array) != 0:
        global app
        if app != None: 
            app.setNewImages(stacked_array)
        else:
            app = ImageDisplay(root, stacked_array)
            
        photo = changeSize(stacked_array[0])
        global text_label_original
        global image_label_original
        image_label_original.config(image= photo)
        image_label_original.place(x= 10,y = (650 - photo.height())/2 - 10)
        image_label_original.image = photo
        
        text_label_original.config(text="Original Image")
        text_label_original.place(x = 300, y = (650 - photo.height())/2 - 40)
        

def main():

    # Thiết lập kích thước cho cửa sổ
    root.geometry("1300x650")
    root.configure(bg="gray")
    # Tạo một button để tải ảnh lên
    button = tk.Button(root, text="Load Image", command=loadOriginalImage)
    button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()