import QtQuick 2.5
import QtQuick.Controls 1.1
import QtCharts 2.0

ApplicationWindow {
    id: window
    visible: true
    width: 1000
    height: 600

    SignalPlot
    {
        title: "Ultrasonic (cm)"
        width: 400;
        height: 400;
        name1: "distance";
        value1: backend.measurement;
    }
}

