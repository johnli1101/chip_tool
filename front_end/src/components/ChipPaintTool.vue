<template>
    <div>
        <v-card
            max-width="180vh"
            max-height="100vh"
        >
            <v-card-title primary-title class="justify-center">
                Front Side
            </v-card-title>
            <v-toolbar>
                <v-btn icon @click="handleSwitchMode('line')">
                    <v-icon>mdi-vector-line</v-icon>
                </v-btn>
                <v-btn icon @click="handleSwitchMode('rectangle')">
                    <v-icon>mdi-rectangle-outline</v-icon>
                </v-btn>
                <v-btn icon @click="handleSwitchMode('eraser')">
                    <v-icon>mdi-eraser</v-icon>
                </v-btn>
                <v-btn icon @click="handleSwitchMode('move')">
                    <v-icon>mdi-arrow-all</v-icon>
                </v-btn>
                <v-btn icon @click="handleSwitchMode('undo')">
                    <v-icon>mdi-undo</v-icon>
                </v-btn>
                <!-- <v-btn icon @click="handleSwitchMode('clear')">
                    <v-icon>mdi-backspace-reverse-outline</v-icon>
                </v-btn> -->
                <v-btn icon @click="handleTransparency()">
                    <v-icon>mdi-play-box-outline</v-icon>
                </v-btn>
            </v-toolbar>
            <Editor 
                :canvasWidth="canvasWidth" 
                :canvasHeight="canvasHeight" 
                ref="editor" 
            />
        </v-card>
        <ChipTransparencyDialog @switch-transparency="switchTransparencyImageGlobal($event, 'front')"/>
    </div>
</template>

<script>
    import Editor from 'vue-image-markup';
    import ChipTransparencyDialog from './ChipTransparencyDialog.vue';

    export default {
        created() {
            this.$root.$refs.FrontPaintTool = this;
            //this.$root.$refs.FrontEditor = this.$refs.editor;
            console.log("Hi");
        },
        mounted() {
            // let randomVariable = "http://localhost:8080/chip_images/originals/chip_compare2.png"
            // this.$refs.editor.setBackgroundImage(randomVariable);
            //this.$refs.editor.setBackgroundImage(require("../assets/ic_chip.jpeg"));
            // let customizeRectangle = { stroke: 'blue',strokeWidth: "5" }
            //this.$refs.editor.set('line',customizeRectangle)
        },
        components: {
            Editor
            ,ChipTransparencyDialog
        },
        props: {
            sizeName: String,
            side: String,
        },
        computed: {
            chipFrontUrl() {
                return this.$store.state.chipFrontUrl;
            },
            databaseLocalHost() {
                return this.$store.state.databaseLocalHost;
            },
            localHostName() {
                return this.$store.state.localHostName;
            },
            chipInstructionUrls() {
                return this.$store.state.chipInstructionUrls;
            },
            chipInstructionSize() {
                return this.$store.state.chipInstructionSize;
            },
            chipImageSize() {
                return this.$store.state.chipImageSize;
            },
        },
        data: () => ({
            canvasWidth: 1500
            ,canvasHeight: 1300
            ,frontBackground: ""
            ,chip_test_image: ""
            // ,bars: [
            //     { class: '' },
            //     { class: '', dark: true },
            //     { class: 'primary', dark: true },
            //     { class: 'elevation-0' },
            // ],
        }),
        methods: {
            handleSwitchMode(mode) {
                //let customizeRectangle = { stroke: 'blue',strokeWidth: "5" };
                switch(mode) {
                    case "line":
                        //let customizeLine = { stroke: 'blue', strokeWidth: "5" };
                        this.$refs.editor.set('line');
                        break;
                    case "rectangle":
                        //let customizeRectangle = { stroke: 'blue',strokeWidth: "5" };
                        this.$refs.editor.set('rect');
                        break;
                    case "eraser":
                        this.$refs.editor.set('eraser')
                        break;
                    case "move":
                        this.$refs.editor.set('selectMode');
                        break;
                    case "undo":
                        this.$refs.editor.undo();
                        break;
                    // case "clear":
                    //     this.$refs.editor.clear();
                    //     break;
                }
            },
            handleTransparency() {
                console.log("Hello");
                this.$store.dispatch('changeDialogTransparency', true);
            },
            // getImgUrl(url) {
            //     var images = require.context('../../public/chip_images/transparencies/', false, /\.png$/)
            //     return images('./' + url)
            // },
            async switchTransparencyImageGlobal(transparencyFile, side) {
                this.$store.dispatch('changeLoading', true);
                console.log(transparencyFile);
                let localFilename = transparencyFile.replace(/^.*[\\/]/, '');
                console.log('../../public/chip_images/transparencies/' + localFilename);
                console.log(localFilename);
                //this.chip_test_image = require('../../public/chip_images/transparencies/' + localFilename);

                if(side === "front") {
                    console.log("Hello");
                    this.$refs.editor.setBackgroundImage("http://" + this.localHostName + "/chip_images/transparencies/" + localFilename);
                }
                else if (side === "back") {
                    this.$refs.editor.setBackgroundImage(require('../assets/transparent/' + localFilename));
                }
                this.$store.dispatch('changeLoading', false);
            },
            switchBackgroundImagesGlobal(frontUrl, frontSize) {
                console.log("hello");
                console.log(frontUrl);
                var filename_front = frontUrl.replace(/^.*[\\/]/, '');
                let chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename_front;
                console.log(chip_image_path);
                console.log(this.chipFrontUrl);
                this.frontBackground = chip_image_path;
                console.log(this.chipInstructionUrls);
                console.log(frontSize);
                this.canvasWidth = frontSize[0];
                this.canvasHeight = frontSize[1];
                console.log(this.canvasWidth + " " + this.canvasHeight);
                console.log(chip_image_path);
                this.$refs.editor.setBackgroundImage(chip_image_path);
                //this.$refs.editor.setBackgroundImage(chip_image_path);
            },
        }
    }
</script>

<style scoped>

</style>
