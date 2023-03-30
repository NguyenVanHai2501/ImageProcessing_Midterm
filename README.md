# ImageProcessing_Midterm
Chương trình viết bằng py, có sử dụng một số thư viện của py trong quá trình viết.
Sau khi clone code về chạy chương trình chính (midterm.py)
* Tast 1:
- Sử dụng 2 thuật toán là lọc màu theo ngưỡng và tìm viền bằng canny để xây dựng 3 mức độ xử lý.
- Mức 1: 
  + Sử dụng thuật toán lọc màu theo ngưỡng để lọc màu đen ra khỏi ảnh, sau đó thay thế bằng 1 màu bất kì.
  + Thuật toán được viết ở hàm changeAllBlack(image, color): image là ảnh gốc truyền vào, color là màu dùng để thay thế màu đen. (trong bài sử dụng màu xám)
  + Example 1: (input bên trái, ouput bên phải)
    <img width="948" alt="image" src="https://user-images.githubusercontent.com/82854095/228606893-d00cb130-f998-4f6f-9f0e-5e22102c6228.png">
  + Trong ví dụ trên, khi đưa ra đáp án em đổi màu sao cho sự thay đổi rõ ràng nhất
 - Mức 2:
  + Sử dụng thuật toán Canny edge detection để tìm viền và lấy ra các vùng vật thể trong ảnh. Dùng findContours trong openCV để lấy ra các vùng đó. (được viết khi load ảnh gốc lên trong hàm loadOriginalImage())
    •	Sau khi đọc ảnh, ảnh được chuyển qua màu xám, được làm mịn bởi thuật toán GaussianBlur(gray, (9, 9), 0) của OpenCv.
    •	Sau đó áp dụng thuật toán canny edge detection lên ảnh đã được làm mờ để tìm ra viền của ảnh.
    •	Dùng thuật toán findContours của OpenCV để tìm kiếm các vật thể là vùng liên thông trong ảnh.
    •	Sau đó lấy ra 2 vùng lớn nhất để thực hiện sự thay đổi trên chúng.
  + Sau đó từ vùng sẽ được lấy ra để thay đổi màu sắc tạo ra mức độ tiếp theo của bài toán.
  + Màu sắc ở đây được là tất cả các điểm ảnh được duyệt qua và được tăng (giảm) độ sáng của màu sắc đó.
  + Hàm changeContourColor(image, n_contour, contour, change) thực hiện việc thay đổi màu sắc:
    •	Tham số truyền vào là ảnh gốc (image) , 1 contour mới (n_contour) là vùng contour sau khi thực hiện phép biến đổi (thu nhỏ, dịch chuyển) contour ban đầu, 1 contour ban đầu (contour) và 1 số nguyên là độ lệch màu của màu cũ so với màu mới (change).
    •	Hàm sẽ chuyển ảnh sang màu xám, sau đó tạo 2 mask có màu đen trên ảnh xám ban đầu.
    •	Sau đó sẽ vẽ vùng contour và n_contour với màu trắng trên mask và n_mask đó.
    •	Sau đó dùng hàm findNonZero(mask) thuộc OpenCV để tìm ra tất cả các điểm có giá trị khá 0 (khác màu đen) trên mask và n_mask. => Ta được tập hợp tất cả các điểm ở trong vật thể đó.
    •	Sau đó chuyển ảnh sang dạng hsv để dễ dàng xử lý.
    •	Duyệt qua tất cả điểm ảnh trong n_contour (n_pixel), lấy giá trị màu ở vùng contour cũ (pixel) rồi gán lại giá trị màu đó với 1 chút thay đổi cho vùng n_contour.
    •	Cuối cùng convert lại thành dạng BGR rồi return ảnh đã thay đổi.
  + Example 2: (input bên trái, output bên phải)
    <img width="948" alt="image" src="https://user-images.githubusercontent.com/82854095/228608212-a803a6e3-8e32-4eb0-bde3-1ea10693d18b.png">
  + trong ví dụ trên, kết quả được đánh dấu bằng hình chữ nhật màu đỏ.
 - Mức 3: 
  + Từ mức độ 2, vùng contour được chọn sẽ được thu nhỏ theo tỉ lệ (hàm resizeContour(contour) ) và thay đổi màu sắc tạo ra mức độ khó hơn cho bài toán.
  + Màu sắc ở đây được là tất cả các điểm ảnh được duyệt qua và được tăng (giảm) độ sáng của màu sắc đó.
  + Có thể dịch chuyển cả contour được chọn nhưng dễ gây khó khăn cho người chơi nên em chỉ thu nhỏ lại và đặt trong lòng vật thể ban đầu.
  + Example 3: (input bên trái, output bên phải)
    <img width="940" alt="image" src="https://user-images.githubusercontent.com/82854095/228608790-bdbc5e01-f807-4dc1-8dde-aa407862afa6.png">

  + trong ví dụ trên, kết quả được đánh dấu bằng hình chữ nhật màu đỏ.
* Tast 2:
- Kết quả được show ngay ở trong chương trình khi xem xong 3 mức độ xử lý.
- Với mức 1 thì kết quả được đưa ra là 1 dòng chữ, thêm vào đó là màu sắc được thay đổi rõ ràng hơn.
  + hàm resultForChangeAllBlack(image, color) sẽ nhận vào ảnh gốc và 1 màu sắc để thay đổi màu đen của ảnh gốc sang màu mới để người dùng dễ nhận ra điểm khác biệt hơn.
- Với mức 2 và 3 thì kết quả sẽ được vẽ 1 hình chữ nhật bao quanh điểm khác biệt đó.
  + Hàm resultForChangeContourColor(image, contour) sẽ nhận vào ảnh sau biến đổi và 1 vùng contour là vùng thay đổi trong ảnh so vs ảnh gốc.
  + Sau đó hàm sẽ vẽ 1 hình chữ nhật bao quanh vùng contour đó và trả về hình ảnh sau khi vẽ.
# Trong bài có từng thử cách tìm kết quả bằng việc thực hiện thuật toán để tìm sự khác biệt giữa 2 ảnh nhưng sự thay đổi là quá nhỏ so với ảnh gốc nên việc tìm kiếm sự khác biệt giữa 2 ảnh đôi lúc bị nhầm lẫn.

* Cách sử dụng:
- Chương trình viết bằng py, có sử dụng một số thư viện của py trong quá trình viết.
- Sau khi clone code về chạy chương trình chính (midterm.py)
  + Một màn hình tương tác hiện lên, người dùng có thể ấn nút "Load Image" để tải ảnh từ máy tính cá nhân. ( Lưu ý: Ảnh phải là một trong các định dạng .jpg, .jpeg hoặc .png. Nếu không chương trình sẽ lỗi và ảnh không được load lên)
  + Sau khi ảnh được load thành công, ảnh gốc sẽ được show ở bên trái (có tiêu đề là "Original Image").
  + Người dùng ấn nút "View" để xem các mức độ thay đổi của hình ảnh sau khi xử lý. Ảnh được xử lý sẽ show ở bên phải màn hình với tiêu đề là các Level từ 1 đến 3.
  + Ấn "Next Level" để xem các level tiếp theo.
  + Sau khi xem 3 Level thì sẽ show ra các kết quả của từng ảnh.
  + Ấn nút "Next Result" để xem các kết quả tiếp theo của từng Level.
  + Sau khi xem 3 kết quả thì sẽ lại quay lại 3 ảnh được xử lý.
  + Trong quá trình sử dụng có thể thay đổi ảnh khác bằng cách lại nút "Load Image"

