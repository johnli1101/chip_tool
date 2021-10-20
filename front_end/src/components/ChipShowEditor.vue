<template>
    <div>
        <v-btn
            depressed
            color="success"
            @click="handleOpenEditor"
        >
            Show Editor
        </v-btn>
    </div>
</template>

<script>
//import Painterro from 'painterro'

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
        currentEditImage() {
            return this.$store.state.currentEditImage;
        }
    },
    components: {
        
    },
    props: {
        
    },
    methods: {
        handleOpenEditor() {
            if(this.currentEditImage !== "" && this.currentEditImage.length > 0) {
                this.$emit("show-painterro");
            }
        },
    }
}
</script>

<style scoped>



</style>