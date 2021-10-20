<template>
    <div>
        <v-dialog
            v-model="dialogPointSelection"
            width="150vh"
            height="100vh"
            persistent
        >
            <v-card>
                <v-card-title class="headline grey lighten-2">
                    Choose points for each template
                </v-card-title>
                <v-divider></v-divider>
                <v-row>
                    <v-col
                        cols="12"
                        sm="6"
                    >
                        <div id="mapid">
                            <l-map
                                :min-zoom="minZoom"
                                @click="addMarker"
                                :crs="crs"
                                :center="[0,0]"
                                style="z-index: 0;"
                            >
                            <l-image-overlay
                                :url="getMapImage()"
                                :bounds="[[0, 0], mapBounds]"
                            />
                            <l-marker
                                v-for="marker in markers[currentIndex]"
                                :key="marker.label"
                                :lat-lng="marker"
                                :draggable="true"
                                @dragstart="dragStartHandler"
                                @dragend="dragEndHandler"
                            >
                                <l-tooltip 
                                    :options="tooltipOptions"
                                >
                                    {{marker.label}}
                                </l-tooltip>
                            </l-marker>
                            </l-map>
                        </div>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="6"
                    >
                        <div id="mapid">
                            <l-map
                                :min-zoom="minZoom"
                                @click="addInstructionMarker"
                                :crs="crs"
                                :center="[0,0]"
                                style="z-index: 0;"
                            >
                            <l-image-overlay
                                :url="getOverlayMapImage()"
                                :bounds="[[0, 0], instructionMapBounds]"
                            />
                            <l-marker
                                v-for="marker in instructionMarkers[currentIndex]"
                                :key="marker.label"
                                :lat-lng="marker"
                                :draggable="true"
                                @dragstart="dragInstructionStartHandler"
                                @dragend="dragInstructionEndHandler"
                            >
                                <l-tooltip 
                                    :options="tooltipOptions"
                                >
                                    {{marker.label}}
                                </l-tooltip>
                            </l-marker>
                            </l-map>
                        </div>
                    </v-col>
                </v-row>
                <!-- <ChipPointSelectionTextArea  
                    :b1x="markers[currentIndex][0].lng"
                    :b1y="markers[currentIndex][0].lat"
                    :b2x="markers[currentIndex][1].lng"
                    :b2y="markers[currentIndex][1].lat"
                    :b3x="markers[currentIndex][2].lng"
                    :b3y="markers[currentIndex][2].lat"
                    :b4x="markers[currentIndex][3].lng"
                    :b4y="markers[currentIndex][3].lat"
                    :s1x="instructionMarkers[currentIndex][0].lng"
                    :s1y="instructionMarkers[currentIndex][0].lat"
                    :s2x="instructionMarkers[currentIndex][1].lng"
                    :s2y="instructionMarkers[currentIndex][1].lat"
                    :s3x="instructionMarkers[currentIndex][2].lng"
                    :s3y="instructionMarkers[currentIndex][2].lat"
                    :s4x="instructionMarkers[currentIndex][3].lng"
                    :s4y="instructionMarkers[currentIndex][3].lat"
                /> -->
                
                <v-row v-for="(marker, index) in markers[currentIndex]"
                    :key="index"
                >
                    <v-col
                        cols="12"
                        sm="3"
                    >
                        <span v-if="marker" >
                            {{marker.lng.toFixed(3)}} {{marker.lat.toFixed(3)}}
                        </span>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="3"
                    >
                        <span v-if="instructionMarkers[currentIndex][index]">
                            {{instructionMarkers[currentIndex][index].lng.toFixed(3)}} {{instructionMarkers[currentIndex][index].lat.toFixed(3)}}
                        </span>
                    </v-col>
                </v-row>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-select
                        :items="chipInstructionDropdown"

                        label="Instruction to Select"
                        outlined
                        @change="handleChangeDropdown"
                    ></v-select>
                    <v-btn
                        color="primary"
                        text
                        @click="handleContinue"
                    >
                        Ok
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { Icon } from 'leaflet';

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
iconUrl: require('leaflet/dist/images/marker-icon.png'),
shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});
// import FileSaver from 'file-saver';
import L from 'leaflet';
import { LMap, LImageOverlay, LMarker, LTooltip } from "vue2-leaflet";
//import ChipPointSelectionTextArea from "./ChipPointSelectionTextArea";
export default {
    created() {
        this.$root.$refs.PointSelection = this;
    },
    mount() {
    
    },
    data: () => ({
        markers: [],
        instructionMarkers: [],
        minZoom: -1,
        crs: L.Util.extend(L.CRS.Simple, {
                transformation: new L.Transformation(1,0,1,0)
            }),
        tooltipOptions: {
            permanent: true
        },
        prevMarkerCoord: [],
        testImage: "",
        labels: 1,
        chip_instruction_url: "",
        chip_instruction_index: 0,
        currentPoint: [],
        overlayMapImage: "",
        instructionMapBounds: [0, 0],
        currentIndex: 0,
        original_distances: [],
        instruction_distances: []
    }),
    watch: {
        currentIndex: function () {
            console.log("I've changed.");
            // var filename_front = this.chipInstructionDropdown[this.currentIndex].value.replace(/^.*[\\/]/, '');
            // let chip_image_path = "http://" + this.localHostName + "/chip_images/instructions/" + filename_front;
            // console.log(chip_image_path);
            this.overlayMapImage = this.chipInstructionDropdown[this.currentIndex].value;
            console.log(this.overlayMapImage);
        }
    },
    computed: {
        databaseLocalHost() {
            return this.$store.state.databaseLocalHost;
        },
        localHostName() {
            return this.$store.state.localHostName;
        },
        dialogPointSelection() {
            return this.$store.state.dialogPointSelection;
        },
        chipFrontUrl() {
            return this.$store.state.chipFrontUrl;
        },
        chipFrontSize() {
            return this.$store.state.chipFrontSize;
        },
        mapBounds() {
            return this.$store.state.mapBounds;
        },
        chipInstructionDropdown() {
            return this.$store.state.chipInstructionDropdown;
        },
        chipInstructionSizes() {
            return this.$store.state.chipInstructionSizes;
        },
        chipInstructionUrls() {
            return this.$store.state.chipInstructionUrls;
        }
    },
    components: {
        LMap,
        LImageOverlay,
        LMarker,
        LTooltip,
        //ChipPointSelectionTextArea
    },
    props: {
        
    },
    methods: {
        handlePointDialogOff() {
            this.$store.dispatch('changeDialogPointSelection', false);
        },
        getMapImage() {
            if(this.chipFrontUrl !== "") {
                var filename_front = this.chipFrontUrl.replace(/^.*[\\/]/, '');
                let chip_image_path = "http://" + this.localHostName + "/chip_images/originals/" + filename_front;
                console.log(chip_image_path);
                console.log(this.mapBounds);
                return chip_image_path;
            }
            return "";
        },
        calculateDistance(point1, point2) {
            return Math.pow(point2[0] - point1[0], 2) + Math.pow(point2[1] - point1[1], 2);
        },
        getOverlayMapImage() {
            if(this.overlayMapImage !== "") {
                // var filename_front = this.chipInstructionDropdown[this.currentIndex].value.replace(/^.*[\\/]/, '');
                // let chip_image_path = "http://" + this.localHostName + "/chip_images/instructions/" + filename_front;
                // console.log(chip_image_path);
                // console.log(this.mapBounds);
                // return chip_image_path;
                console.log(this.chipInstructionDropdown);
                return this.chipInstructionDropdown[this.currentIndex].value;
            }
            return "";    
        },
        addMarker(event) {
            console.log(event);
            console.log(this.currentIndex);
            console.log(this.markers);
            if(this.markers[this.currentIndex].length <= 3) {
                let newMarker = {};
                let label = this.markers[this.currentIndex].length + 1
                // let label = 1
                // if(this.markers[this.currentIndex].length) {
                //     label = this.markers[this.currentIndex].length;
                // }
                newMarker = {label: label, lat: event.latlng["lat"], lng: event.latlng["lng"]};
                console.log(newMarker);
                this.markers[this.currentIndex].push(newMarker);
                console.log(this.markers);

                if(label > 1 && label < 4 ) {
                    console.log("Hello")
                    let point1 = this.markers[this.currentIndex][label-2]
                    let point2 = this.markers[this.currentIndex][label-1]
                    console.log(point1);
                    console.log(point2);
        
                    let distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);
                    console.log(distance);
                    let tempObj = {
                        pt1: label,
                        pt2: label-1,
                        distance: distance
                    }
                    this.original_distances[this.currentIndex].push(tempObj);
                }
                else if(label === 4) {
                    console.log("I'm in ")
                    let point1 = this.markers[this.currentIndex][2];
                    let point2 = this.markers[this.currentIndex][3];
                    let distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);

                    let tempObj = {
                        pt1: 3,
                        pt2: 4,
                        distance: distance
                    }
                    this.original_distances[this.currentIndex].push(tempObj);

                    point1 = this.markers[this.currentIndex][0]
                    point2 = this.markers[this.currentIndex][3]
                    distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);

                    tempObj = {
                        pt1: 1,
                        pt2: 4,
                        distance: distance
                    }
                    this.original_distances[this.currentIndex].push(tempObj);
                }
                console.log(this.original_distances[this.currentIndex])
                console.log(this.instruction_distances[this.currentIndex])
            }
        },
        addInstructionMarker(event) {
            console.log(this.instructionMarkers);
            if(this.instructionMarkers[this.currentIndex].length <= 3) {
                console.log(event);
                let newMarker = {};
                let label = this.instructionMarkers[this.currentIndex].length + 1
                // let label = 1
                // if(this.instructionMarkers[this.currentIndex].length) {
                //     label = this.instructionMarkers[this.currentIndex].length;
                // }
                newMarker = {label: label, lat: event.latlng["lat"], lng: event.latlng["lng"]};
                console.log(newMarker);
                this.instructionMarkers[this.currentIndex].push(newMarker);
                console.log(this.markers);
                if(label > 1 && label !== 4 ) {
                    let point1 = this.instructionMarkers[this.currentIndex][label-1]
                    let point2 = this.instructionMarkers[this.currentIndex][label-2]
                    let distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);

                    let tempObj = {
                        pt1: label,
                        pt2: label-1,
                        distance: distance
                    }
                    this.instruction_distances[this.currentIndex].push(tempObj);
                }
                else if(label === 4) {
                    let point1 = this.instructionMarkers[this.currentIndex][2];
                    let point2 = this.instructionMarkers[this.currentIndex][3];
                    let distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);

                    let tempObj = {
                        pt1: 3,
                        pt2: 4,
                        distance: distance
                    }
                    this.instruction_distances[this.currentIndex].push(tempObj);

                    point1 = this.instructionMarkers[this.currentIndex][0]
                    point2 = this.instructionMarkers[this.currentIndex][3]
                    distance = this.calculateDistance([point1.lat, point1.lng], [point2.lat, point2.lng]);

                    tempObj = {
                        pt1: 1,
                        pt2: 4,
                        distance: distance
                    }
                    this.instruction_distances[this.currentIndex].push(tempObj);
                }
            }
        },
        getInstructionMarkerFromCoords(coord) {
            for(let i = 0; i < this.instructionMarkers[this.currentIndex].length; ++i) {
                if(this.instructionMarkers[this.currentIndex][i].lat === coord[0] && this.instructionMarkers[this.currentIndex][i].lng === coord[1]) {
                    return this.instructionMarkers[this.currentIndex][i];
                }
            }
            return {};
        },
        dragInstructionStartHandler(e) {
            console.log(e);
            let coords = [e.target._latlng.lat, e.target._latlng.lng];
            this.currentPoint = this.getMarkerFromCoords(coords)
        },
        dragInstructionEndHandler(e) {
            console.log(e);
            let coords = [e.target._latlng.lat, e.target._latlng.lng];
            for(let i = 0; i < this.instructionMarkers[this.currentIndex].length; ++i) {
                if(this.instructionMarkers[this.currentIndex][i] === this.currentPoint) {
                    this.instructionMarkers[this.currentIndex][i].lat = coords[0];
                    this.instructionMarkers[this.currentIndex][i].lng = coords[1];
                }
            }
        },
        getMarkerFromCoords(coord) {
            for(let i = 0; i < this.markers[this.currentIndex].length; ++i) {
                if(this.markers[this.currentIndex][i].lat === coord[0] && this.markers[this.currentIndex][i].lng === coord[1]) {
                    return this.markers[this.currentIndex][i];
                }
            }
            return {};
        },
        dragStartHandler(e) {
            console.log(e);
            let coords = [e.target._latlng.lat, e.target._latlng.lng];
            this.currentPoint = this.getMarkerFromCoords(coords)
        },
        dragEndHandler(e) {
            console.log(e);
            let coords = [e.target._latlng.lat, e.target._latlng.lng];
            for(let i = 0; i < this.markers[this.currentIndex].length; ++i) {
                if(this.markers[this.currentIndex][i] === this.currentPoint) {
                    this.markers[this.currentIndex][i].lat = coords[0];
                    this.markers[this.currentIndex][i].lng = coords[1];
                }
            }
        },
        handleChangeDropdown(event) {
            console.log(event);
            console.log(this.chipInstructionDropdown);
            let instructionIndex = 0; 
            for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
                if(event === this.chipInstructionDropdown[i].value) {
                    instructionIndex = i;
                }
            }
            console.log(instructionIndex)
            this.chip_instruction_index = instructionIndex;
            this.chip_instruction_url = event;
            this.currentIndex = instructionIndex;
            console.log(this.chipInstructionSizes[instructionIndex][1], this.chipInstructionSizes[instructionIndex][0]);
            this.instructionMapBounds = [this.chipInstructionSizes[instructionIndex][1], this.chipInstructionSizes[instructionIndex][0]];
            this.overlayMapImage = this.chipInstructionDropdown[instructionIndex].text;
            console.log(this.markers);
            console.log(instructionIndex);
            console.log(this.chipInstructionSizes);
        },
        handleContinue() {
            let pointJson = {
                original: {
                    image: this.chipFrontUrl
                    ,image_size: this.chipFrontSize
                    ,orig_instruct_points: []
                }
                ,instructions: []
            };
            let tempPoint = [];
            console.log(this.chipInstructionSizes);
            for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
                pointJson["original"]["orig_instruct_points"].push([]);
                pointJson["instructions"].push({
                    image: this.chipInstructionUrls[i]
                    ,image_size: this.chipInstructionSizes[i]
                    ,points: []
                });

                for(let j = 0; j < this.markers[i].length; ++j) {
                    tempPoint = [this.markers[i][j]["lng"], this.markers[i][j]["lat"]];
                    pointJson["original"]["orig_instruct_points"][i].push(tempPoint);
                }

                for(let j = 0; j < this.instructionMarkers[i].length; ++j) {
                    tempPoint = [this.instructionMarkers[i][j]["lng"], this.instructionMarkers[i][j]["lat"]];
                    pointJson["instructions"][i]["points"].push(tempPoint);
                }
            }

            console.log(pointJson);

            this.uploadPoints(pointJson);

        },
        async uploadPoints(pointJson) {
            this.$store.dispatch("changeLoading", true);

            let passJson = {
                original: {
                    image: pointJson["original"]["image"]
                    ,image_size: this.chipFrontSize
                    ,points: []
                },
                instruction: {
                    image: ""
                    ,image_size: []
                    ,points: []
                }
            };
            let newDropdown = [];
            let adjDropdown = [];
            let tempUrlArr = [];
            let tempFile = "";
            let tempPath = "";

            for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
                passJson["original"]["points"] = pointJson["original"]["orig_instruct_points"][i];
                passJson["instruction"]["image"] = pointJson["instructions"][i]["image"];
                passJson["instruction"]["image_size"] = pointJson["instructions"][i]["image_size"];
                passJson["instruction"]["points"] = pointJson["instructions"][i]["points"];
                console.log(passJson);
                await this.axios.post("http://" + this.databaseLocalHost + "/imageAdjust", passJson)
                .then(response => {
                    console.log(response);
                    let newFileImage = response["data"];
                    
                    tempUrlArr.push(newFileImage);
                    tempFile = newFileImage.split('/').pop();
                    //tempPath = "http://" + this.localHostName + "/chip_images/instructions_adj/" + tempFile;
                    tempPath = "http://" + this.databaseLocalHost + "/static/" + tempFile;
                    newDropdown.push({text: tempFile, value: tempPath});
                    adjDropdown.push(tempPath);
                }).catch(error => {
                    console.log(error);
                    return;
                });

            }
            this.$store.dispatch("changeChipInstructionAdjustDropdown", newDropdown);
            this.$store.dispatch("changeChipInstructionAdjustDropdownAdj", adjDropdown);
            console.log(newDropdown);
            console.log(tempUrlArr);
            this.$store.dispatch("changeChipInstructionAdjustUrls", tempUrlArr);
            this.$store.dispatch("changeLoading", false);
            this.$store.dispatch("changeShowPaintTool", true);
            this.$store.dispatch("changeDialogPointSelection", false);
        },
        setUpPointSelection() {
            console.log(this.chipInstructionDropdown);
            console.log(this.markers);
            for(let i = 0; i < this.chipInstructionDropdown.length; ++i) {
                this.markers.push([]);
                this.instructionMarkers.push([]);
                this.original_distances.push([]);
                this.instruction_distances.push([]);
            }

        }
    }
}
</script>

<style scoped>
    #mapid { 
        height: 60vh; 
        width: 80vh;
        z-index: 0;
        display: block;
        align-items: center;
    }
    .leaflet-tooltip {
        background-color: #006FFF;
        color: #FFFFFF;
    }


</style>