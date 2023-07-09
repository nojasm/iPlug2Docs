# Your First iPlug2 Project
Your first iPlug2 project won't be Serum 2 or the next Autotune. In fact, as you will find out later, it won't be anything groundbraking at first. Before this documentation, there was close to no true documentation.

iPlug2 is still popular, but not as popular as the official VST SDK. And of course, even the official SDK by Steinberg is just a niche thing, most people to this day develop their plugins in JUCE - which also has it's limitation due to a company sitting behind it. There is also the option of using a plugin creator program, like SynthEdit of course.
However, as your experience grows, you will find old documents and old forum entries of 2010, of people having developed just the algorithm or piece of code you need. You will have to get used to it.

# Getting started
The recommended way of getting started is to first download newest release of the iPlug2 library: [iPlug2 Releases](https://github.com/iPlug2/iPlug2/tags).
After that, you have to download Python, a scripting programming language, that will help you by executing a small piece of code: [Install Python from here](https://www.python.org/downloads/).

Put the downloaded iPlug2 folder somewhere. I personally have a folder called "C:/MyProjects/VST". In this are subfolders, one of them being iPlug2 and the others being plugins. The iPlug2 folder contains the code of the library, examples, a rough documentation and more.

Open the windows terminal ("CMD"). Navigate to the folder at "C:/MyProjects/VST/iPlug2/Examples". In this folder, there is duplicate.py, a Python script that duplicates a project and prepares some things like names and variables for us. In the console, run "python duplicate.py". This will show us a help message on how to use the script. On example would be "python duplicate.py iPlugEffect myNewPlugin myCompany ..\..\". This duplicates the iPlugEffect project (A simple gain plugin) to a location at ..\..\, which is `C:\MyProjects\VST` or whatever, with the name and manufacturer name of "myNewPlugin" and "myCompany". After the script finished, you can close the terminal.

You can then access the plugin by going into the folder and opening the .sln solution file for Visual Studio. This opens up Visual Studio, with everything already set up.

You should have Visual Studio installed of course.

`iPlugEffect` is the simplest example project with just a message and a gain knob. In Visual Studio, you can see different plugin types on the right, like VST2, VST3 and so on. Right click on VST3 and set the project as a startup project. Then open up the folder.

[Here](https://github.com/nojasm/iPlug2Docs#files) you can find out more about what all the files do in that folder.

# Going through the code
Lets look at every part of the code to understand it.

```C++
#include "myEffect.h"
#include "IPlug_include_in_plug_src.h"
#include "IControls.h"
```

includes various files needed, among other things, there is "myEffect.h". Take a look at this file and you can see that it just defines some stuff. We will come to that later.

The `myEffect` constructor defines both all of the parameters used, like knobs and toggle switches as well as a function called mLayoutFunc (We don't need mMakeGraphicsFunc for now). mLayoutFunc gets called as the plugin's window opens. In this function we place knobs in the form IControls (see [Using IControls](https://github.com/nojasm/iPlug2Docs#using-icontrols)