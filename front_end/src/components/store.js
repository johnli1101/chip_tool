import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        localHostName: "localhost:8080"         //localhost link for front end
        ,databaseLocalHost: "localhost:5000"    //localhost link for python backend
        ,globalMode: "fileUpload"                         
        ,template: ""                           //template type chosen when exporting
        ,loading: false                         //for loading spinner
        ,errorMsg: []                           //error message array
        ,showError: false                       //boolean for showing error on alert
        ,chipInstructionUrls: []                //image for cutting line instructions
        ,chipInstructionSizes: []               //size of image of chip instruction
        ,chipInstructionAdjustUrls: []
        ,chipFrontUrl: ""                       //image for chip
        ,chipFrontUrlAdj: ""
        ,chipFrontNewImageData: ""
        ,chipBackNewImageData: ""
        ,chipFrontPaintImageUrl: ""
        ,chipBackPaintImageUrl: ""
        ,chipBackUrlAdj: ""
        ,chipFrontSize: [0, 0]                  //size of image of chip instruction
        ,currentEditImage: ""                   //edit of final image
        ,mapBounds: [0, 0]
        ,chipBackUrl: ""                        //image for chip
        ,chipInstructionDropdown: []
        ,chipInstructionAdjustDropdown: []
        ,chipInstructionAdjustDropdownAdj: []
        ,chipBackSize: [0, 0]                   //size of image of chip instruction
        ,tabMode: "front"                       //tab control for front or back side of chips
        ,showPaintTool: false                   //bool to showing the paint tool
        ,dialogFileUpload: false                //dialog variable control for file upload
        ,dialogTransparency: false              //dialog variable control for transparency
        ,dialogPointSelection: false
        ,dialogCropping: false                  //cropping 
    },
    mutations: {
        // ----- misc changes -----
        changeLoading(state, load) {
            state.loading = load;
        },
        changeGlobalMode(state, mode) {
            state.globalMode = mode;
        },
        changeTemplate(state, template) {
            state.template = template;
        },
        changeTabMode(state, mode) {
            state.tabMode = mode;
        },
        changeMapBounds(state, sizeArr) {
            console.log(sizeArr)
            state.mapBounds = [sizeArr[1], sizeArr[0]];
        },
        changeErrorMsg(state, errorArr) {
            state.errorMsg = errorArr;
        },
        changeShowError(state, bool) {
            state.showError = bool;
        },
        changeCurrentEditImage(state, filePath) {
            state.currentEditImage = filePath;
        },
        changeShowPaintTool(state, mode) {
            state.showPaintTool = mode;
        },
        // ----- changing chip mutations ----
        changeChipInstructionUrls(state, filePaths) {
            state.chipInstructionUrls = filePaths;
        },
        changeChipInstructionSizes(state, sizeArr) {
            state.chipInstructionSizes = sizeArr;
        },
        changeChipInstructionAdjustUrls(state, urlArr) {
            state.chipInstructionAdjustUrls = urlArr;
        },
        changeChipInstructionDropdown(state, list) {
            state.chipInstructionDropdown = list;
        },
        changeChipInstructionAdjustDropdown(state, list) {
            state.chipInstructionAdjustDropdown = list;
        },
        changeChipInstructionAdjustDropdownAdj(state, list) {
            state.chipInstructionAdjustDropdownAdj = list;
        },
        changeChipFrontUrl (state, filePath) {
            state.chipFrontUrl = filePath;
        },
        changeChipFrontUrlAdj (state, filePath) {
            state.chipFrontUrlAdj = filePath;
        },
        changeChipFrontSize (state, size) {
            state.chipFrontSize = size;
        },
        changeChipFrontNewImageData (state, data) {
            state.chipFrontNewImageData = data;
        },
        changeChipBackNewImageData (state, data) {
            state.chipBackNewImageData = data;
        },
        changeChipFrontPaintImageUrl (state, data) {
            state.chipFrontPaintImageUrl = data;
        },
        changeChipBackPaintImageUrl (state, data) {
            state.chipBackPaintImageUrl = data;
        },
        changeChipBackUrlAdj (state, filePath) {
            state.chipBackUrlAdj = filePath;
        },
        changeChipBackUrl (state, filePath) {
            state.chipBackUrl = filePath;
        },
        changeChipBackSize (state, size) {
            state.chipBackSize = size;
        },
        // ----- dialog control mutations ----
        changeDialogFileUpload(state, mode) {
            state.dialogFileUpload = mode;
        },
        changeDialogTransparency(state, mode) {
            state.dialogTransparency = mode;
        },
        changeDialogPointSelection(state, mode) {
            state.dialogPointSelection = mode;
        },
        changeDialogCropping(state, mode) {
            state.dialogCropping = mode;
        },
    },
    actions: {
        // ------ misc changes ------
        changeLoading(context, load) {
            context.commit('changeLoading', load);
        },
        changeGlobalMode(context, mode) {
            context.commit('changeGlobalMode', mode);
        },
        changeTemplate(context, template) {
            context.commit('changeTemplate', template);
        },
        changeTabMode(context, mode) {
            context.commit('changeTabMode', mode);
        },
        changeMapBounds(context, sizeArr) {
            context.commit('changeMapBounds', sizeArr);
        },
        changeErrorMsg(context, errorArr) {
            context.commit('changeErrorMsg', errorArr);
        },
        changeShowError(context, bool) {
            context.commit('changeShowError', bool);
        },
        changeCurrentEditImage(context, filePath) {
            context.commit('changeCurrentEditImage', filePath);
        },
        changeShowPaintTool(context, mode) {
            context.commit('changeShowPaintTool', mode);
        },
        // ------  changing chip data ------
        //NOTE: this takes in an array for filepaths
        changeChipInstructionUrls (context, filePaths) {
            context.commit('changeChipInstructionUrls', filePaths);
        },
        changeChipInstructionSizes (context, sizeArr) {
            context.commit('changeChipInstructionSizes', sizeArr);
        },
        changeChipInstructionAdjustUrls (context, urlArr) {
            context.commit('changeChipInstructionAdjustUrls', urlArr);
        },
        changeChipInstructionDropdown(context, list) {
            context.commit('changeChipInstructionDropdown', list);
        },
        changeChipInstructionAdjustDropdown(context, list) {
            context.commit('changeChipInstructionAdjustDropdown', list);
        },
        changeChipInstructionAdjustDropdownAdj(context, list) {
            context.commit('changeChipInstructionAdjustDropdownAdj', list);
        },
        changeChipFrontUrl (context, filePath) {
            context.commit('changeChipFrontUrl', filePath);
        },
        changeChipFrontUrlAdj (context, filePath) {
            context.commit('changeChipFrontUrlAdj', filePath);
        },
        changeChipFrontSize (context, size) {
            context.commit('changeChipFrontSize', size);
        },
        changeChipFrontNewImageData (context, data) {
            context.commit('changeChipFrontNewImageData', data);
        },
        changeChipBackNewImageData (context, data) {
            context.commit('changeChipBackNewImageData', data);
        },
        changeChipFrontPaintImageUrl (context, data) {
            context.commit('changeChipFrontPaintImageUrl', data);
        },
        changeChipBackPaintImageUrl (context, data) {
            context.commit('changeChipBackPaintImageUrl', data);
        },
        changeChipBackUrl (context, filePath) {
            context.commit('changeChipBackUrl', filePath);
        },
        changeChipBackUrlAdj (context, filePath) {
            context.commit('changeChipBackUrlAdj', filePath);
        },
        changeChipBackSize (context, size) {
            context.commit('changeChipBackSize', size);
        },
        // ----- dialog changes ------
        changeDialogFileUpload(context, mode) {
            context.commit('changeDialogFileUpload', mode);
        },
        changeDialogTransparency(context, mode) {
            context.commit('changeDialogTransparency', mode);
        },
        changeDialogPointSelection(context, mode) {
            context.commit('changeDialogPointSelection', mode);
        },
        changeDialogCropping(context, mode) {
            context.commit('changeDialogCropping', mode);
        },
    }
  })