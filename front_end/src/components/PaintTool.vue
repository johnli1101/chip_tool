<template>
  <!--main div-->
  <div id="app">
    <div v-if="overlays">
      <div v-for="(image, index) in overlays" v-bind:key="index">
        <img :src="image" alt="" :id="'id-overlay'+index" crossorigin="anonymous"/>
      </div>
    </div>

    <v-row
        align="center"
        justify="space-around"
    >
      <v-col
          cols="12"
          class="py-2"
      >
        <v-btn-toggle tile color="deep-purple accent-3" group>
          <v-btn @click="createRectangle(canvas)">
            <v-icon dark>
              mdi-rectangle-outline
            </v-icon>
            Add Rectangle
          </v-btn>
          <v-divider
              vertical
          ></v-divider>

          <v-btn @click="createCircle(canvas)">
            <v-icon dark>
              mdi-circle-outline
            </v-icon>
            Add Circles
          </v-btn>
          <v-divider
              vertical
          ></v-divider>

          <v-btn @click="createLine(canvas)">
            <v-icon dark>
              mdi-slash-forward
            </v-icon>
            Add Lines
          </v-btn>
          <v-divider
              vertical
          ></v-divider>

          <v-btn @click="createText(canvas)">
            <v-icon dark>
              mdi-format-textbox
            </v-icon>
            Add Text
          </v-btn>
          <v-divider
              vertical
          ></v-divider>

          <v-btn @click="deactivateLine(canvas)">
            <v-icon dark>
              mdi-select-drag
            </v-icon>
            Drag Shape
          </v-btn>
          <v-divider
              vertical
          ></v-divider>
          <v-btn @click="undo(canvas)">
            <v-icon dark>
              mdi-delete-empty-outline
            </v-icon>
            Delete shape
          </v-btn>

        </v-btn-toggle>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col
          class="d-flex"
          cols="12"
          md="6">
        <v-divider
            vertical
        ></v-divider>
      </v-col>
      <!-- Manage Overlays and transparency -->
    </v-row>
    <v-card
        class="d-flex justify-center mb-6"
        flat
    >
      <v-card
          class="pa-2"
          outlined
      >
        <div class="select">
              <select id="overlays-id" @change="handler($event,canvas)">
                <option value="" selected="selected" disabled="disabled">Select overlay</option>
                <option value="none">None</option> <!--index : yebda 0 -->
                <option v-for="(index, i) in overlays.length" v-bind:key="index" :value="'id-overlay'+i">{{"overlay"+i}}</option>
              </select>
        </div>
      </v-card>
      <v-card
          class="pa-2"
          outlined
      >
        <div class="rangeSlider">
        <label for="range" class="form-label">Set Overlay transparency</label><br>
        <input type="range" class="form-range" id="range" min="0" max="100" value="50"
               oninput="this.nextElementSibling.value = this.value">
        <output for="range" id="slider-value"></output>
        </div>
      </v-card>
    </v-card>

    <v-card class="mx-auto" max-width="730">
      <v-col cols="12" class="py-2">
        <v-btn-toggle tile color="deep-purple accent-3" group>
          <v-btn @click="switchView1(canvas)"> View 1</v-btn>
          <v-divider
              vertical
          ></v-divider>
          <v-btn @click="switchView2(canvas)"> View 2</v-btn>
          <v-divider
              vertical
          ></v-divider>
          <v-btn @click="downloadImg(canvas)"><a id="download" download="image.png"></a> Save</v-btn>
          <v-divider
              vertical
          ></v-divider>
          <!-- <v-btn @click="rasterize()">Export</v-btn> -->
        </v-btn-toggle>
        <v-divider></v-divider>
      </v-col>

      <!-- Paintable canvas -->
      <canvas ref="can" id="fabricCanvas" class="canvasLayout"></canvas>

      <!-- import image -->
      <img src="" id="imgConverted">
      <div v-if="images">
        <div v-for="(image, index) in images" v-bind:key="index">
          <img :src="image" alt="" id="image_id"/>
          <button @click="removeImage(index)" class="btn btn-primary">Remove image</button>
        </div>
      </div>
      <v-card-actions>
        <v-btn
            color="red"
            text
            @click="clearCanvas(canvas)"> Clear canvas
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
//import libraries
import {fabric} from "fabric";
import html2canvas from "html2canvas";

export default {
  name: "PaintTool",
  components: {},
  created() {
    this.$root.$refs.PaintTool = this;
  },
  props: {
    data() {
    },
    canvasWidth: null,
    canvasHeight: null,
    background_image_view1: String,
    background_image_view2: String,
    overlays: Array,
    background_image_size: Array,
    saveViews: {},
  },
  data: function () {
    return {
      images: [],
      vueCanvas: null,
      publicPath: process.env.BASE_URL,
      selectOverlay: {value: null, text: 'None'},
    };
  },

  mounted() {
    this.image1 = new Image();
    this.image2 = new Image();
    const ref = this.$refs.can;
    const canvas = new fabric.Canvas(ref, {
      width: this.background_image_size[0], //800
      height: this.background_image_size[1], //350 500 this.background_image_size[1]
    });
    this.canvas = canvas;
    this.vueCanvas = canvas.getContext();
    /*this.view2Save = canvas.toObject(["cacheKey", "selectable", "opacity"]);
    this.view1image.src = canvas.toDataURL("image/png")*/


    //init switch views
    this.currentView = 1;
    this.view1Save = {};
    this.view2Save = {};


    this.view1 = document.querySelector(".one");
    this.view2 = document.querySelector(".two");

    fabric.Image.fromURL(this.background_image_view1,
        function(img) {
          img.set({
            left: 0,
            top: 0,
          });
          //img.set({height: this.background_image_size[0], width:this.background_image_size[1] }); //background_image_height = 500
          img.scaleToHeight(this.background_image_size[0]); //background_image_height = 500
          img.scaleToWidth(this.background_image_size[1]); //background_image_width = 500
          this.canvas.backgroundImage = img;
          this.canvas.renderAll();
        }.bind(this), 
        {crossOrigin: "anonymous"}
    );

    /*const select = document.getElementById("overlays-id");
    if (select.value == "Overlay 0") {
      console.log(select.value);
    }*/
    this.range = document.getElementById("range");
    this.rangevalue = this.range.value / this.range.max;

    this.lastelement = "";
    this.index;
    this.tab = {};
    this.last = {};

    //this.filepath = '../assets/filepath.png'
    //this.filepath = 'C:\\Users\\Wafa\\Desktop\\WORK\\15-RUTILEA\\edited_image.png'

  },
  methods: {
    //method to download canvas as image (before/after painting)

    async downloadImg() {
      const options = {};
      var image = document.getElementsByClassName("lower-canvas")[0];
      const printCanvas = await html2canvas(image, options);
      // const link = document.createElement("a");
      // link.setAttribute("download", "Edited_Image.png");
      // link.setAttribute(
      //     "href",
      //     printCanvas
      //         .toDataURL("image/png")
      //         .replace("image/png", "image/octet-stream" ),
      // );
      console.log(printCanvas.src)
      //link.click();
      let image_data = printCanvas.toDataURL("image/png");
      console.log(image_data);
      if(this.currentView === 1) {
        this.$store.dispatch("changeChipFrontNewImageData", image_data);
      }
      else {
        this.$store.dispatch("changeChipBackNewImageData", image_data);
      }
    },

    //method to Switch from "view 1" to "view 2"
    switchView1(canvas) {
      const select = document.getElementById("overlays-id");

      for (var i = 0; i < canvas._objects.length; i++) {
        switch (this.last["view1"]) {
          case 'id-overlay'+i:
            select.value = 'id-overlay'+i;
            break;
          /*default:
            select.value = "none";
            break;*/
        }
      }

      if (this.currentView === 2) {
        if (this.last["view1"] != undefined) {
          this.lastelement = this.last["view2"];
        }
        console.log(this.lastelement)

        this.view2Save = canvas.toObject(["cacheKey", "selectable", "opacity"]);
        //this.image2.src = canvas.toDataURL('image/png')
        //console.log("VIEW1 :view2image.src", this.$view2image.src)
        canvas.clear();
        canvas.loadFromJSON(this.view1Save, this.canvas.renderAll.bind(canvas));
        this.currentView = 1;
        /*this.view1.disabled = true;
        this.view2.disabled = false;*/

        this.range.addEventListener("change", () => {
          canvas._objects[0].set({opacity: this.range.value / this.range.max});
          canvas.renderAll();
        });
      }
      console.log(this.currentView);
      console.log("view2 save : ", this.view2Save);
    },

    //method to switch from "view 2" to "view 1"
    switchView2(canvas) {
      //used for select management
      const select = document.getElementById("overlays-id");

      for (var i = 0; i < canvas._objects.length; i++) {
        switch (this.last["view2"]) {
          case 'id-overlay'+i:
          select.value = 'id-overlay'+i;
            break;
          /*default:
            select.value = "none";
            break;*/
        }
      }

      fabric.Image.fromURL(this.background_image_view2,
          function(img) {
            img.set({
              left: 0,
              top: 0,
            });
            img.scaleToHeight(this.background_image_size[0]);
            img.scaleToWidth(this.background_image_size[1]);

            /*img.resize(this.background_image_size[0], this.background_image_size[1])
            img.resizeTo(this.background_image_size[0], this.background_image_size[1])*/
            this.canvas.backgroundImage = img;
            this.canvas.renderAll();
            console.log("height", img.height, "width", img.width)
          }.bind(this),
          {crossOrigin: "anonymous"}
      );
      if (this.currentView === 1) {
        if (this.last["view2"] != undefined) {
          this.lastelement = this.last["view2"];
        }

        this.view1Save = canvas.toObject(["cacheKey", "selectable", "opacity"]);
        //this.image1.src = canvas.toDataURL('image/png')
        //console.log("VIEW2 : view1image.src", this.$view1image.src)
        canvas.clear();
        canvas.loadFromJSON(this.view2Save, canvas.renderAll.bind(canvas));
        this.currentView = 2;
        /*this.view1.disabled = false;
        this.view2.disabled = true;*/
      }
      console.log(this.currentView);
      console.log("view 1 save : ", this.view2Save);
    },

    //method to select between overlays to display on canvas
    handler(event, canvas) {
      console.log(event.target.value)
      if (event.target.value == "none") {
        for (i = 0; i < canvas._objects.length; i++) {
          if (canvas._objects[i].cacheKey == this.lastelement) {
            canvas.remove(canvas._objects[index]);
          }
        }
      }

      for (var i = 0; i < canvas._objects.length; i++) {
        if (canvas._objects[i].cacheKey == this.lastelement) {
          var index = i;
        }
      }

      //console.log(event.target.value);
      if (this.lastelement != "") {
        this.tab[this.lastelement] = canvas._objects[index];
      }
      var overlayElement = document.getElementById(event.target.value);
      //var range = document.getElementById("range");
      if (this.tab[event.target.value] == undefined) {
        var overlayInstance = new fabric.Image(overlayElement, {
          cacheKey: event.target.value,
          index: 1,
          selectable: false
        }, {crossOrigin: 'anonymous'});
        overlayInstance.scaleToHeight(this.background_image_size[0]);
        overlayInstance.scaleToWidth(this.background_image_size[1]);
      } else {
        overlayInstance = this.tab[event.target.value];
      }
      if (index != null) {
        canvas.remove(canvas._objects[index]);
      }
      canvas.add(overlayInstance);
      canvas.moveTo(overlayInstance, 0);

      this.index = canvas._objects.length - 1;
      this.lastelement = event.target.value;
      if (this.currentView === 1) {
        this.last["view1"] = event.target.value;
      } else {
        this.last["view2"] = event.target.value;
      }
      overlayInstance.set({opacity: this.rangevalue});
      //overlayInstance.on("selected", () => {
      this.range.addEventListener("change", () => {
        overlayInstance.set({opacity: this.range.value / this.range.max});
        console.log(overlayInstance.opacity);
        canvas.renderAll();
      });
      //});
    },

    //display canvas background image
    imageBackground(canvas) {
      const imgElement = document.getElementById('image_id');
      if (this.currentView === 1 || this.currentView === 2) {
        const imgInstance = new fabric.Image(imgElement, {
          selectable: false,
          index: -1,
        });
        imgInstance.scaleToHeight(this.imageHeight);
        imgInstance.scaleToWidth(this.imageWidth);
        //canvas.add(imgInstance);
        //console.log(imgInstance.height, imgInstance.width)
        this.canvas.backgroundImage = imgInstance
        this.canvas.renderAll()

        imgInstance.on('deselected', () => {
          canvas.requestRenderAll()
        });
      }
      this.images.pop()
    },

    //Import images to the paint tool
    onFileChange(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.createImage(files);
    },
    createImage(files) {
      let vm = this;
      for (let index = 0; index < files.length; index++) {
        let reader = new FileReader();
        reader.onload = function (event) {
          const imageUrl = event.target.result;
          vm.images.push(imageUrl);
        };
        reader.readAsDataURL(files[index]);
      }
    },
    removeImage(index) {
      this.images.splice(index, 1);
    },

    /* adding shapes to canvas */

    //Drawing circle function
    createCircle(canvas) {
      var isDrawing
      var circle;
      var origX;
      //var origY;
      canvas.on('mouse:down', (o) => {
        isDrawing = true;
        var pointer = canvas.getPointer(o.e);
        origX = pointer.x;
        //origY = pointer.y;
        //var points = [pointer.x, pointer.y, pointer.x, pointer.y];
        circle = new fabric.Circle({
          id: 'added-circle',
          left: pointer.x,
          top: pointer.y,
          radius: 1,
          strokeWidth: 2,
          stroke: 'red',
          fill: 'transparent',
          selectable: true,
          originX: 'center', originY: 'center',
        });
        canvas.add(circle);
        canvas.setActiveObject(circle);
      });

      canvas.on('mouse:move', function (o) {
        if (isDrawing) {
          var pointer = canvas.getPointer(o.e);
          circle.set({radius: Math.abs(origX - pointer.x)});
          canvas.renderAll();
        }
      });

      canvas.on('mouse:up', function () {
        //circle.setCoords();
        isDrawing = false;
      });
      canvas.selection = false
      canvas.hoverCursor = "auto"
      canvas.renderAll();

    },

    //Drawing rectangle function
    createRectangle(canvas) {
      var isDrawing
      var rect;
      var x = 0;
      var y = 0;
      canvas.on('mouse:down', (o) => {
        isDrawing = true;
        var pointer = canvas.getPointer(o.e);
        console.log(pointer)
        //var points = [pointer.x, pointer.y, pointer.x, pointer.y];
        x = pointer.x;
        y = pointer.y;
        console.log(pointer.x, pointer.y)
        rect = new fabric.Rect({
          id: "added-rect",
          width: 1,
          height: 1,
          fill: "transparent",
          strokeWidth: 5,
          stroke: "red",
          selectable: false,
          hasRotatingPoint: true,
          left: pointer.x,
          top: pointer.y,
        });
        canvas.add(rect);
        canvas.setActiveObject(rect);
        console.log(rect)
      });

      canvas.on('mouse:move', function (o) {
        if (!isDrawing) {
          return false;
        } else if (isDrawing) {
          var pointer = canvas.getPointer(o.e);
          x = Math.min(pointer.x, x),
              y = Math.min(pointer.y, y)
          var w = Math.abs(pointer.x - x),
              h = Math.abs(pointer.y - y);

          if (!w || !h) {
            return false;
          }

          var rect = canvas.getActiveObject();

          rect.set('top', y).set('left', x).set('width', w).set('height', h);

          canvas.renderAll();
        }
      });
      canvas.on('mouse:up', function () {
        rect.setCoords();
        isDrawing = false;

        //lezem dima nenzel aala add rect beshh yjiiblii rectangle
        canvas.off('mouse:down')
        canvas.off('mouse:move')
        canvas.off('mouse:up')
      });
      canvas.selection = false
      canvas.hoverCursor = "auto"
      canvas.renderAll();
    },

    //Drawing Line function
    createLine(canvas) {
      var isDrawing
      var line;
      canvas.on('mouse:down', (o) => {
        isDrawing = true;
        var pointer = canvas.getPointer(o.e);
        console.log(pointer)
        var points = [pointer.x, pointer.y, pointer.x, pointer.y];
        console.log(pointer.x, pointer.y)
        line = new fabric.Line(points, {
          id: "added-line",
          strokeWidth: 5,
          stroke: "red",
          selectable: false,
          hasRotatingPoint: true,
        });
        canvas.add(line);
        console.log(line)
      });

      canvas.on('mouse:move', function (o) {
        if (isDrawing) {
          var pointer = canvas.getPointer(o.e);
          line.set({x2: pointer.x, y2: pointer.y});
          //line.set()
          canvas.renderAll();
        }
      });

      canvas.on('mouse:up', function () {
        line.setCoords();
        isDrawing = false;
      });
      canvas.selection = false
      canvas.hoverCursor = "auto"
      canvas.renderAll();
    },

    //Drag mode function
    deactivateLine(canvas) {
      /*var isDrawing
      var line;*/
      canvas.off('mouse:down')
      canvas.off('mouse:move')
      canvas.off('mouse:up')

      canvas.getObjects().forEach(o => {
        if (o.id === 'added-line') {
          o.set({
            selectable: true
          })
        } else if (o.id === 'added-rect') {
          o.set({
            selectable: true
          })
        } else if (o.id === 'added-circle') {
          o.set({
            selectable: true
          })
        }
      })
    },

    //Add text function
    createText(canvas) {
      const txt = new fabric.IText('here', {
        fontFamily: 'arial black',
        left: 100,
        top: 100,
        //myid: newID,
        objecttype: 'text'
      });
      canvas.add(txt);
      canvas.renderAll();
    },

    //Delete selected shape
    undo(canvas) {
      if (canvas._objects.length > 0) {
        console.log(canvas._objects.length);
        canvas.remove(canvas.getActiveObject());
      }
    },

    //Clear canvas
    clearCanvas(canvas) {
      const select = document.getElementById("overlays-id");
      if (canvas._objects.length > 0) {
      for (var i = 0; i < canvas._objects.length; i++) {
          canvas.remove(canvas._objects[i]);
          //canvas.clear(canvas._objects[i])
        select.value = "none";
        }
      }
    },
    /*restoreCanvas(canvas){
      canvas.restore()
    },*/

    rasterize() {
      if(this.currentView === 1) {
        this.$view1image.src = this.canvas.toDataURL("image/png")
        this.$view2image.src = this.image2.src
      }
      else if (this.currentView === 2) {
        this.$view1image.src = this.image1.src
        this.$view2image.src = this.canvas.toDataURL("image/png")
      }
      console.log("IMAGE 1", this.$view1image.src)
      console.log("IMAGE 2", this.$view2image.src)

      // this.store.dispatch("changeChipFrontNewImageData", this.$view1image.src);
      // this.store.dispatch("changeChipBackNewImageData", this.$view2image.src);

      return ({"this.view1image": this.$view1image.src, "this.view2image":this.$view2image.src})
    },
  },
};
</script>

<style scoped>
#app {
  margin-left: 200px;
}

img {
  width: 100%;
  margin: auto;
  /*display: block;*/
  /*margin-bottom: 10px;*/
  display: none;
}

.v-bottom-navigation.v-bottom-navigation v-btn {
  font-size: .75rem;
}

.img1,
.img2 {
  opacity: 0.5;
  display: none;
}

h1 {
  margin-left: 200px;
}

/* The container must be positioned relative: */
/*select {
  !*margin-left: 150px;*!
  width: 300px;
  display: inline-block;
  font-size: 16px;
  position: relative;
  text-align: left;
  -webkit-appearance: none;
  -moz-appearance: none;
  border: 0;
  border-bottom: 2px solid
}*/
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  appearance: none;
  outline: 0;
  background-image: none;
  width: 100%;
  height: 100%;
  margin: 0 ;
  padding: 0 0 0 .5em;
  cursor: pointer;
}

.select {
  position: relative;
  display: block;
  width: 20em;
  height: 3em;
  line-height: 3;
  overflow: hidden;
  border-radius: .25em;
}

select::-ms-expand {
  display: none;
}
.select::after {
  content: '\25BC';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  padding: 0 1em;
  background: whitesmoke;
  pointer-events: none;
  -webkit-transition: .25s all ease;
  -o-transition: .25s all ease;
  transition: .25s all ease;
}
.select:hover::after {
  color: #F39C12;
}

.rangeSlider{
  position: relative;
  display: block;
  width: 20em;
  height: 3em;
  line-height: 3;
  overflow: hidden;
  border-radius: .25em;
}

input[type=range] {
  height: 22px;
  -webkit-appearance: none;
  margin: 10px 0;
  width: 80%;
}
input[type=range]:focus {
  outline: none;
}
input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 1px 1px 1px #E3E3E3;
  background: #E3E3E3;
  border-radius: 4px;
  border: 1px solid #E3E3E3;
}
input[type=range]::-webkit-slider-thumb {
  box-shadow: 0px 0px 0px #E0E0E0;
  border: 0px solid #2A99D1;
  height: 16px;
  width: 16px;
  border-radius: 15px;
  background: #2A99D1;
  cursor: pointer;
  -webkit-appearance: none;
  margin-top: -6.5px;
}
input[type=range]:focus::-webkit-slider-runnable-track {
  background: #E3E3E3;
}
input[type=range]::-moz-range-track {
  width: 100%;
  height: 4px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 1px 1px 1px #E3E3E3;
  background: #E3E3E3;
  border-radius: 4px;
  border: 1px solid #E3E3E3;
}
input[type=range]::-moz-range-thumb {
  box-shadow: 0px 0px 0px #E0E0E0;
  border: 0px solid #2A99D1;
  height: 16px;
  width: 16px;
  border-radius: 15px;
  background: #2A99D1;
  cursor: pointer;
}
input[type=range]::-ms-track {
  width: 100%;
  height: 4px;
  cursor: pointer;
  animate: 0.2s;
  background: transparent;
  border-color: transparent;
  color: transparent;
}
input[type=range]::-ms-fill-lower {
  background: #E3E3E3;
  border: 1px solid #E3E3E3;
  border-radius: 8px;
  box-shadow: 1px 1px 1px #E3E3E3;
}
input[type=range]::-ms-fill-upper {
  background: #E3E3E3;
  border: 1px solid #E3E3E3;
  border-radius: 8px;
  box-shadow: 1px 1px 1px #E3E3E3;
}
input[type=range]::-ms-thumb {
  margin-top: 1px;
  box-shadow: 0px 0px 0px #E0E0E0;
  border: 0px solid #2A99D1;
  height: 16px;
  width: 16px;
  border-radius: 15px;
  background: #2A99D1;
  cursor: pointer;
}
input[type=range]:focus::-ms-fill-lower {
  background: #E3E3E3;
}
input[type=range]:focus::-ms-fill-upper {
  background: #E3E3E3;
}

</style>