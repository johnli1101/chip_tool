import {fabric} from 'fabric';
// import CanvasHistory from "./canvasHistory";

export default (function () {
    let drag;
    //let shape;
    let color;
    let lineWidth, fillCircle, angle,shapeId;
    let strokeDashArray;
    let borderRadius;
    let properties;
    //let isDown = false;

    function Shape(canvas, params) {
        //let draggable = false;
        // if (!draggable) {
        //     drag = false;
        //     console.log("Wow");
        //     return Shape;
        // }
        // if (color && color !== params.stroke) {
        //     color = params.stroke;
        //     shape = type;
        //     new Shape(canvas, true, shape, params)
        //     return Shape;
        // }
        // if ((shape && shape !== type)) {
        //     shape = type;
        //     drag = true;
        //     new Shape(canvas, true, shape, params)
        //     return Shape;
        // }
        properties = params;
        if (properties) {
            fillCircle = properties.fill;
            color = properties.stroke;
            lineWidth = properties.strokeWidth;
            angle = properties.angle;
            strokeDashArray = properties.strokeDashArray;
            borderRadius = properties.borderRadius;
            shapeId = properties.id
        }
        this.canvas = canvas;
        this.className = 'Shape';
        this.isDrawing = false;
        this.origX = 0;
        this.origY = 0;

        drag = true;
        //shape = type;
        console.log("Hello");
        this.bindEvents();
    }

    Shape.prototype.bindEvents = function () {
        console.log("What")
        let inst = this;
        console.log(inst);
        console.log("I'm in");
        document.onkeydown = (e) => {
            if ( e.keycode === 46) {
                inst.canvas.getActiveObjects().forEach((obj) => {
                    inst.canvas.remove(obj)
                });
            }
            inst.canvas.renderAll()
        };
        inst.selectable = true;
        inst.canvas.off('mouse:down');

        inst.canvas.on('mouse:down', function (o) {
            inst.onMouseDown(o);
        });
        inst.canvas.on('mouse:move', function (o) {
            inst.onMouseMove(o);
        });
        inst.canvas.on('mouse:up', function (o) {
            inst.onMouseUp(o);
        });
        inst.canvas.on('object:moving', function () {
            inst.disable();
        });


    };
    Shape.prototype.onMouseUp = function () {
        //isDown = false;
        let inst = this;
        if (!inst.isEnable()) {
            return;
        }
        if (drag) {
            inst.canvas.getObjects().forEach(function (object, index, array) {
                if (index === (array.length - 1)) {
                    if (inst.canvas.getActiveObject() && inst.canvas.getActiveObject()._objects && inst.canvas.getActiveObject()._objects.length > 1) {
                        inst.canvas.setActiveObject(object);

                    }
                }
            });
            if (inst.canvas.getActiveObject()) {
                inst.canvas.getActiveObject().hasControls = false;
                inst.canvas.getActiveObject().hasBorders = false;
                inst.canvas.getActiveObject().lockMovementX = true;
                inst.canvas.getActiveObject().lockMovementY = true;
                inst.canvas.getActiveObject().lockUniScaling = true;
            }
            inst.canvas.renderAll();
        }
        // let canvasProperties = {width:inst.canvas.width,height:inst.canvas.height}
        // let currentCanvas = { json: inst.canvas.toJSON(),canvas: canvasProperties};
        // new CanvasHistory(inst.canvas,currentCanvas)
        inst.disable();

    };
    Shape.prototype.onMouseMove = function (o) {
        let inst = this;
        if (!inst.isEnable()) {
            return;
        }
        inst.canvas.selection = false;
        let pointer = inst.canvas.getPointer(o.e);
        let activeObj;
        if (inst.canvas.getActiveObject()) {
            activeObj = inst.canvas.getActiveObject();
            activeObj.stroke = color;
            activeObj.strokeWidth = lineWidth;
            activeObj.id = shapeId;
            activeObj.fill = fillCircle;
            activeObj.noScaleCache = false;
            activeObj.strokeUniform = true;
        }
        if (this.origX > pointer.x) {
            activeObj.set({
                left: Math.abs(pointer.x)
            });
        }
        if (this.origY > pointer.y) {
            activeObj.set({
                top: Math.abs(pointer.y)
            });
        }
        // if (shape == "rect") {
            activeObj.set({
                width: Math.abs(this.origX - pointer.x),
                height: Math.abs(this.origY - pointer.y),
            });
        // }
        activeObj.setCoords();
        inst.canvas.renderAll();
    };

    Shape.prototype.onMouseDown = function (o) {
        console.log("Hello I'm down");
        //isDown = true;
        let inst = this;
        // if (!drag) {

        //     if (inst.canvas.getActiveObject()) {
        //         inst.canvas.getActiveObject().hasControls = shape === 'line' ? false : true;
        //         inst.canvas.getActiveObject().hasBorders = shape === 'line' ? false : true;
        //         inst.canvas.getActiveObject().lockMovementX = false;
        //         inst.canvas.getActiveObject().lockMovementY = false;
        //         inst.canvas.getActiveObject().lockUniScaling = false;
        //         inst.canvas.renderAll();
        //     }
        //     inst.disable();
        //     return;
        // }
        inst.enable();

        if (inst.canvas.getActiveObject()) {
            inst.canvas.getActiveObject().hasControls = false;
            inst.canvas.getActiveObject().hasBorders = false;
            inst.canvas.getActiveObject().lockMovementX = true;
            inst.canvas.getActiveObject().lockMovementY = true;
            inst.canvas.getActiveObject().lockUniScaling = true;
            inst.canvas.renderAll();
        }
        let pointer = inst.canvas.getPointer(o.e);
        this.origX = pointer.x;
        this.origY = pointer.y;
        // if (shape === "rect") {
            let rect = new fabric.Rect({
                left: this.origX,
                top: this.origY,
                originX: 'left',
                originY: 'top',
                width: pointer.x - this.origX,
                height: pointer.y - this.origY,
                angle: angle,
                fill: fillCircle,
                transparentCorners: false,
                stroke: color,
                strokeWidth: lineWidth,
                strokeDashArray: strokeDashArray,
                rx: borderRadius,
                ry: borderRadius,
                id: shapeId
            });
            inst.canvas.add(rect).setActiveObject(rect);
            console.log("Hello");
            console.log(inst.canvas);
        // }
    };
    Shape.prototype.isEnable = function () {
        return this.isDrawing;
    }

    Shape.prototype.enable = function () {
        this.isDrawing = true;
    }

    Shape.prototype.disable = function () {
        this.isDrawing = false;
    }
    return Shape;
}());