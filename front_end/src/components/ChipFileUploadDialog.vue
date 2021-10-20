<template>
    <v-dialog
        v-model="dialogFileUpload"
        width="150vh"
        height="150vh"
        persistent
    >
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <v-col cols="12" align="center" justify="center">
                    <v-card
                        max-width="90vh"
                        class="main-card"
                    >
                        <v-card-title primary-title class="justify-center">
                            Chip File Upload
                        </v-card-title>
                        <v-container>
                            <ChipFileUpload 
                                fileInputPlaceholder="Chip Front" 
                                fileUploadType="single" 
                                @update-file-variable="updateFileVariable($event, 'front')"
                            />
                            <ChipFileUpload 
                                fileInputPlaceholder="Chip Back" 
                                fileUploadType="single" 
                                @update-file-variable="updateFileVariable($event, 'back')"
                            />
                            <ChipFileUpload 
                                fileInputPlaceholder="Chip Instructions" 
                                fileUploadType="multiple" 
                                @update-file-variable="updateFileVariable($event, 'instructions')"
                            />
                            <!-- <v-row align="center" justify="center">
                                <v-col md="4">
                                    <v-text-field
                                        placeholder="Project Name"
                                        v-model="project_name"
                                    >
                                    </v-text-field>
                                </v-col>
                            </v-row> -->
                            <v-row align="center" justify="center">
                                <!-- <span v-if="errorMsg.length > 0"> -->
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
                                <!-- </span> -->
                            </v-row>
                            <v-row align="center" justify="center">
                                <v-btn
                                    class="primary spacing"
                                    @click="handleProceed"
                                >
                                    Proceed
                                </v-btn>
                            </v-row>
                        </v-container>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-dialog>
</template>

<script>
  import ChipFileUpload from './ChipFileUpload';

  export default {
    components: {
        ChipFileUpload
    },
    data: () => ({
        chipFrontFile: []
        ,chipBackFile: []
        ,chipInstructionFiles: []
        ,project_name: "chip_project"
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
        dialogFileUpload() {
            return this.$store.state.dialogFileUpload;
        }
    },
    methods: {
        updateFileVariable(file, type) {
            switch (type) {
                case "instructions":
                    this.chipInstructionFiles = file;
                    break;

                case "front":
                    this.chipFrontFile = file;
                    break;
                
                case "back":
                    this.chipBackFile = file;
                    break;

                default:
                    break;
            }
        },
        //error checking for empty fields
        checkEmptyFields() {
            if(this.chipFrontFile.length === 0) {
                this.errorMsg.push("Chip front file is empty.");
            }
            if(this.chipBackFile.length === 0) {
                this.errorMsg.push("Chip back file is empty.");
            }
            if(this.chipInstructionFiles.length === 0) {
                this.errorMsg.push("Chip instructions is empty.");
            }
            if(this.project_name.length === 0) {
                this.errorMsg.push("File name is empty");
            }
            if(this.errorMsg.length > 0) {
                return true;
            }
            else {
                return false;
            }
        },
        //main error checking function for this component
        checkError() {
            this.$store.dispatch("changeErrorMsg", []);
            this.errorMsg = []
            this.alert = false;
            // this.$store.dispatch('changeShowError', false);
            if(this.checkEmptyFields()) {
                this.$store.dispatch("changeErrorMsg", this.errorMsg);
                // this.$store.dispatch('changeShowError', true);
                this.alert = true;
                console.log(this.errorMsg);
                return true;
            }
            return false;
        },
        async handleProceed() {
            let fileInfo = {};
            let newFilePath = "";
            let chipInstructionPaths = [];
            let chipInstructionSizes = [];
            let instructionDropdown = [];
            let tempPath = "";
            let tempFile = "";
            let frontUrl = "";
            let backUrl = "";
            let frontSize = [];
            let backSize = [];

            //if there are errors then don't proceed
            if(this.checkError()) {
                console.log("I'm in here");
            }
            else {

                this.$store.dispatch('changeLoading', true);

                // handle the loading for the chip instructions
                for(let i = 0; i < this.chipInstructionFiles.length; ++i) {
                    fileInfo = await this.getImageData(this.chipInstructionFiles[i]);
                    newFilePath = await this.uploadImageToFileSystem(this.chipInstructionFiles[i], "instructions");
                    chipInstructionPaths.push(newFilePath);
                    chipInstructionSizes.push(fileInfo.fileSize);
                }

                this.$store.dispatch('changeChipInstructionUrls', chipInstructionPaths);
                this.$store.dispatch('changeChipInstructionSizes', chipInstructionSizes);

                //create a dropdown list for the transparency selection
                
                for(let i = 0; i < chipInstructionPaths.length; ++i) {
                    tempFile = chipInstructionPaths[i].split('/').pop();
                    tempPath = "http://" + this.localHostName + "/chip_images/instructions/" + tempFile;
                    instructionDropdown.push({
                        text: tempFile
                        ,value: tempPath
                    });
                }

                this.$store.dispatch('changeChipInstructionDropdown', instructionDropdown);

                // handle the loading for the chip front and back
                fileInfo = await this.getImageData(this.chipFrontFile);
                console.log("Pushing into originals")
                frontUrl = await this.uploadImageToFileSystem(this.chipFrontFile, "originals");
                frontSize = fileInfo.fileSize;
                console.log(frontUrl);
                this.$store.dispatch('changeChipFrontUrl', frontUrl);
                this.$store.dispatch('changeChipFrontSize', fileInfo.fileSize);
                
                let filename = frontUrl.split('/').pop()
                let chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename;
                this.$store.dispatch('changeChipFrontUrlAdj', chip_image_path);

                fileInfo = await this.getImageData(this.chipBackFile);
                backUrl = await this.uploadImageToFileSystem(this.chipBackFile, "originals");
                backSize = fileInfo.fileSize;
                this.$store.dispatch('changeChipBackUrl', backUrl);
                this.$store.dispatch('changeChipBackSize', fileInfo.fileSize);
                this.$store.dispatch('changeLoading', false);

                filename = backUrl.split('/').pop()
                chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename;
                this.$store.dispatch('changeChipBackUrlAdj', chip_image_path);

                console.log(chip_image_path)
                console.log(this.chipFrontFile);
                console.log(this.chipBackFile);
                console.log(frontUrl);

                console.log(backSize);

                // this.$root.$refs.PointSelection.setUpPointSelection();
                this.$root.$refs.ChipCropping.init();
                this.$store.dispatch('changeMapBounds', frontSize);
                this.$store.dispatch('changeDialogFileUpload', false);
                this.$store.dispatch('changeDialogCropping', true);
                // this.$store.dispatch('changeDialogPointSelection', true);
            }
        },
        async uploadImageToFileSystem(file, folder) {
            console.log(file);
            console.log(folder);
            let newFilename = "";
            var data = new FormData()
            data.append('file', file);
            //data.append('folder', folder);
            console.log(data);
            if(folder === "instructions") {
                await this.axios.post("http://" + this.databaseLocalHost + "/uploadImageInstructions", data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(response => {
                    console.log(response);
                    newFilename = response["data"];

                }).catch(error => {
                    console.log(error);
                });
            }
            else if (folder === "originals") {
                await this.axios.post("http://" + this.databaseLocalHost + "/uploadImageOriginals", data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(response => {
                    console.log(response);
                    newFilename = response["data"];

                }).catch(error => {
                    console.log(error);
                });
            }


            return newFilename;
        },
        async getImageData(file) {
            let fileUrl = URL.createObjectURL(file);

            const img = new Image();
            img.src = fileUrl;
            await img.decode();

            console.log(img.width + " " + img.height);
            let fileSize = [img.width, img.height];
            
            let payload = {
                fileUrl: fileUrl
                ,fileSize: fileSize
            }

            return payload;
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
