<template>
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
    }),
    computed: {
        databaseLocalHost() {
            return this.$store.state.databaseLocalHost;
        },
        localHostName() {
            return this.$store.state.localHostName;
        },
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
        async handleProceed() {
            let fileInfo = {};
            let newFilePath = "";
            let instructionDropdown = [];
            let tempPath = "";
            let tempFile = "";
            let chipInstructionPaths = [];
            let chipInstructionSizes = [];
            let frontUrl = "";
            let backUrl = "";
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
            this.$store.dispatch('changeChipFrontUrl', frontUrl);
            this.$store.dispatch('changeChipFrontSize', fileInfo.fileSize);
            

            fileInfo = await this.getImageData(this.chipBackFile);
            backUrl = await this.uploadImageToFileSystem(this.chipBackFile, "originals");
            this.$store.dispatch('changeChipBackUrl', backUrl);
            this.$store.dispatch('changeChipBackSize', fileInfo.fileSize);

            this.$store.dispatch('changeLoading', false);
            let filename = newFilePath.split('/').pop()
            let chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename;
            console.log(chip_image_path)
            console.log(this.chipFrontFile);
            console.log(this.chipBackFile);
            //this.$root.$refs.FrontEditor.setBackgroundImage(frontUrl);
            //this.$router.push('chip_canvas');
            //this.$store.dispatch('changeGlobalMode', "paintTool");
            this.$root.$refs.PaintTool.switchBackgroundImagesGlobal(frontUrl, backUrl);
            this.$store.dispatch('changeDialogFileUpload', false);
            
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
        // handleProceed() {
        //     console.log(this.newChipInstruction.length);
        //     console.log(this.newChipImage.length);
        //     if(this.newChipInstruction.length !== {} && this.newChipImage.length !== {}) {
        //         console.log("HELLO");
        //         this.$store.dispatch('changeChipImage', this.newChipImageURL);
        //         this.$store.dispatch('changeChipInstruction', this.newChipInstructionURL);
        //         this.$store.dispatch('changeChipImageSize', this.newChipImageSize);
        //         this.$store.dispatch('changeChipInstructionSize', this.newChipInstructionSize);
        //         console.log(this.newChipImageURL);
        //         //this.$refs.editor.setBackgroundImage(this.newChipImageURL);
                
        //         console.log(this.newChipImage);


        //     }
        // },
    }
  }
</script>

<style scoped>
    .main-card {
        align-items: "center";
        padding-bottom: 30px;
    }
</style>
