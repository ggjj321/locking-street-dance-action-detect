# locking (street dance) action detect

# function
This repository is an application with mediapipe.  
It can detect 4 different actions and sort left hand side move and right hand side move.

# Core concept
Mediapipe provides a trained model with body landmarks.  
Using it can detect the poses.   
Parting a action to different poses can achieve the function.  
Pose detect's cocept is to calculate the distance and angle of hand, shoulder , arm...and so.  
The method can be easily to define a pose.  
But it's defect is that the misjudge will occur when other action's process.  
For example, the highst frequency misjudgement is the Muscle Man's judge.  
Muscle Man's process need to raise hand.It's easy to achieve lock's angle.  
So the error need to be a small range.  
The advantage is that it can quickly to define a action.  
If you just want to detect one action , the method can quickly and precisely to detect.  
But you want to detect many actions and has higher fault tolerance,deep learning should be need.  


# package and python version
- opencv
- mediapipe
- numpy
- python3.7

# 4 actions
- Twirl
- Punch
- Lock
- Muscle Man

# demo
- twirl
![image](https://github.com/ggjj321/locking-street-dance-action-detect/blob/main/demo/MediaPipe%20Pose%202021-08-14%2012-47-42_Trim.gif)
- punch
![image](https://github.com/ggjj321/locking-street-dance-action-detect/blob/main/demo/MediaPipe%20Pose%202021-08-14%2012-45-33_Trim.gif)


