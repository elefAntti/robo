import QtQuick 2.5
import QtQuick.Controls 1.1
import QtCharts 2.0

ApplicationWindow {
    id: window
    visible: true
    width: 1000
    height: 600

	Row
	{
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
		Column
		{
			SignalPlot
			{
				title: "Wheel speed (rad/s)"
				width: 400;
				height: 400;
				name1: "left";
				value1: robot.leftWheelVel;
				name2: "right";
				value2: robot.rightWheelVel;
			}
		}
	}
}

