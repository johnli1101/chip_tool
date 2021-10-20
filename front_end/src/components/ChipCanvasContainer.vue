<template>
    <div>
        <ChipOverlay />
        <ChipAppBar />
        <ChipTabAreaContainer />
        <ChipFileUploadDialog />
        <ChipCropping />
        <ChipError />
    </div>
</template>

<script>
    import ChipAppBar from './ChipAppBar';
    import ChipFileUploadDialog from './ChipFileUploadDialog';
    import ChipTabAreaContainer from './ChipTabAreaContainer.vue';
    import ChipOverlay from './ChipOverlay';
    import ChipError from './ChipError';
    import ChipCropping from './ChipCropping';

    export default {
        mounted() {
            console.log(this.chipFrontUrl);
            if(!this.chipFrontUrl) {
                this.$store.dispatch('changeDialogFileUpload', true);
            }
        },
        components: {
            ChipAppBar
            ,ChipFileUploadDialog
            ,ChipTabAreaContainer
            ,ChipOverlay
            ,ChipError
            ,ChipCropping
        },
        computed: {
            chipFrontUrl() {
                return this.$store.state.chipFrontUrl;
            },
            chipBackUrl() {
                return this.$store.state.chipBackUrl;
            },
            chipInstructionSize() {
                return this.$store.state.chipInstructionSize;
            },
            chipImageSize() {
                return this.$store.state.chipImageSize;
            },
        },
        data: () => ({

        }),
        methods: {

        }
    }
</script>

<style scoped>

</style>
