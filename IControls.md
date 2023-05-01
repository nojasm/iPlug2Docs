# IControls
**IControls** are elements can are displayed in the GUI and which the user can interact with. iPlug2 already has many IControls for knobs, buttons, etc. but you can always create your own elements.

# Developing own IControl elements
Developing your own IControls is relatively straightforward. Create a class, such as CustomKnobControl that inherits from the IControl class.
The constructor takes the bounds the elements should have and passes it to the `IControl` constructor. Additionally you can also pass parameters [(See this)](/README.md#parameters) and an action-function <sup>When is the action function called?</sup>.

```C++
class CustomKnobControl : public IControl {
public:
	CustomKnobControl(const IRECT& bounds) : IControl(bounds, {kParam1, kParam2, ...}, &Action) {
		// Initialize variables and other stuff here
	}
}
```

## Drawing using Draw()

Define the `Draw()` function for updating the elements visuals. It takes an `IGraphics&` object as a parameter.
The following function gets called when the IControl is set "dirty", see [SetDirty()](#setting-an-icontrol-dirty-using-setdirty).

Notice that the top left of the IControl element is not at (0/0) (except if the IControl is positioned at (0/0)). Instead the position is relative to the plugins window.

```C++
void Draw(IGraphics& g) {
	// Example: Draw a line from the top left to the bottom right of the IControl
	g.DrawLine(COLOR_RED, mRECT.L, mRECT.T, mRECT.R, mRECT.B)
}
```

## Setting an IControl dirty using SetDirty()
If an IControl is set dirty using the `SetDirty()` function in a function like `CustomKnobControl::OnMouseOver`, it means that the visuals will be updated on the next frame. Notice that `SetDirty()` takes a boolean parameter that has nothing to do with if the element should be set dirty or not. From the official docs: *If this [argument] is true and the control is linked to a parameter notify the class implementing the IEditorDelegate interface that the parameter changed. If this control has an ActionFunction, that can also be triggered.*


## Mouse Events
To use mouseover events, you first have to enable them in the layout function inside your plugin's constructor:
```C++
pGraphics->EnableMouseOver(true);
```

After enabling, you can define corresponding functions:

```C++
void OnMouseOver(float x, float y, const IMouseMod& m) {
	// ...

	// The documentation warns about using SetDirty in the OnMouseOver function
	// as it increases CPU usage redrawing every frame
	SetDirty(true);
}
```

## Action Function
ToDo

## List of all IControl Methods
ToDo
