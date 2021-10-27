<template>
    <div>
        <v-btn
            depressed
            color="success"
            @click="dialog = true"
        >
            Export Chips
        </v-btn>
        <v-dialog
            v-model="dialog"
            width="50vh"
            height="120vh"
            @click:outside="handleExportDialogOff()"
        >
            <v-card>
                <v-card-title class="headline grey lighten-2">
                    Chooser a template to export as:
                </v-card-title>
                <v-divider></v-divider>
                <v-container>
                    <v-radio-group v-model="templateSelection" mandatory>
                        <v-row>
                            <!-- <v-col> -->
                            <v-radio
                                value="A"
                            >
                                <template v-slot:label>
                                    <v-img             
                                        :src="require('../assets/chip_template_a.png')"
                                        lazy-src=""
                                        max-width="15vh"
                                        max-height="10vh"
                                    >
                                    </v-img>
                                </template>
                            </v-radio>
                            <!-- <v-radio
                                value="C"
                            >
                                <template v-slot:label>
                                    <v-img             
                                        :src="require('../assets/chip_template_c.png')"
                                        lazy-src=""
                                        max-width="10vh"
                                        max-height="20vh"
                                    >
                                    </v-img>
                                </template>
                            </v-radio> -->
                            <!-- </v-col> -->
                            <!-- <v-col>
                            <v-radio
                                value="B"
                            >
                                <template v-slot:label>
                                    <v-img             
                                        :src="require('../assets/chip_template_b.png')"
                                        lazy-src=""
                                        max-width="15vh"
                                        max-height="10vh"
                                    >
                                    </v-img>
                                </template>
                            </v-radio>
                            <v-radio
                                value="D"
                            >
                                <template v-slot:label>
                                    <v-img             
                                        :src="require('../assets/chip_template_d.png')"
                                        lazy-src=""
                                        max-width="10vh"
                                        max-height="20vh"
                                    >
                                    </v-img>
                                </template>
                            </v-radio>
                            </v-col> -->
                        </v-row>
                    </v-radio-group>
                </v-container>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        text
                        @click="handleExport()"
                    >
                        Export
                    </v-btn>
                    <v-btn
                        color="primary"
                        text
                        @click="handleExportDialogOff()"
                    >
                        Cancel
                    </v-btn>
                </v-card-actions>
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
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
//import Painterro from 'painterro';

export default {
    mounted() {
    //    this.$nextTick( () => {
    //      this.painterro= Painterro({
    //        id: 'painterro',
    //        colorScheme: {
    //          main: '#f8f8f8',
    //          control: '#d5d5d5',
    //          controlContent: '#434649'
    //        },
    //        saveHandler: (image, done) => {
    //          const type = 'image/png';
    //          const file = new File([image.asBlob(type)], "file.png",  {
    //            type: type,
    //          });
    //          this.add_file(file); // do something with file e.g. upload to server
    //          done(true); //done and hide painterro
    //        }
    //      });
    //    });
    },
    data: () => ({
        dialog: false
        ,templateSelection: ""
        ,painterro: null
        ,alert: false
        ,errorMsg: []
    }),
    computed: {
        databaseLocalHost() {
            return this.$store.state.databaseLocalHost;
        },
        localHostName() {
            return this.$store.state.localHostName;
        },
        chipFrontUrl() {
            return this.$store.state.chipFrontUrl;
        },
        chipBackUrl() {
            return this.$store.state.chipBackUrl;
        },
        template() {
            return this.$store.state.template;
        },
        chipFrontNewImageData() {
            return this.$store.state.chipFrontNewImageData;
        },
        chipBackNewImageData() {
            return this.$store.state.chipBackNewImageData;
        }
    },
    components: {
        
    },
    props: {
        
    },
    methods: {
        getImage() {
            var filename_front = this.chipFrontUrl.replace(/^.*[\\/]/, '');
            let chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename_front;
            return chip_image_path;
        },
        handleExportDialogOff() {
            this.dialog = false;
        },
        async downloadImage(image_info, filename) {
            //await this.downloadImage(this.activeMarker.picture);
            console.log(image_info);
            console.log(filename);

            // console.log(response);
            // var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileURL = window.URL.createObjectURL(image_info);
            var fileLink = document.createElement('a');

            fileLink.href = fileURL;
            fileLink.setAttribute('download', filename);
            document.body.appendChild(fileLink);

            fileLink.click();
            this.$store.dispatch('changeLoading', false);
            
        },

        async uploadImageToFileSystem(image, filename) {
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
            let data = {image: image, filename: filename};
            let newFilename = "";
            console.log(data);
            await this.axios.post("http://" + this.databaseLocalHost + "/paintImageUpload", data
            ).then(response => {
                console.log(response);
                newFilename = response["data"];
            }).catch(error => {
                console.log(error);
            });

            return newFilename;
        },

        // lengthCheck() {
        //     if(this.templateSelection === "") {
        //         this.alert = true;
        //         this.errorMsg.push("Please select a template.");
        //         return false;
        //     }
        //     return true;
        // },
        // checkError() {
        //     this.alert = false;
        //     this.errorMsg = [];
        //     if(!this.lengthCheck()) {
        //         console.log("Hello");
        //         this.alert = true;
        //         return true;
        //     }
        //     return false;
        // },

        async handleExport() {
            // if(this.checkError()) {
            //     return;
            // }
            this.$store.dispatch("changeTemplate", this.templateSelection);
            // console.log("Hello");
            // console.log(this.$root.$refs.PaintTool.rasterize());
            // console.log("Hello");
            // let imageSrcs = this.$root.$refs.PaintTool.rasterize();

            // console.log(imageSrcs);
            this.$store.dispatch("changeLoading", true);

            let chipFront = this.chipFrontUrl;
            let chipBack = this.chipBackUrl;
            console.log(this.chipFrontNewImageData);
            console.log(this.chipBackNewImageData);
            if(this.chipFrontNewImageData !== "") {
                console.log("Front");
                chipFront = await this.uploadImageToFileSystem(this.chipFrontNewImageData, "chip_front.png");
                console.log(chipFront);
                this.$store.dispatch('changeChipFrontPaintImageUrl', chipFront);
            
            }
            if(this.chipBackNewImageData !== "") {
                console.log("Back");
                chipBack = await this.uploadImageToFileSystem(this.chipBackNewImageData, "chip_back.png");
                console.log(chipBack);
                this.$store.dispatch('changeChipBackPaintImageUrl', chipBack);
                
            }

            let payload = {
                template: this.templateSelection
                ,front_url: chipFront
                ,back_url: chipBack
            };
            let filepath = "";
            let fileSize = [0, 0];

            await this.axios.post("http://" + this.databaseLocalHost + "/createExport", payload)
            .then(response=> {
                console.log(response);
                filepath = response["data"]["filepath"];
                fileSize = response["data"]["filesize"];
            }).catch(error => {
                console.log(error);
            });
            this.$store.dispatch("changeLoading", false);

            var filename = filepath.replace(/^.*[\\/]/, '');
            //let image_path = "http://" + this.localHostName + "/chip_images/exported/" + filename;
            let image_path = "http://" + this.databaseLocalHost + "/static/export/" + filename;
            console.log(image_path)

            payload = {
                image: image_path
                ,image_size: fileSize
            };
            this.$store.dispatch('changeShowFinalEdit', true);
            this.$emit("show-painterro", payload);
            this.dialog = false;

            // let payload = {
            //     template: this.templateSelection
            //     ,front_url: this.chipFrontUrl
            //     ,back_url: this.chipBackUrl
            // };
            // let filepath = "";
            // let fileSize = [0, 0];
            // this.$store.dispatch("changeLoading", true);
            // await this.axios.post("http://" + this.databaseLocalHost + "/createExport", payload)
            // .then(response=> {
            //     console.log(response);
            //     filepath = response["data"]["filepath"];
            //     fileSize = response["data"]["filesize"];
            // }).catch(error => {
            //     console.log(error);
            // });
            // this.$store.dispatch("changeLoading", false);

            // var filename = filepath.replace(/^.*[\\/]/, '');
            // let image_path = "http://" + this.localHostName + "/chip_images/exported/" + filename;
            // console.log(image_path)
            // // Painterro({
            // //     saveHandler: (image, done) => {
                    
            // //         let filename = "file.png";
            // //         const type = 'image/png';
            // //         const file = new File([image.asBlob(type)], filename,  {type: type,});
            // //         this.downloadImage(file, filename)
            // //         done(true);
            // //     }
            // // }).show(image_path);
            // payload = {
            //     image: image_path
            //     ,image_size: fileSize
            // };
            // this.$emit("show-painterro", payload);
            // this.dialog = false;
            // //let command = {command: "gimp " + this.chipFrontUrl}
            // // let command = {command: "/Applications/krita.app/Contents/MacOS/krita"}
            // // console.log(command);
            // // await this.axios.post("http://" + this.databaseLocalHost + "/launchGimp", command)
            // // .then(response => {
            // //     console.log(response);

            // // }).catch(error => {
            // //     console.log(error);
            // // });
        }
    }
}
</script>

<style scoped>



</style>