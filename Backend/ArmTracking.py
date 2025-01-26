import cv2
import mediapipe as mp
import numpy as np
import time
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

def track_arm_rom():
    highest_angle_right = 0
    highest_angle_left = 0
    hold_start_time_right = None
    hold_start_time_left = None
    hold_duration = 3
    angle_threshold = 15
    cap = cv2.VideoCapture(0)

    # Ensure output folder exists
    output_folder = "ROM_Captures"
    os.makedirs(output_folder, exist_ok=True)

    print("Position yourself. Tracking will start in 5 seconds.")
    buffer_start = time.time()
    while time.time() - buffer_start < 5:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, f"Starting in {5 - int(time.time() - buffer_start)}...", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv2.imshow("Arm Angle Tracker", frame)
        if cv2.waitKey(10) & 0xFF == 27:
            print("Exiting during setup.")
            cap.release()
            cv2.destroyAllWindows()
            return None

    print("Tracking started.")
    final_angle_right = None
    final_angle_left = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


            arm_angle_right = calculate_angle(right_hip, right_shoulder, right_wrist)
            arm_angle_left = calculate_angle(left_hip, left_shoulder, left_wrist)

              # right arm

            if arm_angle_right > highest_angle_right:
                highest_angle_right = arm_angle_right
                hold_start_time_right = time.time()

            if highest_angle_right - arm_angle_right <= angle_threshold:
                if hold_start_time_right and (time.time() - hold_start_time_right >= hold_duration):
                    final_angle_right = int(highest_angle_right)
                    print(f"ROM: {final_angle_right}° from starting position (right arm.)")

                    # Take a photo and save it
                    timestamp_right = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"ROM_{final_angle_right}_degrees_{timestamp_right}.jpg"
                    file_path = os.path.join(output_folder, filename)
                    cv2.imwrite(file_path, frame)
                    print(f"Photo saved: {file_path}")

                    cap.release()
                    cv2.destroyAllWindows()
                    return final_angle_right
            else:
                hold_start_time_right = None

            
              # left arm

            if arm_angle_left > highest_angle_left:
                highest_angle_left = arm_angle_left
                hold_start_time_left = time.time()

            if highest_angle_left - arm_angle_left <= angle_threshold:
                if hold_start_time_left and (time.time() - hold_start_time_left >= hold_duration):
                    final_angle_left = int(highest_angle_left)
                    print(f"ROM: {final_angle_left}° from starting position (left arm.)")

                    # Take a photo and save it
                    timestamp_left = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"ROM_{final_angle_left}_degrees_{timestamp_left}.jpg"
                    file_path = os.path.join(output_folder, filename)
                    cv2.imwrite(file_path, frame)
                    print(f"Photo saved: {file_path}")

                    cap.release()
                    cv2.destroyAllWindows()
                    return final_angle_left
            else:
                hold_start_time_left = None


            

            cv2.putText(image, f'Right Arm Angle: {int(arm_angle_right)} deg', (800, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            cv2.putText(image, f'Left Arm Angle: {int(arm_angle_left)} deg', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            h, w, _ = image.shape
            for point in [right_shoulder, right_hip, right_wrist]:
                cv2.circle(image, (int(point[0] * w), int(point[1] * h)), 10, (0, 255, 0), -1)

            for point in [left_shoulder, left_hip, left_wrist]:
                cv2.circle(image, (int(point[0] * w), int(point[1] * h)), 10, (0, 0, 255), -1)

        cv2.imshow("Arm Angle Tracker", image)
        key = cv2.waitKey(10)
        if key == 27:
            print("Exiting program (ESC).")
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    print("Failed to capture ROM.")
    return None

  # remove this after
track_arm_rom()