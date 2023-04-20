# iPlug2Docs
| An alternative iPlug2 Documentation
---

This documentation is aimed at beginners in audio,
C/C++ and iPlug2 development. It will only focus on developing VST3 plugins with the use of Visual Studio.

<span style="color: white; background-color: #f44; padding: 1px 7px; border-radius: 15px; text-transform: uppercase">unconfirmed</span>     This means that I am not sure if the following is correct.

(<span style="color: #999; font-style: italic">What does this do?</span>)      This means that everyone is free to open a pull request to answer my question.


# Getting started
To get started I recommend creating a `vst-dev` folder that will contain all your plugins as well as the `iPlug2` SDK, which you can simply clone from GitHub:
```sh
vst-dev/ $ git clone https://github.com/iPlug2/iPlug2
```

Visual Studio is the industry standard for C/C++ developing and also recommended in that case. We will use it to code, compile and debug our plugins all in one software.

After cloning, go into the `iPlug2` directory and pick `IPlugEffect` in the `Examples` folder. Double click the .sln (Visual Studio Solution) to open the corresponding Visual Studio Project.

## Other resources
- (iPlug2 Official API Docs - doxygen)[https://iplug2.github.io/docs/]
- (iPlug2 Official Wiki)[https://github.com/iPlug2/iPlug2/wiki]
- (iPlug2 Forum)[https://iplug2.discourse.group/]
- (iPlug2 Discord)[https://discord.gg/7h9HW8N9Ke]
- (Oli Larkin - An Introduction to iPlug2)[https://www.youtube.com/watch?v=YT_0TEftO54&t=290s] by The Audio Programmer

## Tipps and Tricks
In cases that you don't have a 100% done, handwritten, image-included documentation to hand, it can be useful to use Visual Studios tools like autocompletion, Go-To-Definition and Go-To-Declaration (Right click on variable).

# Files
Visual Studio shows our project files in the **Solution Explorer** (View -> Solution Explorer or CTRL+ALT+L). Note that sometimes the files are different than the ones shown in your normal file explorer, as VS treats files differently. In most cases everything works fine if the Solution Explorer shows them normally.

Set <your-plugin>-vst as a startup project in the Solution Explorer using a right click and "Set as Startup Project".

Extend the project to reveal all of the source files.

You should also set your Solution Configuration to "Debug" or "Trace" when developing and only switch it to "Release" when you actually plan to share the plugin somewhere. Make sure the Solution Platform is correct (You most likely use a an x64 device). You can find these options at the top of Visual Studio.

[Solution Configuration and Platform](res/sol-conf.png)

# A plugins structure
A plugin is divided into two parts: The UI and the digital signal processing (DSP).
They both run independent from each other and communicate through so called (Senders)[#Senders].


## config.h
As the name suggests, `config.h` is a configuration file containing `#define` statements for constant values. The `#define` keyword passes a constant to the compiler, which replaces it with the corresponding value in every file it compiles.



Let's take a look at the most important values.

| Name | Note |
| --- | --- |
| PLUG_NAME | The name of your plugin |
| PLUG_MFR | The manufacturer's name |
| PLUG_VERSION_HEX & PLUG_VERSION_STR | The version of your plugin in both hexadecimal and string format |
| PLUG_UNIQUE_ID | A unique identifier with the length of 4 characters |
| PLUG_MFR_ID | A unique identifier for the manufacturer, also with the length of 4 characters |
| PLUG_URL_STR | A link to your website |
| PLUG_EMAIL_STR | Your E-Mail address |
| PLUG_COPYRIGHT_STR | A copyright string |
| PLUG_CLASS_NAME | The name of the class the host (like your DAW) should use. Don't use quotations here |
| BUNDLE_NAME, BUNDLE_MFR and BUNDLE_DOMAIN | Three strings defining the bundle identifier. This is similar to the package name in app development. Often the website of the developer is used: dev.jondoe.myplugin1. It is used to uniquely identify each plugin, even if they have the same name |
| PLUG_CHANNEL_IO | <span style="color: white; background-color: #f44; padding: 1px 7px; border-radius: 15px; text-transform: uppercase">unconfirmed</span> Different options for input and output combinations seperated by a space. "1-1 2-2" means that you can either have 1 input, 1 output or 2 inputs, 2 outputs |
| PLUG_WIDTH & PLUG_HEIGHT | The width and height of your plugin in pixels |
| VST3_SUBCATEGORY | <span style="color: white; background-color: #f44; padding: 1px 7px; border-radius: 15px; text-transform: uppercase">unconfirmed</span> Not quite sure but I think (those are the ones)[https://steinbergmedia.github.io/vst3_doc/vstinterfaces/group__plugType.html] |
| ROBOTO_FN | The reference to the "Roboto Regular" font. See (fonts)[#fonts] |

## IPlugEffect.h
This file is a so called header file and holds all declarations. You can declare and define an object in one line (`int a = 42;`), but you can also declare it first (`int a;`) and define it later on (`a = 42;`). C/C++ developers like to declare their variables, enumerations and classes in headers files that end on `.h`. Sometimes, when working with C++, the extensions `.hpp` is used to show that C++ is used, but this is not the case here.

In the header file

## IPlugEffect.cpp
The first thing we do in our actual code is include the header file using `#include "IPlugEffect.h"`. This makes sure that all objects are already declared and ready to work with. We also include `IPlug_include_in_plug_src.h` (<span style="color: #999; font-style: italic">What does this do?</span>) as well as `IControls.h` which gives us some [control objects](#Using-IControls) to use.

### Constructor
The constructor is the starting point of every class, in our case `IPlugEffect`. This is also used to initialize the plugin, any variables, the UI and more.

`IPlugEffect.h` defines the **IPlugEffect** Class, a constructor with the same name (which is how you know that it's the constructor) and a function called `ProcessBlock` that will become important later on.

We use the double colon (::) operator to overwrite the constructor of the class. So we don't have to reinvent the wheel, there is another class, simply called **Plugin** that acts as an API to Steinbergs VST3 SDK and that we can inherit (Basically copy everything) from:

```C++
IPlugEffect::IPlugEffect(const InstanceInfo& info) : Plugin(info, MakeConfig(kNumParams, kNumPresets)) {
	// Initialize stuff in here
}
```

Notice that `kNumParams` and `kNumPresets` are defined in `config.h`.

Next, [parameters](#parameters) are defined.

After that,
See [this](https://github.com/iPlug2/iPlug2/wiki/Distributed-Plugins) to find out, why the next portion is wrapped inside `IPLUG_EDITOR`.

The next step is to write a lambda function that creates the UI Window. We pass the plugin's width and height, the FPS (<span style="color: #999; font-style: italic">Is this the MAX-FPS or the FPS the plugin should try to reach?</span>) as well as a scale factor (<span style="color: #999; font-style: italic">Didn't understand that one yet</span>).

```C++
mMakeGraphicsFunc = [&]() {
    return MakeGraphics(*this, PLUG_WIDTH, PLUG_HEIGHT, PLUG_FPS, GetScaleForScreen(PLUG_WIDTH, PLUG_HEIGHT));
  };
```

The final step is to initialize our UI with another lambda function. See [UI](#ui) for further details.

# UI
The UI is initialized in the `mLayoutFunc` function. It passes a **IGraphics\*** object which represents our plugin's window. Here any fonts are loaded, settings defined and, most importantly, elements attached to the window. Those elements are objects of type `IControl`. Drawing is often not done in this function by the way, as it only ones once when the plugin is started (<span style="color: #999; font-style: italic">Does it run when the plugin window is opened again?</span>). Instead the backend UI library **IGraphics** goes through each attached control and checks if it is `dirty`. If it is, it redraws it using the IControl's `Draw()` function and sets it back to `clean`.
For further information refer to [Using IControls](#using-icontrols).

If you want to add a knob for example, you can do it like this:
```C++
mLayoutFunc = [&](IGraphics* pGraphics) {
	// Add a corner resizer so we can easily resize the window
    pGraphics->AttachCornerResizer(EUIResizerMode::Scale, false);

	// Set the background color to COLOR_GRAY (127, 127, 127)
	pGraphics->AttachPanelBackground(COLOR_GRAY);

	// Load font, use name "Roboto-Regular" to reference it and load it from ROBOTO_FN ("Roboto-Regular.ttf")
    pGraphics->LoadFont("Roboto-Regular", ROBOTO_FN);

	// Get the bounds of the window
    const IRECT b = pGraphics->GetBounds();

	// Create a new IVKnobControl knob and attach it to the window
	// GetCentredInside(100) centers the object inside the current window with a width of 100 pixels
	// GetVShifted(-100) shifts the object down up on the virtual axis (up = 0px, down = PLUG_HEIGHTpx)
    pGraphics->AttachControl(new IVKnobControl(b.GetCentredInside(100).GetVShifted(-100)));
  };
```

In the original code we also pass `kGain` to the function. We do this so the plugin knows that the knob represents this parameter. `kGain` is defined in `IPlugEffect.h` in **EParams** and just translates to an integer (0) that is used as a kind of ID for the parameter. See [Parameters](#parameters) for more.

# DSP

# Parameters
A parameter is a value of a certain type that can be changed by the host DAW, the plugin itself or the user tweaking knobs on the UI.

Every parameter should be defined by a unique integer > -1. We use an enumeration to do define parameters, which has the advantage of `kNumParams` always being correct:

```C++
enum EParams
{
  kGain = 0,
  kOtherParameter,
  ...
  kNumParams
};
```

After that we have to initialize the parameter in the constructor of our plugin:
```
GetParam(kGain)->InitDouble("Gain", 0.0, 0.0, 100.0, 0.01, "%");
```

---

Every **Init** function takes similar parameters:

| Parameter | Type | Notes |
| --- | --- | --- |
| name | const char* |  |
| defaultValue | Depends | The value the parameter should have when starting the plugin or reseting the value |
| minVal | number |  |
| maxVal | number |  |
| step | number | The size of individual steps when turning the knob. Should be relatively small to not 'stutter' |
| listItems | List of const char* | Only used in InitEnum: A list of strings to use as options |
| label | const char* | A suffix for the parameter. Something like "%", "s" or "ms" or whatever |
| flags | const char* | Defines additional information, such as if the parameter can be automated. See [EFlags](#eflags) |
| group | const char* | (<span style="color: #999; font-style: italic">Heellpp what are groups?</span>)

---

All initializer functions are:

| Function | Notes |
| --- | --- |
| InitBool |  |
| InitEnum | Don't pass options, but only the number of options it will have using *nEnums* |
| InitEnum | Just pass `{"Option 1", "Option 2", ..}` as the value for listItems |
| InitInt |  |
| InitDouble |  |
| InitSeconds |  |
| InitMilliseconds |  |
| InitFrequency |  |
| InitPitch |  |
| InitGain |  |
| InitPercentage |  |
| InitAngleDegrees |  |
| Init | Initialized the parameter based on another parameter |

---

Copied straight from `IPlugParameter.h` in the source:

```
void InitBool(const char* name, bool defaultValue, const char* label = "", int flags = 0, const char* group = "", const char* offText = "off", const char* onText = "on");
void InitEnum(const char* name, int defaultValue, int nEnums, const char* label = "", int flags = 0, const char* group = "", const char* listItems = 0, ...);
void InitEnum(const char* name, int defaultValue, const std::initializer_list<const char*>& listItems, int flags = 0, const char* group = "");
void InitInt(const char* name, int defaultValue, int minVal, int maxVal, const char* label = "", int flags = 0, const char* group = "");
void InitDouble(const char* name, double defaultVal, double minVal, double maxVal, double step, const char* label = "", int flags = 0, const char* group = "", const Shape& shape = ShapeLinear(), EParamUnit unit = kUnitCustom, DisplayFunc displayFunc = nullptr);
void InitSeconds(const char* name, double defaultVal = 1., double minVal = 0., double maxVal = 10., double step = 0.1, int flags = 0, const char* group = "");
void InitMilliseconds(const char* name, double defaultVal = 1., double minVal = 0., double maxVal = 100., int flags = 0, const char* group = "");
void InitFrequency(const char* name, double defaultVal = 1000., double minVal = 0.1, double maxVal = 10000., double step = 0.1, int flags = 0, const char* group = "");
void InitPitch(const char* name, int defaultVal = 60, int minVal = 0, int maxVal = 128, int flags = 0, const char* group = "", bool middleCisC4 = false);
void InitGain(const char* name, double defaultVal = 0., double minVal = -70., double maxVal = 24., double step = 0.5, int flags = 0, const char* group = "");
void InitPercentage(const char* name, double defaultVal = 0., double minVal = 0., double maxVal = 100., int flags = 0, const char* group = "");
void InitAngleDegrees(const char* name, double defaultVal = 0., double minVal = 0., double maxVal = 360., int flags = 0, const char* group = "");
void Init(const IParam& p, const char* searchStr = "", const char* replaceStr = "", const char* newGroup = "");
```

<span style="border: 1px solid #ccc; border-radius: 15px; padding: 30px">
We can pass our parameters to functions like `pGraphics->AttachControl(..., kGain)` to show that the parameter is representing that particular control. (<span style="color: #999; font-style: italic">What effects does this have?</span>)
</span>

# Senders
- ISender
- ISenderData

# Fonts
- Recommended to load as image

# Debugging
- Trace
- VST3PluginTestHost

# Misc

## IPattern
Todo

## IColor
You can create a new color using the `IColor` function. Notice that this is a function, not a class, that doesn't need the *new* operator. Also notice that the colors are in format `IColor(alpha, red, green, blue)`.

There are several predefined color constants, like COLOR_RED, COLOR_WHITE, and so on, defined in `IGraphics/IGraphicsStructs.h`.

## IRECT
Todo

## Drawing functions
Todo

## EFlags
Todo

# Using IControls
Todo
