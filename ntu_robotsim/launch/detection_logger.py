#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yolo_msgs.msg import DetectionArray
from collections import Counter
from datetime import datetime
import os

# ── CONFIG ───────────────────────────────────────────────────────────────────
LOG_DIR = "/home/ntu-user/ros2_ws/src/NTU_COMP30271_CW_RobotSim/detection_logs"
MIN_CONF = 0.5   # only log detections above this confidence
# ─────────────────────────────────────────────────────────────────────────────

class DetectionLogger(Node):

    def __init__(self):
        super().__init__('detection_logger')

        # Create log directory
        os.makedirs(LOG_DIR, exist_ok=True)

        # Create log file with timestamp in name
        timestamp     = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(LOG_DIR, f"detections_{timestamp}.txt")

        # Write header
        with open(self.log_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write(f"  YOLO Detection Log\n")
            f.write(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"  Min Conf: {MIN_CONF}\n")
            f.write("=" * 60 + "\n\n")

        self.subscription = self.create_subscription(
            DetectionArray,
            '/detections',
            self.detection_cb,
            10
        )

        # Session totals
        self.session_counts = Counter()
        self.total_frames   = 0

        print(f"Detection Logger started")
        print(f"Logging to: {self.log_path}")
        print(f" Press Ctrl+C to stop and save summary\n")

    def detection_cb(self, msg):

        if not msg.detections:
            return

        # Filter by confidence
        detections = [d for d in msg.detections if d.score >= MIN_CONF]
        if not detections:
            return

        self.total_frames += 1
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        class_list = [d.class_name for d in detections]
        counts = Counter(class_list)

        # Update session totals
        self.session_counts.update(class_list)

        # Build log entry
        lines = []
        lines.append(f"[{timestamp}] Frame #{self.total_frames} — {len(detections)} object(s) detected")

        for i, detection in enumerate(detections):
            lines.append(
                f"  [{i+1}] {detection.class_name:<20} "
                f"conf={detection.score:.2f}  "
                f"bbox=({detection.bbox.center.position.x:.0f}, {detection.bbox.center.position.y:.0f})  "
                f"size={detection.bbox.size.x:.0f}x{detection.bbox.size.y:.0f}"
            )

        lines.append(f"  Summary: { ', '.join(f'{k}:{v}' for k, v in sorted(counts.items())) }")
        lines.append("")

        # Print to terminal
        for line in lines:
            print(line)

        # Write to log file
        with open(self.log_path, 'a') as f:
            f.write("\n".join(lines) + "\n")

    def save_summary(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = []
        summary.append("\n" + "=" * 60)
        summary.append(f"  SESSION SUMMARY")
        summary.append(f"  Ended   : {timestamp}")
        summary.append(f"  Frames  : {self.total_frames}")
        summary.append(f"  Total detections: {sum(self.session_counts.values())}")
        summary.append("")
        summary.append("  Count per class:")
        for class_name, count in sorted(self.session_counts.items()):
            summary.append(f"    {class_name:<20} : {count}")
        summary.append("=" * 60)

        for line in summary:
            print(line)

        with open(self.log_path, 'a') as f:
            f.write("\n".join(summary) + "\n")

        print(f"\nLog saved to: {self.log_path}")


def main(args=None):
    rclpy.init(args=args)
    node = DetectionLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.save_summary()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
