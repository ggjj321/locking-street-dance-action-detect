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


def unit_vector(vector):
    # Returns the unit vector of the vector.
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    # Returns the angle in radians between vectors 'v1' and 'v2'::
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def errorcal(lmList):
    # use distance of two shoulders to estimate the error
    leftSide = np.array([lmList[12][1], lmList[12][2]])
    rightSide = np.array([lmList[11][1], lmList[11][2]])

    shoulderDistance = np.linalg.norm(leftSide - rightSide)

    return 0.08 * shoulderDistance + 36.4
    # actually measure linear equation


def putText(Action, pos, image):
    wordInterval = 0
    for move in Action:
        cv2.putText(image, move, (80 + pos, 100 + wordInterval),
                    cv2.FONT_HERSHEY_PLAIN,4, (255, 0, 0), 5)
        wordInterval += 70


class fundamental():
    def HandBesideWaist(self, lmList, rl):
        # hand beside waist
        if rl == 0:  # right
            pos = lmList[23][1] + 100  # follow the error
            if aboveJudge(lmList[19][1] - pos) and aboveJudge(
                    lmList[19][2] - lmList[23][2]):
                return True

        if rl == 1:  # left
            pos = lmList[24][1] - 100  # follow the error
            if 0 <= lmList[20][1] - pos <= 100 and \
                0 <= lmList[20][2] - lmList[24][2] <= 100:
                return True
        return False

    def HandShoulderElbow(self, lmList, rl):
        # hand at the shoulder, and shoulder has the same height with elbow
        if absJudge(lmList[19 + rl][1] - lmList[11 + rl][1]) and \
                absJudge(lmList[19 + rl][2] - lmList[11 + rl][2]):
            if absJudge(lmList[11 + rl][2] - lmList[13 + rl][2]):
                return True
        return False


class twirl(fundamental):
    def __init__(self, rl):
        super().__init__()
        self.moveList = [self.HandShoulderElbow, self.MidProcess,
                         self.HandOnShoulder, self.MidProcess,
                         self.HandShoulderElbow
                         ]
        self.moveStep = 0
        self.rl = rl
        self.name = 'twirl'

    def MidProcess(self, lmList, notuse):
        # twril's mid process
        shoulder = lmList[11 + self.rl][2] - 150  # follow the error
        if aboveJudge(lmList[19 + self.rl][2] - shoulder):
            return True
        return False

    def HandOnShoulder(self, lmList, notuse):
        # hand on the shoulder
        shoulder = lmList[11 + self.rl][2] - 100  # follow the error
        if aboveJudge(lmList[19 + self.rl][2] - shoulder):
            return True
        return False

    def judge(self, lmList):
        rl = self.rl
        if self.moveList[self.moveStep](lmList, rl):
            self.moveStep += 1
        if self.moveStep == 5:
            return True
        return False


class punch(fundamental):
    def __init__(self, rl):
        super().__init__()
        self.moveList = [self.HandShoulderElbow, self.ShoulderElbowHand,
                         self.HandShoulderElbow
                         ]
        self.moveStep = 0
        self.rl = rl
        self.name = 'punch'

    def ShoulderElbowHand(self, lmList, notuse):
        # shoulder,elbow and hand become a line
        pos = lmList[13 + self.rl][2] - 50
        if absJudge(lmList[19 + self.rl][2] - pos) and \
                absJudge(pos - lmList[11 + self.rl][2]):
            ShoulderCector = np.array([lmList[11 + self.rl][1] - lmList[13 + self.rl][1],
                                      lmList[11 + self.rl][2] - lmList[13 + self.rl][2]])
            HandVector = np.array([lmList[19 + self.rl][1] - lmList[13 + self.rl][1],
                                      lmList[19 + self.rl][2] - lmList[13 + self.rl][2]])
            angle = angle_between(ShoulderCector, HandVector) / np.pi * 180
            if 155 <= angle <= 180:
                return True
        return False

    def judge(self, lmList):
        rl = self.rl
        if self.moveList[self.moveStep](lmList, rl):
            self.moveStep += 1
        if self.moveStep == 3:
            return True
        return False


class muscleMan(fundamental):
    def __init__(self, rl):
        super().__init__()
        self.moveList = [self.HandBesideWaist, self.handAboveVertical]
        self.rl = rl
        self.name = 'Mman'
        self.moveStep = 0

    def handAboveVertical(self, lmList, notuse):
        ShoulderCector = np.array([lmList[11 + self.rl][1] - lmList[13 + self.rl][1],
                                   lmList[11 + self.rl][2] - lmList[13 + self.rl][2]])
        HandVector = np.array([lmList[19 + self.rl][1] - lmList[13 + self.rl][1],
                               lmList[19 + self.rl][2] - lmList[13 + self.rl][2]])
        angle = angle_between(ShoulderCector, HandVector) / np.pi * 180
        print(angle)
        if 80 <= angle <= 100:
            return True

    def judge(self, lmList):
        rl = self.rl
        if self.moveList[self.moveStep](lmList, rl):
            self.moveStep += 1
        if self.moveStep == 2:
            return True
        return False


class queue():  # It's a maintain 9 simple queue, not standard queue
    def __init__(self):
        self.qu = []

    def add(self, action):
        self.qu.append(action)
        if len(self.qu) >= 9:
            self.qu.pop(0)


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
RightMman = muscleMan(0)
LeftMnan = muscleMan(1)

RightSideObj = [Righttwirl, RightPunch, RightMman]
LeftSideObj = [Lefttwirl, LeftPunch, LeftMnan]

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

        cv2.rectangle(image, (1000, 50), (1200, 750), (255, 0, 0), 3)
        cv2.rectangle(image, (80, 50), (280, 750), (255, 0, 0), 3)


        if results.pose_landmarks:

            myBody = results.pose_landmarks
            for id, lm in enumerate(myBody.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            error = errorcal(lmList)

            for raction in RightSideObj:
                # print('Right', raction.name, raction.moveStep)
                if raction.judge(lmList):
                    RightSideAction.add(raction.name)
                    for zeroAction in RightSideObj:
                        zeroAction.moveStep = 0
            for laction in LeftSideObj:
                # print('left', laction.name, laction.moveStep)
                if laction.judge(lmList):
                    LeftSideAction.add(laction.name)
                    for zeroAction in LeftSideObj:
                        zeroAction.moveStep = 0

            putText(RightSideAction.qu, 920, image)
            putText(LeftSideAction.qu, 0, image)

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
