<template>
    <div>
    <!-- <v-container fill-height fill-width fluid>
        <v-row align="center" justify="center"> -->
            <!-- <span> -->
                <!-- <div className="container" style="width:600px" v-if="showPaintTool" >
                    <div style="margin: 20px"> -->
                    <span v-if="showPaintTool">
                        <PaintTool
                            :canvasWidth="chipFrontSize[0]"
                            :canvasHeight="chipFrontSize[1]"
                            :background_image_view1="chipFrontUrlAdj"
                            :background_image_view2="chipBackUrlAdj"
                            v-bind:overlays="chipInstructionAdjustDropdownAdj"
                            v-bind:background_image_size="chipFrontSize"
                        />
                    </span>
                    <!-- </div> -->
                <!-- </div> -->
                <!-- <ChipPaintTool side="front" /> -->
                <ChipPointsSelection />
                <!-- <ChipPaintTool2 side="back" /> -->
            <!-- </span> -->
            
        <!-- </v-row>
    </v-container> -->
    </div>
</template>

<script>
    // import ChipPaintTool from './ChipPaintTool.vue';
    import ChipPointsSelection from './ChipPointSelection.vue';
    //import PaintTool from './paint_tool/PaintTool';
    import PaintTool from './PaintTool';

    export default {
        mounted() {

        },
        components: {
            // ChipPaintTool,
            ChipPointsSelection,
            PaintTool
            //ChipPaintTool2
        },
        computed: {
            chipFrontUrlAdj() {
                return this.$store.state.chipFrontUrlAdj;
            },
            chipBackUrlAdj() {
                return this.$store.state.chipBackUrlAdj;
            },
            chipInstructionSize() {
                return this.$store.state.chipInstructionSize;
            },
            chipInstructionAdjustDropdown() {
                return this.$store.state.chipInstructionAdjustDropdown;
            },
            chipInstructionAdjustDropdownAdj() {
                return this.$store.state.chipInstructionAdjustDropdownAdj;
            },
            chipFrontSize() {
                return this.$store.state.chipFrontSize;
            },
            showPaintTool() {
                return this.$store.state.showPaintTool;
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
