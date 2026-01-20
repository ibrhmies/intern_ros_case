#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class RobotMoveNode:
    def __init__(self):
        # Params değerleri sonradan değiştirebiliriz
        self.linear_speed = rospy.get_param("~linear_speed", 0.2)
        self.angular_speed = rospy.get_param("~angular_speed", 0.5)
        self.forward_time  = rospy.get_param("~forward_time", 5.0)
        self.stop_time     = rospy.get_param("~stop_time", 1.0)
        self.turn_angle_deg= rospy.get_param("~turn_angle_deg", 90.0)

        #90 derece dönmek için kaç saniye dönmem gerekiyor formülü
        self.turn_time = math.radians(self.turn_angle_deg) / abs(self.angular_speed)

        self.cmd_publisher_ = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.odom_subscriber_ = rospy.Subscriber("/odom", Odometry, self.odom_cb)

        self.asama = 0
        self.asama_baslangic = rospy.Time.now()

        self.son_yazdirma = rospy.Time(0)

        rospy.on_shutdown(self.on_shutdown)
        rospy.loginfo("robot_move_node baslatildi.")

    def odom_cb(self, msg: Odometry):
        # X, Y
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Quaternion’dan yaw açısını bulmak z ekseni etrafındaki dönüşü
        q = msg.pose.pose.orientation
        roll, pitch, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

        # terminale X Y Yaw çıktılarının basılması
        now = rospy.Time.now()
        if (now - self.son_yazdirma).to_sec() >= 0.2:
            rospy.loginfo("X: %.2f | Y: %.2f | Yaw: %.2f rad", x, y, yaw)
            self.son_yazdirma = now

    def publish_cmd(self, lin_x: float, ang_z: float):
        msg = Twist()
        msg.linear.x = lin_x
        msg.angular.z = ang_z
        self.cmd_publisher_.publish(msg)

    def on_shutdown(self):
        # Robotu durdur
        self.publish_cmd(0.0, 0.0)

    def gorev_yap(self):
        gecen_sure = (rospy.Time.now() - self.asama_baslangic).to_sec()

        # ileri doğru 5 saniye ilerle
        if self.asama == 0:
            self.publish_cmd(self.linear_speed, 0.0)
            if gecen_sure >= self.forward_time:
                self.asama = 1
                self.asama_baslangic = rospy.Time.now()

        # robotu 1 sn durdur
        elif self.asama == 1:
            self.publish_cmd(0.0, 0.0)
            if gecen_sure >= self.stop_time:
                self.asama = 2
                self.asama_baslangic = rospy.Time.now()

        # robotu 90 derece döndür
        elif self.asama == 2:
            self.publish_cmd(0.0, self.angular_speed)
            if gecen_sure >= self.turn_time:
                self.asama = 3
                self.asama_baslangic = rospy.Time.now()

        # robotu durdur
        elif self.asama == 3:
            self.on_shutdown()

def main():
    rospy.init_node("robot_move_node", anonymous=False)
    node = RobotMoveNode()
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        node.gorev_yap()
        rate.sleep()

if __name__ == "__main__":
    main()