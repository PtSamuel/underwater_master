import pygame
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

class JoystickPublisherNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.publisher = self.create_publisher(Joy, "joystick", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.xbox = pygame.joystick.Joystick(0)
            self.xbox.init()
            print("Joystick detected")
        else: 
            self.xbox = None
            print("Joystick not found")

    def timer_callback(self):

        if self.xbox != None:
            pygame.event.get()
            axes = [self.xbox.get_axis(i) for i in range(self.xbox.get_numaxes())]
            buttons = [self.xbox.get_button(i) for i in range(self.xbox.get_numbuttons())]
            self.get_logger().info(f"axes: {axes}, buttons: {buttons}")
        else:
            axes = []
            buttons = []
            
        message = Joy()
        message.axes = axes
        message.buttons = buttons
        self.publisher.publish(message)
        self.get_logger().info("Publishing joystick message")
    
def main(args=None):
    rclpy.init(args=args)
    node = JoystickPublisherNode("joystick_publisher_node")
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()
    # simple fuckup:
    # colcon build --merge-install --packages-select joystick_publisherpuyhjon