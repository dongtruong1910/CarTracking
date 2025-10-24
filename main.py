import cv2
from src.counter import VehicleCounter
from src.utils import load_config
import os


def main():
    # 1. Tải cấu hình
    config_path = 'configs/config.yaml'
    config = load_config(config_path)
    if config is None:
        return

    video_cfg = config['video']

    # 2. Khởi tạo bộ đếm (Counter)
    counter = VehicleCounter(config)

    # 3. Mở nguồn video
    video_source = 0 if video_cfg['source'] == 'webcam' else video_cfg['source']
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Lỗi: Không thể mở nguồn video '{video_cfg['source']}'")
        return

    print("Đang xử lý video... Nhấn 'q' để thoát.")

    # 4. (Tùy chọn) Chuẩn bị file output nếu lưu video
    writer = None
    if video_cfg['save_output']:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Đảm bảo thư mục samples tồn tại
        os.makedirs(os.path.dirname(video_cfg['output_path']), exist_ok=True)
        writer = cv2.VideoWriter(video_cfg['output_path'], fourcc, fps, (frame_width, frame_height))

    # 5. Vòng lặp xử lý chính
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Hết video hoặc lỗi đọc frame.")
            break

        # 6. Xử lý khung hình
        annotated_frame = counter.process_frame(frame)

        # 7. Lưu và/hoặc Hiển thị kết quả
        if video_cfg['save_output'] and writer:
            writer.write(annotated_frame)

        if video_cfg['show_output']:
            cv2.imshow("Vehicle Counter", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 8. Dọn dẹp
    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

    print("--- HOÀN THÀNH ---")
    print(f"Tổng số xe đếm được: {counter.vehicle_count}")


if __name__ == "__main__":
    main()