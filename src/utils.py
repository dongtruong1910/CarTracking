import cv2
import yaml

def load_config(config_path):
    """Tải file cấu hình YAML."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file config tại '{config_path}'")
        return None

def draw_counting_line(frame, y_coord, color, thickness):
    """Vẽ vạch đếm ngang trên khung hình."""
    frame_width = frame.shape[1]
    cv2.line(frame, (0, y_coord), (frame_width, y_coord), color, thickness)

def draw_vehicle_count(frame, count, color, font_scale, thickness):
    """Hiển thị tổng số xe đếm được."""
    cv2.putText(frame, f"Vehicle Count: {count}", (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

def draw_pass_event(frame, center_x, center_y, color=(0, 255, 0)):
    """Vẽ một vòng tròn nhỏ khi xe đi qua vạch."""
    cv2.circle(frame, (int(center_x), int(center_y)), 5, color, -1)