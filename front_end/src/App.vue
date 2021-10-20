
<template>
  <v-app>
    <v-main> 
      <ChipCanvasContainer />
      <!-- <router-view/> -->
    </v-main>
  </v-app>
</template>

<script>
//import ChipAllContainer from './components/ChipAllContainer';
import ChipCanvasContainer from './components/ChipCanvasContainer';

export default {
  name: 'Chip',

  components: {
    //ChipAllContainer
    ChipCanvasContainer
  },
  data: () => ({
    //
  })
};
</script>
