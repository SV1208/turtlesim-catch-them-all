## 📚 About the Project

This project was completed as part of the **Turtlesim Catch Them All** exercise featured in the "[ROS 2 for Beginners](https://www.udemy.com/course/ros2-for-beginners/)" course by **Edouard Renard** on Udemy.

It demonstrates how to spawn multiple turtles in the `turtlesim` simulator and catch them with another turtle using ROS 2 launch files, subscribers, publishers, and simple logic to "catch" targets.

## 🎥 Demo Video

Check out the video of this project here:  

[![Demo Thumbnail](https://img.youtube.com/vi/qsUvp61ZfWY/0.jpg)](https://www.youtube.com/watch?v=qsUvp61ZfWY)


## Installation

1.  Create a ROS 2 workspace (if you haven't already):
    ```bash
    mkdir  ~/ros2_ws/src
    cd ~/ros2_ws
    ```

2.  Place all the above package files within a `src` directory inside your ROS 2 workspace:

3.  Navigate back to the root of your ROS 2 workspace:
    ```bash
    cd ~/ros2_ws
    ```

4.  Build the package using `colcon`:
    ```bash
    colcon build
    ```

5.  Source the environment setup script:
    ```bash
    source install/setup.bash
    ```

## Usage

To launch the `turtlesim_catch_them_all` example, execute the following command:

```bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.py
```
