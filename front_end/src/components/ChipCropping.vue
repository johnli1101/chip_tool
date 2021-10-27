<template>
    <v-dialog
        v-model="dialogCropping"
        width="150vh"
        height="150vh"
        persistent
    >
        <v-card>
            <v-card-title primary-title class="justify-center">
                Chip Cropping
            </v-card-title>
            <cropper
                ref="cropper"
                :src="getImage()"
                :defaultSize="currentSize()"
                :defaultPosition="currentPosition()"
                @change="handleChangeCrop"
            />
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-select
                    :items="chipInstructionDropdown"
                    item-text="text"
                    item-value="value"
                    v-model="dropdownDefault"
                    label="Instruction to Select"
                    outlined
                    @change="handleChangeDropdown"
                ></v-select>
                <v-btn
                    color="primary"
                    text
                    @click="handleContinue"
                >
                    Next
                </v-btn>
                <v-row align="center" justify="center">
                    <v-alert
                        type="error"
                        v-model="alert"
                    >
                        <span v-for="(error, index) in errorMsg"
                            :key=index
                        >
                            {{error}} <br>
                        </span>
                    </v-alert>
                </v-row>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';

  export default {
    created() {
        this.$root.$refs.ChipCropping = this;
    },
    components: {
        Cropper,
    },
    data: () => ({
        chipInstructionFiles: []
        ,newImages: []
        ,currentIndex: 0
        ,instructionCropAreas: []
        ,errorMsg: []
        ,dropdownDefault: ""
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
    // mount() {
    //     this.init();
    // },
    methods: {
        init() {
            console.log(this.chipInstructionSizes);
            console.log(this.chipInstructionDropdown);
            for(let i = 0; i < this.chipInstructionSizes.length; ++i) {
                this.instructionCropAreas.push({width: this.chipInstructionSizes[i][0]
                                        ,height: this.chipInstructionSizes[i][1]
                                        ,left: 0
                                        ,top: 0
                                    });
                this.newImages.push({image: this.chipInstructionUrls[i], same: true});
            }
            this.dropdownDefault = this.chipInstructionDropdown[0].value;
            console.log(this.instructionCropAreas[this.currentIndex]);

            console.log(this.instructionCropAreas);
            console.log(this.dropdownDefault);
        },
        currentPosition() {
            if(this.instructionCropAreas.length > 0) {
                let sizes = this.instructionCropAreas[this.currentIndex]
                return {left: sizes.left, top: sizes.top};
            }
        },
        currentSize() {
            if(this.instructionCropAreas.length > 0) {
                let sizes = this.instructionCropAreas[this.currentIndex]
                console.log(sizes);
                return {width: sizes.width, height: sizes.height};
            }
        },
        getImage() {
            if(this.chipInstructionDropdown.length === 0) {
                return "";
            } else {
                console.log("hello");
                console.log(this.chipInstructionDropdown[this.currentIndex].value);
                return this.chipInstructionDropdown[this.currentIndex].value;
            }
        },
        handleChangeCrop({coordinates, canvas}) {
            console.log(coordinates);
            this.newImages[this.currentIndex].image = canvas.toDataURL();
            this.newImages[this.currentIndex].same = false;
            this.instructionCropAreas[this.currentIndex] = coordinates;
        },
        async uploadImageToFileSystem(image, same, filename) {
            // console.log(file);
            // console.log(folder);
            // let newFilename = "";
            // var data = new FormData()
            // data.append('file', file);
            // //data.append('folder', folder);
            // console.log(data);

            // await this.axios.post("http://" + this.databaseLocalHost + "/croppedImageUpload", data, {
            //     headers: {
            //         'Content-Type': 'multipart/form-data'
            //     }
            // }).then(response => {
            //     console.log(response);
            //     newFilename = response["data"];

            // }).catch(error => {
            //     console.log(error);
            // });
            let data = {image: image, same: same, filename: filename};
            let newFilename = "";
            console.log(data);
            await this.axios.post("http://" + this.databaseLocalHost + "/croppedImageUpload", data
            ).then(response => {
                console.log(response);
                newFilename = response["data"];
            }).catch(error => {
                console.log(error);
            });

            return newFilename;
        },
        addImageProcess(src){
            return new Promise((resolve, reject) => {
                let img = new Image()
                img.onload = () => resolve(img)
                img.onerror = reject
                img.src = src
            })
        },

        async handleContinue() {
            let newFilename = "";
            let textFilename = "";
            let newDropdown = [];
            let newSizeList = [];
            let newInstructionUrls = [];
            let newUrlsList = [];
            console.log(this.newImages);
            for(let i = 0; i < this.newImages.length; ++i) {
                console.log(this.newImages[i]);
                newFilename = await this.uploadImageToFileSystem(this.newImages[i].image, this.newImages[i].same, this.chipInstructionDropdown[i].text);
                console.log(newFilename);
                textFilename = newFilename.split('/').pop();
                console.log(textFilename);
                newDropdown.push({value: "http://" + this.databaseLocalHost + "/static/image_cropped/" + textFilename
                                    ,text: textFilename});
                newInstructionUrls.push(newFilename);
                newUrlsList.push(newFilename);
                if(!this.newImages[i].same) {
                    await this.addImageProcess(this.newImages[i].image).then(result => {
                        console.log(result);
                        newSizeList.push([result.width, result.height]);
                    })
                }
                else {
                    newSizeList.push(this.chipInstructionSizes[i]);
                }

            }
            console.log(newDropdown);
            console.log(newSizeList);
            this.$store.dispatch('changeChipInstructionUrls', newUrlsList);
            this.$store.dispatch('changeChipInstructionSizes', newSizeList);
            console.log(this.chipInstructionSizes);
            this.$store.dispatch('changeChipInstructionDropdown', newDropdown);
            this.$root.$refs.PointSelection.setUpPointSelection();
            this.$store.dispatch('changeDialogCropping', false);
            this.$store.dispatch('changeDialogPointSelection', true);
        },
        handleChangeDropdown(event) {
            console.log(event);
            this.dropdownDefault = event;
            for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
                if(this.chipInstructionDropdown[i].value === event) {
                    this.currentIndex = i;
                }
            }
            this.$refs.cropper.setCoordinates(this.instructionCropAreas[this.currentIndex]);
            // let instructionIndex = 0; 
            // for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
            //     if(event === this.chipInstructionDropdown[i].value) {
            //         instructionIndex = i;
            //     }
            // }
            // console.log(instructionIndex)
            // this.chip_instruction_index = instructionIndex;
            // this.chip_instruction_url = event;
            // this.currentIndex = instructionIndex;
            // console.log(this.chipInstructionSizes[instructionIndex][1], this.chipInstructionSizes[instructionIndex][0]);
            // this.instructionMapBounds = [this.chipInstructionSizes[instructionIndex][1], this.chipInstructionSizes[instructionIndex][0]];
            // this.overlayMapImage = this.chipInstructionDropdown[instructionIndex].text;
            // console.log(this.markers);
            // console.log(instructionIndex);
            // console.log(this.chipInstructionSizes);
        },
    }
  }
</script>

<style scoped>
    .main-card {
        align-items: "center";
        padding-bottom: 30px;
    }
</style>
