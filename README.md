# 🚀 Dự án Đếm và Theo dõi Xe cộ bằng YOLOv8

Đây là dự án sử dụng mô hình YOLOv8 của Ultralytics để phát hiện, theo dõi (tracking) và đếm số lượng xe cộ (ô tô, xe máy, xe buýt) đi qua một vạch đếm ảo được thiết lập trong video.

## 🌟 Tính năng

* **Phát hiện Đối tượng:** Sử dụng `yolov8m.pt` (bản medium) để phát hiện xe cộ.
* **Theo dõi Đa Đối tượng (Multi-Object Tracking):** Gán ID duy nhất cho mỗi chiếc xe và theo dõi chúng qua các khung hình.
* **Đếm xe qua vạch:** Đếm số lượng xe khi chúng đi qua một vạch ngang có thể tùy chỉnh.
* **Cấu trúc Code Sạch sẽ:** Tách biệt logic (`src/`), cấu hình (`configs/`), và dữ liệu mẫu (`samples/`).

---

## ❗ Yêu cầu Bắt buộc: Tải Video Đầu vào

Do giới hạn kích thước file của GitHub (100MB), file video demo (`input.mp4`) **không** được lưu trữ trực tiếp trên kho code này.

Để chạy dự án, bạn **bắt buộc** phải tải file video về và đặt vào đúng thư mục:

1.  Tải file **`input.mp4`** tùy chọn 

2.  Sau khi tải về, di chuyển file đó vào thư mục `samples/`.

3.  Cấu trúc thư mục cuối cùng của bạn phải trông như thế này:
    ```
    vehicle_counter_yolo/
    ├─ samples/
    │  └─ input.mp4   <-- (File bạn vừa tải về)
    ├─ src/
    ├─ configs/
    ├─ main.py
    └─ ...
    ```
