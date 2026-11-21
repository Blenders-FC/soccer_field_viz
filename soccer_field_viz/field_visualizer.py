import rclpy
from rclpy.node import Node
import math
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point


class SoccerFieldVisualizer(Node):

    def __init__(self):
        super().__init__('soccer_field_visualizer')

        self.publisher = self.create_publisher(
            MarkerArray,
            '/soccer_field/markers',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_field)

    def create_line(self, marker_id, points):
        marker = Marker()

        marker.header.frame_id = 'map'
        marker.ns = 'field_lines'
        marker.id = marker_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD

        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.025

        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        for x, y in points:
            point = Point()
            point.x = x
            point.y = y
            point.z = 0.02
            marker.points.append(point)

        return marker

    def create_circle(self, marker_id, x, y, radius):
        marker = Marker()

        marker.header.frame_id = 'map'
        marker.ns = 'field_circles'
        marker.id = marker_id
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD

        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = 0.02
        marker.pose.orientation.w = 1.0

        marker.scale.x = radius * 2.0
        marker.scale.y = radius * 2.0
        marker.scale.z = 0.001

        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        return marker
    
    def create_center_circle(self, marker_id):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.ns = "soccer_field"
        marker.id = marker_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD

        # Center of the COLLADA mesh after its node transform
        center_x = 0.003
        center_y = -0.020
        radius = 0.56

        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.052
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        segments = 100

        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments

            point = Point()
            point.x = center_x + radius * math.cos(angle)
            point.y = center_y + radius * math.sin(angle)
            point.z = 0.011

            marker.points.append(point)

        return marker

    def publish_field(self):
        markers = MarkerArray()

        # Outer field boundary
        markers.markers.append(self.create_line(
            0,
            [
                (-3.0, -2.0),
                (3.0, -2.0),
                (3.0, 2.0),
                (-3.0, 2.0),
                (-3.0, -2.0)
            ]
        ))

        # Halfway line
        markers.markers.append(self.create_line(
            1,
            [(0.0, -2.0), (0.0, 2.0)]
        ))

        # Left penalty area
        markers.markers.append(self.create_line(
            2,
            [
                (-3.0, -1.5),
                (-2.4, -1.5),
                (-2.4, 1.5),
                (-3.0, 1.5)
            ]
        ))

        # Right penalty area
        markers.markers.append(self.create_line(
            3,
            [
                (3.0, -1.5),
                (2.4, -1.5),
                (2.4, 1.5),
                (3.0, 1.5)
            ]
        ))

        # Penalty marks and center point
        markers.markers.append(
            self.create_circle(0, -1.2, 0.0, 0.05)
        )

        markers.markers.append(
            self.create_circle(1, 1.2, 0.0, 0.05)
        )

        markers.markers.append(
            self.create_circle(2, 0.0, 0.0, 0.05)
        )

        markers.markers.append(self.create_center_circle(0))

        self.publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)

    node = SoccerFieldVisualizer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()