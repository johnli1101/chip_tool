<template>
    <v-app-bar
          color="deep-purple accent-4"
          dark
          flat
        >
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>Chip Project</v-toolbar-title>

            <v-spacer></v-spacer>
            <!-- <v-row>
                <v-tabs
                    background-color="deep-purple accent-4"
                    center-active
                    dark
                >
                    <v-tab>Front</v-tab>
                    <v-tab>Back</v-tab>
                </v-tabs>
            </v-row> -->
            <ChipFinalExport />
            <ChipShowEditor @show-painterro="showPainterro()" />
            <ChipExportButton @show-painterro="showPainterro($event)"/>
    </v-app-bar>
</template>

<script>
    import ChipFinalExport from './ChipFinalExport';
    import ChipExportButton from "./ChipExportButton";
    import ChipShowEditor from "./ChipShowEditor";
    import Painterro from "painterro";

    export default {
        mounted() {
            this.$nextTick( () => {
                this.painterro= Painterro({
                    saveHandler: (image, done) => {
                        let filename = "file.png";
                        const type = 'image/png';
                        const file = new File([image.asBlob(type)], filename,  {type: type});
                        this.downloadImage(file, filename)
                        done(true);
                    }
                });
            });
        },
        props: {

        },
        components: {
            ChipFinalExport
            ,ChipExportButton
            ,ChipShowEditor
        },
        computed: {
            chipInstruction() {
                return this.$store.state.chipInstruction;
            },
            currentEditImage() {
                return this.$store.state.currentEditImage;
            },
            databaseLocalHost() {
                return this.$store.state.databaseLocalHost;
            },
            localHostName() {
                return this.$store.state.localHostName;
            },
            chipImage() {
                return this.$store.state.chipImage;
            },
            chipInstructionSize() {
                return this.$store.state.chipInstructionSize;
            },
            chipImageSize() {
                return this.$store.state.chipImageSize;
            },
        },
        data: () => ({
            painterro: null,
        }),
        methods: {
            showPainterro(payload) {
                if(payload) {
                    if(payload.image && payload.image_size) {
                        console.log("Hello");
                        this.painterro= Painterro({
                            saveHandler: (image, done) => {
                                let filename = "file.png";
                                const type = 'image/png';
                                const file = new File([image.asBlob(type)], filename,  {type: type});
                                
                                this.uploadImageToFileSystem(file);
                                this.$store.dispatch('changeCurrentEditImage', "http://" + this.localHostName + "/chip_images/final/" + filename)
                                this.downloadImage(file, filename)
                                done(true);
                            },
                            defaultSize: payload.image_size[0] + "x" + payload.image_size[1],
                            backplateImgUrl: payload.image,
                        });
                        this.painterro.show();
                    } 
                }
                else {
                    // console.log(this.currentEditImage);
                    // this.painterro.clear();
                    // console.log(this.currentEditImage + "#" + new Date().getTime())
                    // this.painterro.show(this.currentEditImage + "#" + new Date().getTime());
                    this.painterro.show();
                }
                
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
            async uploadImageToFileSystem(file) {
                console.log(file);
                let newFilename = "";
                var data = new FormData()
                data.append('file', file);
                console.log(data);

                this.$store.dispatch('changeLoading', true);
                await this.axios.post("http://" + this.databaseLocalHost + "/uploadImageFinal", data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(response => {
                    console.log(response);
                    newFilename = response["data"];

                }).catch(error => {
                    console.log(error);
                });
                this.$store.dispatch('changeLoading', false);
                return newFilename;
            },
        }
    }
</script>

<style scoped>

</style>
