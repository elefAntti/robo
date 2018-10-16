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
            if (event.key == Qt.Key_Up && !event.isAutoRepeat)
            {
                backend.forward(false);
            }
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
}