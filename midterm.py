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
def changeContourColor(image, n_contour, contour, change):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Khởi tạo contour mask zero
    mask = np.zeros(gray.shape, np.uint8)
    n_mask = np.zeros(gray.shape, np.uint8)
    # Vẽ contour trên back ground mask zero
    cv2.drawContours(mask,[contour],0,255,-1)
    cv2.drawContours(n_mask,[n_contour], 0, 255, -1)

    # dùng hàm cv2.findNoneZero() lấy ra toàn bộ các points có giá trị khác 0 là các điểm ở trong contour
    pixel = cv2.findNonZero(mask)
    n_pixel = cv2.findNonZero(n_mask)
    # chuyển ảnh từ BGR sang HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # lăp qua tất cả điểm ở trong contour, lấy màu của điểm đó (dạng HSV) rồi thay đổi 1 chút.(change)
    for i in range(len(n_pixel)):
        h, s, v = hsv[pixel[i][0][1], pixel[i][0][0]]
        hsv[n_pixel[i][0][1], n_pixel[i][0][0]] = np.clip([h,s,v + change], 0, 255)
    
    # chuyển ảnh về dạng BRG rồi return lại ảnh
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
def resizeContour(contour):
    # # Chuyển contour đến vị trí mới
    # M = np.float32([[1, 0, -50], [0, 1, 10]])  # Tạo ma trận chuyển đổi 2D
    # # Dùng hàm transform để chuyển đổi tọa độ của các điểm trong contour
    # contour_transformed = cv2.transform(contour, M)

    # Lấy contour đầu tiên và tính toán hình dạng của nó
    M = cv2.moments(contour)
    cx = int(M['m10'] / M['m00']) #tổng tọa độ x chia cho diện tích
    cy = int(M['m01'] / M['m00']) #tổng tọa độ y chia cho diện tích

    # Tính toán tỉ lệ thu nhỏ và tạo ma trận biến đổi
    scale_percent = 0.5 # tỉ lệ thu nhỏ
    M = cv2.getRotationMatrix2D((cx, cy), 0, scale_percent)

    # Áp dụng ma trận biến đổi để thu nhỏ contour
    contour_transformed = cv2.transform(contour, M)
    return contour_transformed

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
def findDifference(image1, image2):
    #Grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    #find the difference
    diff = cv2.absdiff(gray1, gray2)

    #Apply threshold
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    #Dilation
    kernel = np.ones((7,7), np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    #Find contours
    contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    max_area = cv2.contourArea(contours[0])
    max_contour = contours[0]

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contour = cnt

    x, y, w, h = cv2.boundingRect(max_contour)
    cv2.rectangle(image2, (x, y), (x+w, y+h), (0,0,255), 2)
    return image2
def resultForChangeContourColor(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)
    return image

def resultForChangeAllBlack(image, color):
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
            if len(contours) == 1:
                cnt2 = cnt1
            else:
                cnt2 = contours[area_sort[1]]
            doChange(image, cnt1, cnt2)
            
            
def doChange(image, cnt1, cnt2):
    img1 = changeAllBlack(image.copy(), (35,35,35))
    img2 = changeContourColor(image.copy(), cnt1, cnt1, -30)
    img3 = changeContourColor(image.copy(), resizeContour(cnt2), resizeContour(cnt2), -10)
    img_result1 = resultForChangeAllBlack(img1.copy(), (255,0,0))
    img_result2 = resultForChangeContourColor(img2.copy(), cnt1)
    img_result3 = resultForChangeContourColor(img3.copy(), resizeContour(cnt2))

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