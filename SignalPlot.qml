import QtQuick 2.5
import QtQuick.Controls 1.1
import QtCharts 2.0


ChartView
{
    //title: "Line"
    width: 300
    height: 200
    antialiasing: true

    property string name1: "";
    property string name2: "";
    property real value1: 0;
    property real value2: 0;
    property real timeWindow: 10.0;
    property real refreshInterval: 0.5;


    ValueAxis {
        id: axisX
        min: 0
        max: 10
        tickCount: 5
    }

    ValueAxis {
        id: axisY
        min: 0
        max: 1
        tickCount: 5
    }

    LineSeries {
        name: name1;
        id: myseries;
        axisX: axisX;
        axisY: axisY;
    }

    LineSeries {
        name: name2;
        id: myseries2;
        axisX: axisX;
        axisY: axisY;
    }

    Timer
    {
        interval: refreshInterval * 1000.0
        running: true
        repeat: true
        property real startTime: new Date().getTime();

        onTriggered: 
        {
            var time = new Date().getTime();
            var deltaTime = (time - startTime)/1000.0;
            myseries.append(deltaTime, value1);
            myseries2.append(deltaTime, value2);

            axisX.max=deltaTime;
            axisX.min=deltaTime - timeWindow;
            axisY.max=Math.max(value1, axisY.max);
            axisY.min=Math.min(value1, axisY.min);
            axisY.max=Math.max(value2, axisY.max);
            axisY.min=Math.min(value2, axisY.min);
        }
    }
}