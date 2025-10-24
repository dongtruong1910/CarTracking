from ultralytics import YOLO
from collections import defaultdict
import src.utils as utils


class VehicleCounter:
    """
    Một lớp để thực hiện việc tracking và đếm xe.
    """

    def __init__(self, config):
        """
        Khởi tạo bộ đếm với các cài đặt từ file config.
        """
        model_cfg = config['model']
        line_cfg = config['counting_line']
        display_cfg = config['display']

        # 1. Tải model YOLO
        self.model = YOLO(model_cfg['name'])
        self.classes_to_count = model_cfg['classes']

        # 2. Cài đặt vạch đếm
        self.line_y = line_cfg['y_coordinate']
        self.line_color = tuple(line_cfg['color_bgr'])
        self.line_thickness = line_cfg['thickness']

        # 3. Cài đặt hiển thị
        self.count_color = tuple(display_cfg['count_text_color_bgr'])
        self.font_scale = display_cfg['font_scale']
        self.font_thickness = display_cfg['thickness']

        # 4. Biến lưu trữ trạng thái
        self.track_history = defaultdict(lambda: [])
        self.counted_ids = set()
        self.vehicle_count = 0

        # Màu sắc cho xe đi lên / đi xuống
        self.pass_color_up = (255, 0, 0)  # Xanh dương
        self.pass_color_down = (0, 255, 0)  # Xanh lá

    def process_frame(self, frame):
        """
        Xử lý một khung hình, thực hiện tracking và đếm.
        Trả về: Khung hình đã được chú thích (annotated_frame).
        """

        # 1. Chạy tracking
        results = self.model.track(frame, persist=True, classes=self.classes_to_count, verbose=False)

        if results[0].boxes.id is None:
            # Nếu không có đối tượng nào, chỉ vẽ vạch và số đếm
            annotated_frame = frame.copy()
        else:
            # Lấy khung hình đã được vẽ box + ID
            annotated_frame = results[0].plot()

            boxes = results[0].boxes.xywh.cpu()  # (x_center, y_center, w, h)
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # 2. Lặp qua các đối tượng đã track
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                center_y = int(y)  # Tọa độ Y của tâm

                # Cập nhật lịch sử vị trí
                track = self.track_history[track_id]
                track.append(center_y)
                if len(track) > 2:
                    track.pop(0)

                # 3. Logic đếm khi vượt qua vạch
                if track_id not in self.counted_ids and len(track) == 2:
                    prev_y = track[0]

                    # Đi từ trên xuống (vượt qua vạch)
                    if prev_y < self.line_y and center_y >= self.line_y:
                        self.vehicle_count += 1
                        self.counted_ids.add(track_id)
                        utils.draw_pass_event(annotated_frame, x, y, self.pass_color_down)

                    # Đi từ dưới lên (vượt qua vạch)
                    elif prev_y > self.line_y and center_y <= self.line_y:
                        self.vehicle_count += 1
                        self.counted_ids.add(track_id)
                        utils.draw_pass_event(annotated_frame, x, y, self.pass_color_up)

        # 4. Vẽ vạch đếm và tổng số xe
        utils.draw_counting_line(annotated_frame, self.line_y, self.line_color, self.line_thickness)
        utils.draw_vehicle_count(annotated_frame, self.vehicle_count, self.count_color, self.font_scale,
                                 self.font_thickness)

        return annotated_frame