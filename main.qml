import QtQuick 2.5
import QtQuick.Controls 1.1

ApplicationWindow {
    id: window
    visible: true
    width: 640
    height: 480

	Column
	{
		Row
		{
			Button
			{
				text: "Stop"
				onClicked: backend.stop()
			}
			Button
			{
				text: "Forward"
				onClicked: backend.forward()
			}
			Button
			{
				text: "Backward"
				onClicked: backend.backward()
			}
			Button
			{
				text: "Left"
				onClicked: backend.left()
			}
			Button
			{
				text: "Right"
				onClicked: backend.right()
			}
			Button
			{
				text: "Pivot left"
				onClicked: backend.pivotLeft()
			}
			Button
			{
				text: "Pivot right"
				onClicked: backend.pivotRight()
			}
		}

		RoboView
		{
			robotX: robot.x;
			robotY: robot.y;
			robotHeading: robot.heading;			
		}
	}
}

