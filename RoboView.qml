import QtQuick 2.5
import QtQuick.Controls 1.1

Canvas
{
    width: 400;
    height: 400;
    id: robocanvas;

    property real robotX: 0;
    property real robotY: 0;
    property real robotHeading: 0;
    property real robotRadius: 0.25;
    
    property real mapXMin: -2.5;
    property real mapXMax: 2.5;
    property real mapYMin: -2.5;
    property real mapYMax: 2.5;

    onRobotHeadingChanged:
    {
        robocanvas.requestPaint();
    }

    onRobotXChanged:
    {
        robocanvas.requestPaint();
    }

    onRobotYChanged:
    {
        robocanvas.requestPaint();
    }

    function drawBackground(ctx)
    {
        ctx.save()

        ctx.lineWidth = 2 / width;
        ctx.strokeStyle = "gray";
        ctx.beginPath();
        ctx.moveTo(0, -1);
        ctx.lineTo(0, 1);
        ctx.stroke();
        ctx.moveTo(-1, 0);
        ctx.lineTo(1, 0);
        ctx.stroke();
        ctx.restore();
    }

    function drawRobot(ctx, x, y, h)
    {
        ctx.save();
        ctx.translate(robotX, robotY);
        ctx.rotate(robotHeading);
        ctx.scale(robotRadius, robotRadius);

        ctx.fillStyle = "light blue";
        ctx.lineWidth = 2 / width / robotRadius;
        ctx.strokeStyle = "blue";

        ctx.beginPath();
        ctx.rect(-0.75, -1.25, 1.5, 0.5);
        ctx.fill();
        ctx.stroke()

        ctx.beginPath();
        ctx.rect(-0.75, 0.75, 1.5, 0.5);
        ctx.fill();
        ctx.stroke()

        ctx.beginPath();
        ctx.arc(0, 0, 1.0, 0, Math.PI * 2.0, false);
        ctx.fill();
        ctx.stroke()

        ctx.beginPath();
        ctx.moveTo( 0.75, 0 );
        ctx.lineTo( 0.6, 0.15);
        ctx.lineTo( 0.6, -0.15);
        ctx.closePath();
        ctx.fillStyle = "blue";
        ctx.fill();

        ctx.restore();        
    }

    onPaint:
    {
        var ctx = getContext("2d");
        ctx.reset();
        ctx.save();
        var x_scale = width/(mapXMax - mapXMin)
        var y_scale = -height/(mapYMax - mapYMin)
        ctx.scale(x_scale, y_scale);
        ctx.translate(-mapXMin, mapYMin);
        drawBackground(ctx);
        drawRobot(ctx, robotX, robotY, robotHeading);
        ctx.restore();
    }
}