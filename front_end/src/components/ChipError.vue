<template id="alert">
    <div>
        <v-alert
            :value="alert"
            type="error"
        >
            <span v-for="(error, index) in errorMsg"
                :key=index
            >
                {{error}} <br>
            </span>
        </v-alert>
    </div>
</template>

<script>

export default {
    template: '#alert',
    mounted() {
        // if(this.showError) {
        //     console.log("hi")
        //     this.alert = true;
        //     this.hideAlert();
        // }
    },
    data: () => ({
        alert: false
    }),
    computed: {
        databaseLocalHost() {
            return this.$store.state.databaseLocalHost;
        },
        localHostName() {
            return this.$store.state.localHostName;
        },
        errorMsg() {
            return this.$store.state.errorMsg;
        },
        showError() {
            return this.$store.state.showError;
        },
    },
    watch: {
        // showError(val) {
        //     console.log("Hello");
        //     if(val) {
        //         this.alert = true;
        //         console.log("Hello")
        //     } 
        // }
    },
    methods: {
        hideAlert() {
            console.log("Hello");
            window.setInterval(() => {
                this.alert = false;
                this.$store.dispatch('changeShowError', false);
                console.log("hide alert after 3 seconds");
            }, 3000)   

        },
        // alertExists() {
        //     return this.errorMsg.length > 0 ? true : false; 
        // },
    }
}
</script>

<style scoped>
    .v-alert {
        position: fixed;
        left: 50%;
        bottom: 50px;
        transform: translate(-50%, -50%);
        margin: 0 auto; 
        z-index: 9000 !important;
    }
</style>
