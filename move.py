import cv2
import mediapipe as mp
import numpy as np


def aboveJudge(num):
    if 0 <= num <= error:
        return True
    return False


def absJudge(num):
    if abs(num) <= error:
        return True


def errorcal(lmList):
    # use distance of two shoulders to estimate the error
    leftSide = np.array([lmList[12][1], lmList[12][2]])
    rightSide = np.array([lmList[11][1], lmList[11][2]])

    shoulderDistance = np.linalg.norm(leftSide - rightSide)

    print(0.08 * shoulderDistance + 36.4, shoulderDistance)
    return 0.08 * shoulderDistance + 36.4
    # actually measure linear equation


class fundamental():
    def HandBesideWaist(self, lmList, rl):
        # hand beside waist
        if rl == 0:  # right
            pos = lmList[23][1] + 50  # follow the error
            if aboveJudge(lmList[19][1] - pos) and aboveJudge(
                    lmList[19][2] - lmList[23][2]):
                return True

        if rl == 1:  # left
            pos = lmList[24][1] - 50  # follow the error
            if aboveJudge(lmList[20][1] - pos) and aboveJudge(
                    lmList[20][2] - lmList[24][2]):
                return True
        return False

    def HandShoulderElbow(self, lmList, rl):
        # hand at the shoulder, and shoulder has the same height with elbow
        if absJudge(lmList[19 + rl][1] - lmList[11 + rl][1]) and absJudge(lmList[19 + rl][2] - lmList[11 + rl][2]):
            if absJudge(lmList[11 + rl][2] - lmList[13 + rl][2]):
                return True
        return False


class twirl(fundamental):
    def __init__(self, rl):
        super().__init__()
        self.moveList = []
        self.rl = rl

    def MidProcess(self, lmList):
        # twril's mid process
        shoulder = lmList[11 + self.rl][2] - 150  # follow the error
        if aboveJudge(lmList[19 + self.rl][2] - shoulder):
            return True
        return False

    def HandOnShoulder(self, lmList):
        # hand on the shoulder
        shoulder = lmList[11 + self.rl][2] - 100  # follow the error
        if aboveJudge(lmList[19 + self.rl][2] - shoulder):
            return True
        return False

    def judge(self, lmList):
        if self.HandBesideWaist(lmList, self.rl):
            self.moveList = [1]
            # cv2.putText(image, "1", (45, 375), cv2.FONT_HERSHEY_PLAIN,
            #             10, (255, 0, 0), 25)
        if self.HandShoulderElbow(lmList, self.rl):
            if 2 not in self.moveList:
                self.moveList.append(2)
            # if 3 in self.moveList:
            #     cv2.putText(image, "6", (45, 375), cv2.FONT_HERSHEY_PLAIN,
            #                 10, (255, 0, 0), 25)
            # else:
            #     cv2.putText(image, "2", (45, 375), cv2.FONT_HERSHEY_PLAIN,
            #                 10, (255, 0, 0), 25)
        if self.MidProcess(lmList):
            if 3 not in self.moveList:
                self.moveList.append(3)
            # cv2.putText(image, "3", (45, 375), cv2.FONT_HERSHEY_PLAIN,
            #             10, (255, 0, 0), 25)
            if 4 in self.moveList:
                self.moveList.append(5)
                # cv2.putText(image, "5", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                #             10, (255, 0, 0), 25)
        if 3 in self.moveList and self.HandOnShoulder(lmList) and 5 not in self.moveList:
            if 4 not in self.moveList:
                self.moveList.append(4)
            # cv2.putText(image, "4", (45, 375), cv2.FONT_HERSHEY_PLAIN,
            #             10, (255, 0, 0), 25)
        for i in range(1, 6):
            if i not in self.moveList:
                return False
        self.moveList = []
        return True


class punch(fundamental):
    def __init__(self, rl):
        super().__init__()
        self.moveList = []
        self.rl = rl
    def ShoulderElbowHand(self, lmList):
        # shoulder,elbow and hand become a line
        pos = lmList[13 + self.rl][2] - 50
        if absJudge(lmList[19 + self.rl][2] - pos) and \
                absJudge(pos - lmList[11 + self.rl][2]):
            if not self.HandShoulderElbow(lmList, self.rl):
                return True
        return False

    def judge(self, lmList):
        if self.HandBesideWaist(lmList, self.rl):
            self.moveList = [1]
            cv2.putText(image, "1", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 25)
        if self.HandShoulderElbow(lmList, self.rl):
            if 2 not in self.moveList:
                self.moveList.append(2)
            if 3 in self.moveList:
                cv2.putText(image, "4", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 25)
                if 4 not in self.moveList:
                    self.moveList.append(4)
            else:
                cv2.putText(image, "2", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 25)
        if self.ShoulderElbowHand(lmList):
            if 2 not in self.moveList:
                self.moveList.append(3)
            cv2.putText(image, "3", (45, 375), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 25)
        for i in range(1, 5):
            if i not in self.moveList:
                return False
        self.moveList = []
        return True


class queue():

    def __init__(self):
        self.qu = []

    def add(self, action):
        self.qu.append(action)
        if len(self.qu) >= 9:
            self.qu.pop(0)

def putText(Action ,pos, image):
    wordInterval = 0
    for move in Action:
        cv2.putText(image, move, (80 + pos, 200 + wordInterval), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 0, 0), 5)
        wordInterval += 70

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

error = 0

# For webcam input:
wCam, hCam = 1280, 960

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# action define
Righttwirl = twirl(0)
Lefttwirl = twirl(1)
RightPunch = punch(0)
LeftPunch = punch(1)

RightSideAction = queue()
LeftSideAction = queue()

with mp_pose.Pose(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lmList = []

        cv2.rectangle(image, (1000, 100), (1200, 800), (255, 0, 0), 3)
        cv2.rectangle(image, (80, 100), (280, 800), (255, 0, 0), 3)


        if results.pose_landmarks:

            myBody = results.pose_landmarks
            for id, lm in enumerate(myBody.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            error = errorcal(lmList)

            print(RightPunch.moveList)

            if Righttwirl.judge(lmList):
                RightSideAction.add("twirl")
            if Lefttwirl.judge(lmList):
                LeftSideAction.add("twirl")
            if RightPunch.judge(lmList):
                RightSideAction.add("punch")
            if LeftPunch.judge(lmList):
                LeftSideAction.add("punch")

            putText(RightSideAction.qu, 920, image)
            putText(LeftSideAction.qu, 0, image)

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()