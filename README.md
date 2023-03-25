# ImageProcessing_Midterm
Chương trình viết bằng py, có sử dụng một số thư viện của py trong quá trình viết.
Sau khi clone code về chạy chương trình chính (midterm.py)
Tast 1:
- Sử dụng 2 thuật toán là lọc màu theo ngưỡng và tìm viền bằng canny để xây dựng 3 mức độ xử lý.
- Mức 1: 
  + Sử dụng thuật toán lọc màu theo ngưỡng để lọc màu đen ra khỏi ảnh, sau đó thay thế bằng 1 màu bất kì.
  + Thuật toán được viết ở hàm changeAllBlack(image, color): image là ảnh gốc truyền vào, color là màu dùng để thay thế màu đen. (trong bài sử dụng màu xám)
 - Mức 2:
  + Sử dụng thuật toán Canny edge detection để tìm viền và lấy ra các vùng vật thể trong ảnh. Dùng findContours trong openCV để lấy ra các vùng đó. (được viết khi load ảnh gốc lên trong hàm loadOriginalImage())
  + Sau đó từ vùng sẽ được lấy ra để thay đổi màu sắc tạo ra mức độ tiếp theo của bài toán.
  + Màu sắc ở đây được là tất cả các điểm ảnh được duyệt qua và được tăng (giảm) độ sáng của màu sắc đó.
 - Mức 3: 
  + Từ mức độ 2, vùng contour được chọn sẽ được thu nhỏ theo tỉ lệ (hàm resizeContour(contour) ) và thay đổi màu sắc tạo ra mức độ khó hơn cho bài toán.
  + Màu sắc ở đây được là tất cả các điểm ảnh được duyệt qua và được tăng (giảm) độ sáng của màu sắc đó.
  + Có thể dịch chuyển cả contour được chọn nhưng dễ gây khó khăn cho người chơi nên em chỉ thu nhỏ lại và đặt trong lòng vật thể ban đầu.
Tast 2:
- Kết quả được show ngay ở trong chương trình khi xem xong 3 mức độ xử lý.
- Với mức 1 thì kết quả được đưa ra là 1 dòng chữ, thêm vào đó là màu sắc được thay đổi rõ ràng hơn.
- Với mức 2 và 3 thì kết quả sẽ được vẽ 1 hình chữ nhật bao quanh điểm khác biệt đó.
