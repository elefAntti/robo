import QtQuick 2.5
import QtQuick.Controls 1.1
import QtCharts 2.0

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
                backend.forward(true);
            }
        }

        Keys.onReleased: 
        {
            if (event.key == Qt.Key_Up)
            {
                backend.forward(false);
            }
        }
    }
}