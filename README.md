# ImageProcessing_Midterm
Chương trình viết bằng py, có sử dụng một số thư viện của py trong quá trình viết.
Sau khi clone code về chạy chương trình chính (midterm.py)
Tast 1:
- Sử dụng 2 thuật toán là lọc màu theo ngưỡng và tìm viền bằng canny để xây dựng 3 mức độ xử lý.
- Mức 1: 
  + Sử dụng thuật toán lọc màu theo ngưỡng để lọc màu đen ra khỏi ảnh, sau đó thay thế bằng 1 màu bất kì.
  + Thuật toán được viết ở hàm changeAllBlack(image, color): image là ảnh gốc truyền vào, color là màu dùng để thay thế màu đen.
 - Mức 2:
  + Sử dụng thuật toán Canny edge detection để tìm viền và lấy ra các vùng vật thể trong ảnh. Dùng findContours trong openCV để lấy ra các vùng đó. (được viết khi load ảnh gốc lên trong hàm loadOriginalImage())
  + Sau đó từ vùng sẽ được lấy ra để thay đổi màu sắc tạo ra mức độ tiếp theo của bài toán.
 - Mức 3: 
  + Từ mức độ 2, vùng contour được chọn sẽ được thu nhỏ theo tỉ lệ và thay đổi màu sắc tạo ra mức độ khó hơn cho bài toán
Tast 2:
- Kết quả được show ngay ở trong chương trình khi xem xong 3 mức độ xử lý.
