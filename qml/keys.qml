import QtQuick 2.5
import QtQuick.Controls 1.1
//import QtCharts 2.0

ApplicationWindow
{
    id: window
    visible: true
    width: 1000
    height: 600
    Item
    {
        focus: true
        Keys.onPressed: 
        {
            if (event.key == Qt.Key_Up && !event.isAutoRepeat)
            {
                backend.forward('up', true);
            }
            if (event.key == Qt.Key_W && !event.isAutoRepeat)
                backend.forward('w', true);
            if (event.key == Qt.Key_A && !event.isAutoRepeat)
                backend.forward('a', true);
            if (event.key == Qt.Key_S && !event.isAutoRepeat)
                backend.forward('s', true);
            if (event.key == Qt.Key_D && !event.isAutoRepeat)
                backend.forward('d', true);
        }

        Keys.onReleased: 
        {
            if (event.key == Qt.Key_W && !event.isAutoRepeat)
                backend.forward('w', false);
            if (event.key == Qt.Key_A && !event.isAutoRepeat)
                backend.forward('a', false);
            if (event.key == Qt.Key_S && !event.isAutoRepeat)
                backend.forward('s', false);
            if (event.key == Qt.Key_D && !event.isAutoRepeat)
                backend.forward('d', false);
        }
    }
    Column
    {
    Row
    {
        Button
        {
            text: "Teleoperation"
            onClicked: backend.releaseManual(0)
        }

        Button
        {
            text: "Initial platform"
            onClicked: backend.releaseManual(1)
        } 

        Button
        {
            text: "Maze"
            onClicked: backend.releaseManual(2)
        }

        Button
        {
            text: "Bars"
            onClicked: backend.releaseManual(3)
        }

        Button
        {
            text: "Companion cube"
            onClicked: backend.releaseManual(4)
        }
        Button
        {
            text: "Discs of Doom"
            onClicked: backend.releaseManual(5)
        }
    }
    Row
    {
        Button
        {
            text: "Hack"
            onClicked: backend.releaseManual(666)
        }
    }
}
}