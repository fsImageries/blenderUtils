# Usage

This Add-on is a collection of multiple smaller operators worked into panels for easy ui handling.  
The panels are all marked with the title "BpyUtils" for easy recognition.  

## Operators

### pose.pose_snap
__Works on selected pose bones.__  
  
This operator copies the world matrix of a pose bone into one or more bones local matrices, achieving a bone snap without in pose mode.  
It uses the currently active pose bone as target for the other selected pose bones.  
You can check off the use of translation, rotation and scale separately.  
__This operator is present at the 3d view's pose mode panel.__
  
  
### node.auto_aov
__Works on renderLayer and fileoutput nodes.__  
  
This operator is used to create a aov ready fileoutput node automatically.  
It takes the first render layer it finds or a selected one if checked and connects its outputs to a fileoutput node.  
OpenEXR Multi-Layered is used as format and the path given by the render properties is going to be used as output.  
__This operator is present in the nodeeditor's view panel.__  
__In there you can also update an already existing fileoutput node, given the aov's used changed.__









