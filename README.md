# locking (street dance) action detect

# function
This repository is an application with mediapipe.  
It can detect 4 different actions and sort left hand side move and right hand side move.
idea from <https://www.youtube.com/watch?v=9iEPzbG-xLE&t=1621s>

# Core concept
Mediapipe provides a trained model with body landmarks.  
Using it can detect the poses.   
Parting a action to different poses can achieve the function.  
Pose detect's cocept is calculating the distance and angle of hand, shoulder , arm...and so.  
The method can easily define a pose.  
But it's defect is that the misjudge will occur during other action's process.  
For example, the highst frequency misjudgement is the Muscle Man's judge.  
Muscle Man's process need to raise hand.It's easy to achieve lock's angle.  
So the error need to be a small range.  
The advantage is that quickly define a action.  
If you just want to detect one action , the method can quickly and precisely detect.  
But you want to detect many actions and has higher fault tolerance,deep learning should be need.  


# install package and python version
I recommend to use PyCharm , and use the PyCharm's settings to install the packages.
![image](https://github.com/ggjj321/locking-street-dance-action-detect/blob/main/demo/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%20(39).png)
## packages
- opencv
- mediapipe
- numpy
## python version
- python3.7

# 4 actions
- Twirl
- Punch
- Lock
- Muscle Man

# demo

![image](https://github.com/ggjj321/locking-street-dance-action-detect/blob/main/demo/MediaPipe%20Pose%202021-08-21%2013-14-16_Trim_Trim.gif)


