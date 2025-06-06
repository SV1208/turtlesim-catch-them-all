#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from functools import partial
from my_robot_interfaces.msg import Turtle, TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from turtlesim.srv import Kill
from std_srvs.srv import Empty

class TurtleControllerNode(Node): 
    def __init__(self):
        super().__init__("turtle_controller") 
        self.declare_parameter("catch_closet_turtle_first", True)
        self.catch_closet_turtle_first_ = self.get_parameter("catch_closet_turtle_first").value

        self.turtle_to_catch_ = None

        self.pose_ = None
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)
        self.pose_subscriber_ = self.create_subscription(
            Pose, "turtle1/pose", self.callback_turtle_pose, 10)
        
        self.alive_turtles_subscriber_ = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles, 10)
        
        self.clear_path = self.create_client(Empty, '/clear')
        
        self.control_loop_timer_ = self.create_timer(0.01, self.control_loop)

    def callback_turtle_pose(self, msg):
        self.pose_ = msg

    def callback_alive_turtles(self, msg):
        if len(msg.turtles) > 0:
            if self.catch_closet_turtle_first_:
                closest_turtle = None
                closest_turtle_distance = None
                for turtle in msg.turtles:
                    dist_x = turtle.x - self.pose_.x
                    dist_y = turtle.y - self.pose_.y
                    distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)

                    if (closest_turtle_distance==None or distance<closest_turtle_distance):
                        closest_turtle = turtle
                        closest_turtle_distance = distance

                self.turtle_to_catch_ = closest_turtle
            else:
                self.turtle_to_catch_ = msg.turtles[0]

    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            return
        
        dist_x = self.turtle_to_catch_.x - self.pose_.x
        dist_y = self.turtle_to_catch_.y - self.pose_.y
        distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)

        msg = Twist()

        if distance > 0.5:
            # position
            msg.linear.x = 2*distance

            # orientation
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - self.pose_.theta

            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi

            msg.angular.z = 6*diff
        else:
            # Reached
            msg.linear.x = 0.0
            msg.linear.z = 0.0
            self.call_catch_turtle_server(self.turtle_to_catch_.name)
            self.turtle_to_catch_=None

        self.cmd_vel_publisher_.publish(msg)
    
    def call_catch_turtle_server(self, turtle_name):
        client = self.create_client(CatchTurtle, 'catch_turtle')
        while not client.wait_for_service(1):
            self.get_logger().warn("waiting for server...")
        
        request = CatchTurtle.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle,turtle_name = turtle_name))

    def callback_call_catch_turtle(self, future, turtle_name):
        try:
            response = future.result()
            if not response:
                self.get_logger().error("Turtle "+str(turtle_name)+" could not be caught")
            else:
                self.get_logger().info("Caught the turtle: "+str(turtle_name))
                while not self.clear_path.wait_for_service(1):
                     self.get_logger().info('Waiting for /clear service...')
                
                request = Empty.Request()
                future = self.clear_path.call_async(request)
                future.add_done_callback(self.callback_clear_path)
        except Exception as e:
            self.get_logger().error("service failed: %r"%(e,))
    
    def callback_clear_path(self, future):
        response = future.result()
        if response:
            self.get_logger().info("Cleared the path")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()