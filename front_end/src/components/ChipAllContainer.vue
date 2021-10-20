
<template>
    <div> 
      <ChipOverlay />
      <ChipContainer v-if="globalMode === 'fileUpload'" />
      <ChipCanvasContainer v-else-if="globalMode === 'paintTool'" />
      <!-- <router-view/> -->
    </div>
</template>

<script>
import ChipOverlay from './ChipOverlay';
import ChipCanvasContainer from './ChipCanvasContainer';
import ChipContainer from './ChipContainer';

export default {
  name: 'Chip',

  components: {
    ChipOverlay
    ,ChipCanvasContainer
    ,ChipContainer
  },
  computed: {
      globalMode() {
        console.log(this.$store.state.globalMode);
          return this.$store.state.globalMode;
      },
  },
  data: () => ({
    //
  })
};
</script>
