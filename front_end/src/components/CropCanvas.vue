<template>
    <div class="hello">
        <canvas id="canvas"></canvas>
    </div>
</template>

<script>

    import { fabric } from 'fabric';

    export default {
        mounted(){
            this.init();
        },
        components: {
            ChipFileUpload
        },
        data: () => ({
            chipInstructionFiles: []
            ,errorMsg: []
            ,alert: false
        }),
        computed: {
            databaseLocalHost() {
                return this.$store.state.databaseLocalHost;
            },
            localHostName() {
                return this.$store.state.localHostName;
            },
            dialogPointSelection() {
                return this.$store.state.dialogPointSelection;
            },
            chipFrontUrl() {
                return this.$store.state.chipFrontUrl;
            },
            chipFrontSize() {
                return this.$store.state.chipFrontSize;
            },
            mapBounds() {
                return this.$store.state.mapBounds;
            },
            chipInstructionDropdown() {
                return this.$store.state.chipInstructionDropdown;
            },
            chipInstructionSizes() {
                return this.$store.state.chipInstructionSizes;
            },
            chipInstructionUrls() {
                return this.$store.state.chipInstructionUrls;
            },
            dialogCropping() {
                return this.$store.state.dialogCropping;
            }
        },
        methods: {
            init(){
            const canvas = new fabric.Canvas('canvas');
            canvas.selection = true;

            // 画像読込み
            const img_path = 'https://vuejs.org/images/logo.png';
            fabric.Image.fromURL(img_path,(img) => {
                    canvas.setDimensions({
                    width: img.width,
                    height: img.height
                });
                canvas.setBackgroundImage(img,() => {
                    canvas.requestRenderAll();
                });
            })
                console.log(canvas);
            }
        }
    }
</script>

<style scoped>
    .main-card {
        align-items: "center";
        padding-bottom: 30px;
    }
</style>
