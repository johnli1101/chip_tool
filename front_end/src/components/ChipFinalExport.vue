<template>
    <div>
        <v-btn
            depressed
            color="success"
            @click="dialog = true"
        >
            Final
        </v-btn>
        <v-dialog
            v-model="dialog"
            width="50vh"
            height="100vh"
            @click:outside="handleExportDialogOff()"
        >
            <v-card>
                <v-card-title class="headline grey lighten-2">
                    Please type in a name to export by:
                </v-card-title>
                <v-divider></v-divider>
                <v-container>
                    <v-row align="center" justify="center">
                        <v-col md="4">
                            <v-text-field
                                placeholder="Project Name"
                                v-model="project_name"
                            >
                            </v-text-field>
                        </v-col>
                    </v-row>
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
        ,project_name: ""
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
    },
    components: {
        
    },
    props: {
        
    },
    methods: {
        handleExportDialogOff() {
            this.dialog = false;
        },
        //export image inside of the file directory
        async handleExport() {

            let image_data = "";

            this.$store.dispatch('changeLoading', true);

            await this.axios.post("http://" + this.databaseLocalHost + "/createFinalExport", {filename: this.project_name},
            {
                responseType: 'arraybuffer'
            })
            .then(response => {
                image_data = Buffer.from(response.data, 'binary').toString('base64')
            })
            // .then(response=> {
            //     console.log(response);
            //     image_data = response["data"];
            // }).catch(error => {
            //     console.log(error);
            // })
            console.log(image_data)

            var a = document.createElement("a"); //Create <a>
            a.href = "data:image/png;base64," + image_data; //Image Base64 Goes here
            a.download = "Image.png"; //File name Here
            a.click(); //Downloaded file

            // const fileURL = URL.createObjectURL(image_data)

            // //var fileURL = window.URL.createObjectURL(image_data);
            // var fileLink = document.createElement('a');

            // fileLink.href = fileURL;
            // fileLink.setAttribute('download', this.project_name + ".png");
            // document.body.appendChild(fileLink);

            // fileLink.click();

            this.$store.dispatch('changeLoading', false);
            
        },
        // async handleExport() {
        //     this.$store.dispatch("changeTemplate", this.templateSelection);
            
        //     let payload = {
        //         template: this.templateSelection
        //         ,front_url: this.chipFrontUrl
        //         ,back_url: this.chipBackUrl
        //     };
        //     let filepath = "";
        //     let fileSize = [0, 0];
        //     this.$store.dispatch("changeLoading", true);
        //     await this.axios.post("http://" + this.databaseLocalHost + "/createExport", payload)
        //     .then(response=> {
        //         console.log(response);
        //         filepath = response["data"]["filepath"];
        //         fileSize = response["data"]["filesize"];
        //     }).catch(error => {
        //         console.log(error);
        //     });
        //     this.$store.dispatch("changeLoading", false);

        //     var filename = filepath.replace(/^.*[\\/]/, '');
        //     let image_path = "http://" + this.localHostName + "/chip_images/exported/" + filename;
        //     console.log(image_path)
        //     payload = {
        //         image: image_path
        //         ,image_size: fileSize
        //     };
        //     this.$emit("show-painterro", payload);
        //     this.dialog = false;
        // }
    }
}
</script>

<style scoped>



</style>