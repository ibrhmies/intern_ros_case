# intern_ros_case 🤖🧭 (TurtleBot3 Simulation – ROS Noetic)

> **ROS Noetic (ROS1)** için hazırlanmış örnek bir paket.  
> `bringup.launch` ile bir hareket düğümünü çalıştırır ve TurtleBot3’ü simülasyonda (veya hazır çalışan bir robot/sim ortamında) **parametrelerle ayarlanabilir** şekilde hareket ettirir.

![ROS](https://img.shields.io/badge/ROS-Noetic-blue)
![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04-E95420)
![Language](https://img.shields.io/badge/Language-Python-yellow)

---

## 📌 Proje Özeti

Bu pakette temel amaç:

- TurtleBot3’ü **basit bir hareket senaryosu** ile sürmek  
  (ör: ileri git → dur → belirli açıyla dön → dur).
- Hareketi **parametrelerle** kontrol etmek:
  - `linear_speed`
  - `angular_speed`
  - `forward_time`
  - `stop_time`
  - `turn_angle_deg`

---

## 🗂️ Repo Yapısı

Bu depo şu temel dosya/klasörleri içerir: :contentReference[oaicite:1]{index=1}

- `launch/` → `bringup.launch` (çalıştırma senaryosu)
- `src/` → Python düğümü(leri) (hareket kontrolü)
- `CMakeLists.txt` → catkin derleme dosyası
- `package.xml` → bağımlılıklar ve paket tanımı

---

## ✅ Gereksinimler

- Ubuntu 20.04
- **ROS Noetic**
- Python3
- TurtleBot3 simülasyonu kullanacaksan:
  - `turtlebot3` ve `turtlebot3_simulations` paketleri (Gazebo)

> Not: Simülasyonu bu repo başlatmıyorsa, önce TurtleBot3 Gazebo’yu ayrı terminalde açman gerekir (aşağıda var).

---

## 🚀 Kurulum

### 1) Catkin workspace içine klonla

```bash
mkdir -p ~/intern_ws/src
cd ~/intern_ws/src
git clone https://github.com/ibrhmies/intern_ros_case.git
cd ..
```

### 2) Bağımlılıkları yükle

```bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### 3) Derle ve source et

```bash
catkin_make
source devel/setup.bash
```

```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Çalıştırma

### TurtleBot3 Gazebo + bu paket (iki terminal)

#### Terminal 1 (Gazebo):

```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

#### Terminal 2 (intern_ros_case bringup.launch):

```bash
roslaunch intern_ros_case bringup.launch
```
