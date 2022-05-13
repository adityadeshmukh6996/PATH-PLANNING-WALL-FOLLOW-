FROM ros:noetic-robot
MAINTAINER Benjamin Staehle <staehle@rwu.de>
ENV ROS_DISTRO noetic
ENV DEBIAN_FRONTEND noninteractive
ENV TURTLEBOT3_MODEL burger


RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update


RUN apt-get update && apt-get -y install vim gazebo11 ros-$ROS_DISTRO-gazebo-plugins python-pytest ros-$ROS_DISTRO-turtlebot3 ros-$ROS_DISTRO-turtlebot3-simulations ros-$ROS_DISTRO-rviz ros-$ROS_DISTRO-turtlebot3-slam ros-$ROS_DISTRO-slam-gmapping ros-$ROS_DISTRO-dwa-local-planner

RUN sed -i '3 c\  <xacro:arg name="laser_visual" default="true"/>' /opt/ros/$ROS_DISTRO/share/turtlebot3_description/urdf/turtlebot3_burger.gazebo.xacro


# create catkin_ws
RUN source /opt/ros/$ROS_DISTRO/setup.bash && \
    mkdir -p ~/catkin_ws/src && \
    cd /root/catkin_ws/src && \
    catkin_init_workspace    && \
    cd /root/catkin_ws && \
    export TURTLEBOT3_MODEL=burger && \
    catkin_make    && \
    echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc && \
    source ~/.bashrc
