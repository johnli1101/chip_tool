<template>
    <div>
        Hello
        <canvas id='c1'></canvas>
    </div>
</template>

<script>
    import {fabric} from 'fabric';
    import Shape from './Shape'

    export default {
        name: 'PaintTool',
        props: {
            canvasWidth: {
                type: [String, Number]
                ,require: true
            },
            canvasHeight: {
                type: [String, Number]
                ,require: true
            },

        },
        components: {
            
        },
        computed: {

        },
        data: () => ({
            canvas: {}
        }),
        mounted() {
            this.canvas = new fabric.Canvas("c1");
            this.canvas.setDimensions({width: this.canvasWidth, height: this.canvasHeight});
            this.canvas.backgroundColor = "#fff";
            //var rectangle, isDown, origX, origY;
            let params = {
                fill: 'transparent',
                stroke: 'red',
                strokeWidth: 3,
                angle: 0,
                width: null,
                height: null,
                top: 0,
                left: 0,
                opacity: 1,
                strokeUniform: true,
                noScaleCache: false,
                strokeDashArray: false,
                borderRadius: 0,
                id: '',
            };

            console.log("Hello");
            new Shape(this.canvas, params);

            // this.canvas.on('mouse:down', function(o){
            //     var pointer = this.canvas.getPointer(o.e);

            //     isDown = true;
            //     origX = pointer.x;
            //     origY = pointer.y;

            //     rectangle = new fabric.Rect({
            //         left: origX,
            //         top: origY,
            //         fill: 'transparent',
            //         stroke: 'red',
            //         strokeWidth: 3,
            //     });
            //     this.canvas.add(rectangle);
            // });

            // this.canvas.on('mouse:move', function(o){
            //     if (!isDown) return;
            //     var pointer = this.canvas.getPointer(o.e);
            //     if(origX>pointer.x){
            //         rectangle.set({ left: Math.abs(pointer.x) });
            //     }
            //     if(origY>pointer.y){
            //         rectangle.set({ top: Math.abs(pointer.y) });
            //     }
                
            //     rectangle.set({ width: Math.abs(origX - pointer.x) });
            //     rectangle.set({ height: Math.abs(origY - pointer.y) });
            //     this.canvas.renderAll();
            // });

            // this.canvas.on('mouse:up', function(o){
            //     isDown = false;
            // });
            // this.canvas.setDimensions({width: this.canvasWidth, height: this.canvasHeight});
            // this.canvas.backgroundColor = "#fff";
            // //slet canvasProperties = {width: this.canvas.width, height: this.canvas.height}
            // //let currentCanvas = {json: this.canvas.toJSON(), canvas: canvasProperties};
            // // new CanvasHistory(this.canvas, currentCanvas);
            // this.canvas.add(new fabric.Circle({ radius: 30, fill: '#f55', top: 100, left: 100 }));

            // this.canvas.item(0).set({
            //     borderColor: 'red',
            //     cornerColor: 'green',
            //     cornerSize: 6,
            //     transparentCorners: false
            // });
            // this.canvas.setActiveObject(this.canvas.item(0));
            // //this.__canvases.push(this.canvas);
        },
        methods: {

            
        }
    }
</script>

<style scoped>

</style>
