<template>
  <div>
    <h1>{{ gymCode }}</h1>
    <Chart v-if="loaded" :gymCode="gymCode" :chart-data="graphData" />
  </div>
</template>

<script type="ts">
import Component from "vue-class-component";
import Chart from "./Chart.vue";
const axios = require("axios").default;
import {
  format,
  yesterday,
  today,
  startOfToday,
  endOfToday,
  formatISO
} from "date-fns";

export default {
  components: {
    Chart
  },
  data() {
    return {
      loaded: false,
      apiData: null,
      graphData: {
        labels: [this.gymCode],
        datasets: [
          {
            backgroundColor: this.backgroundColor,
            label: "Occupancy"
          }
        ],
        options: {
          scales: {
            xAxes: [
              {
                ticks: {},
                type: 'string',
              }
            ]
          }
        }
      }
    };
  },
  props: ["gymCode", "backgroundColor"],
  mounted() {
    this.loaded = false;

    axios
      .get("http://127.0.0.1:9000/" + this.gymCode, {
        params: { from: formatISO(startOfToday()), to: formatISO(endOfToday()) }
      })
      .then(response => {
        this.apiData = response.data.series[0].values;
        this.graphData.datasets[0].data = this.apiData.map(apiDataValue => {
          if (apiDataValue[1] !== null) {
            return apiDataValue[1];
          }
          return 0;
        });
        this.graphData.labels = this.apiData.map(
          apiDataValue => {
            return apiDataValue[0];
          }
        );
        this.loaded = true;
      });
  }
};
</script>

<style>
</style>
