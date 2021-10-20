<template>
    <v-dialog
        v-model="dialogTransparency"
        width="120vh"
        height="100vh"
        @keydown.esc="handleCloseTransparency()"
        @click:outside="handleCloseTransparency()"
    >
        <v-card
            class="main-card"
        >
            <v-card-title primary-title class="justify-center">
                Transparency Control
            </v-card-title>
            <v-container>
                <v-row>
                    <span :style="{ opacity: `${real_opacity}` }">
                    <v-img                        
                        :src="chip_instruction_url"
                        lazy-src=""
                        max-width="1200"
                        max-height="630"
                    >
                        <template v-slot:placeholder>
                            <v-row
                                class="fill-height ma-0"
                                align="center"
                                justify="center"
                            >
                            <v-progress-circular
                                :size="70"
                                :width="7"
                                color="purple"
                                indeterminate
                            >
                            </v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                    </span>
                </v-row>
                <v-row>
                    <v-col
                        cols="12"
                        sm="4"
                    >
                        <v-select
                            :items="chipInstructionAdjustDropdown"

                            label="Instruction to Select"
                            outlined
                            @change="handleChangeDropdown"
                        ></v-select>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="8"
                    >
                        <v-slider
                            v-model="opacity_control"
                            class="align-center"
                            :max="max"
                            :min="min"
                            hide-details
                            @change="handleTransparencyChange"
                        >
                            <template v-slot:append>
                            <v-text-field
                                v-model="opacity_control"
                                class="mt-0 pt-0"
                                hide-details
                                single-line
                                type="number"
                                style="width: 60px"
                            ></v-text-field>
                            </template>
                        </v-slider>
                    </v-col>
                </v-row>
            </v-container>
            <!-- </span> -->
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="green darken-1"
                    text
                    @click="handleSubmitTransparency()"
                >
                    Ok
                </v-btn>
                <v-btn
                    color="red darken-1"
                    text
                    @click="handleCloseTransparency()"
                >
                    Cancel
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>


  export default {
    components: {

    },
    data: () => ({
        chip_instruction_url: ""
        ,chip_instruction_index: 0
        ,opacity_control: 100
        ,real_opacity: 1
        ,max: 100
        ,min: 0
    }),
    props: {
        
    },
    computed: {
        databaseLocalHost() {
            return this.$store.state.databaseLocalHost;
        },
        localHostName() {
            return this.$store.state.localHostName;
        },
        dialogTransparency() {
            return this.$store.state.dialogTransparency;
        },
        chipInstructionUrls() {
            return this.$store.state.chipInstructionUrls;
        },
        chipFrontUrl() {
            return this.$store.state.chipFrontUrl;
        },
        chipInstructionAdjustDropdown() {
            return this.$store.state.chipInstructionAdjustDropdown;
        },
        chipInstructionAdjustUrls() {
            return this.$store.state.chipInstructionAdjustUrls;
        }
    },
    methods: {
        handleCloseTransparency() {
            this.$store.dispatch("changeDialogTransparency", false);
        },
        async handleSubmitTransparency() {
            this.$store.dispatch('changeLoading', true);
            let newFilePath = "";
            let payload = {
                original_url: this.chipFrontUrl
                ,instruction_url: this.chipInstructionAdjustUrls[this.chip_instruction_index]
                ,opacity: this.opacity_control
            }
            console.log(payload);
            await this.axios.post("http://" + this.databaseLocalHost + "/overlay", payload)
                .then(response => {
                    console.log(response);
                    newFilePath = response["data"];
                    console.log("OVER");
                }).catch(error => {
                    console.log(error);
                });

            this.$store.dispatch('changeFrontTransparencyFile', newFilePath);   
            // let localFilename = newFilePath.replace(/^.*[\\/]/, '');
            // console.log(newFilePath);
            // console.log("It's this")
            // let localFilePath = require('../../public/chip_images/transparencies/' + localFilename);
            console.log("Hello");
            this.$emit("switch-transparency", newFilePath);
            this.$store.dispatch('changeDialogTransparency', false);
            this.$store.dispatch('changeLoading', false);
        },
        handleTransparencyChange(event) {
            let new_opacity = (event/100).toFixed(2);
            console.log(new_opacity);
            this.real_opacity = new_opacity;
        },
        handleChangeDropdown(event) {
            console.log(event);
            let instructionIndex = 0; 
            for(let i = 0; i < this.chipInstructionAdjustDropdown.length; ++i) {
                if(event === this.chipInstructionAdjustDropdown[i].value) {
                    instructionIndex = i;
                }
            }
            console.log(instructionIndex)
            this.chip_instruction_index = instructionIndex;
            this.chip_instruction_url = event;
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
