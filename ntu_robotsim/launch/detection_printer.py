#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yolo_msgs.msg import DetectionArray
from collections import Counter
import os

class DetectionPrinter(Node):

    def __init__(self):
        super().__init__('detection_printer')
        self.subscription = self.create_subscription(
            DetectionArray,
            '/detections',
            self.detection_cb,
            10
        )
        self.get_logger().info("Detection Printer started, listening to /detections...")

    def detection_cb(self, msg):

        if not msg.detections:
            return

        # Count detections per class
        class_list = [d.class_name for d in msg.detections]
        counts = Counter(class_list)

        # Clear terminal for clean output
        os.system('clear')

        print("=" * 50)
        print("        YOLO Live Detections")
        print("=" * 50)
        print(f"  Total objects detected: {len(msg.detections)}\n")

        # Per detection info
        print("📦 Detections:")
        for i, detection in enumerate(msg.detections):
            print(f"\n  [{i+1}] Class      : {detection.class_name} (ID: {detection.class_id})")
            print(f"       Confidence : {detection.score:.2f}")
            print(f"       BBox center: x={detection.bbox.center.position.x:.1f}, y={detection.bbox.center.position.y:.1f}")
            print(f"       BBox size  : {detection.bbox.size.x:.1f} x {detection.bbox.size.y:.1f} px")

        # Count summary
        print("\n" + "=" * 50)
        print("Count per Class:")
        for class_name, count in sorted(counts.items()):
            print(f"   {class_name:<20} : {count}")
        print("=" * 50)


def main(args=None):
    rclpy.init(args=args)
    node = DetectionPrinter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
