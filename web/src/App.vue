<template>
  <div id="app">
    <div class="row">
      <div class="col-md-6 col-sm-12 col-12">
        <ChartPanel gymCode="GLA" backgroundColor="#264653" />
      </div>
      <div class="col-md-6 col-sm-12 col-12">
        <ChartPanel gymCode="PST" backgroundColor="#2a9d8f" />
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 col-sm-12 col-12">
        <ChartPanel gymCode="BRI" backgroundColor="#14213d" />
      </div>
      <div class="col-md-6 col-sm-12 col-12">
        <ChartPanel gymCode="UNC" backgroundColor="#e76f51" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import { Component, Vue } from "vue-property-decorator";
import ChartPanel from "./components/ChartPanel.vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

@Component({
  components: {
    ChartPanel
  }
})
export default class App extends Vue {}
</script>

<style scoped>
.row {
  margin-top:20px;
}
</style>
