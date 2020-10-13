<template>
  <div style="margin-bottom:30px;">
    <strong>{{ gymName }}</strong>&nbsp;-&nbsp;<em>{{ gymLocation }}</em>
    <p>
      Open from {{ this.getOpeningTimeText }} to {{ this.getClosingTimeText }}
    </p>
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
  formatISO,
  addHours
} from "date-fns";

export default {
  components: {
    Chart
  },
  data() {
    return {
      baseApiUrl: this.$store.state.baseApiUrl,
      loaded: false,
      gymName: this.$store.state.gymData[this.gymCode].name,
      gymLocation: this.$store.state.gymData[this.gymCode].location,
      openTime: this.$store.state.gymData[this.gymCode].open,
      closeTime: this.$store.state.gymData[this.gymCode].close,
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
                type: "string"
              }
            ]
          }
        }
      }
    };
  },
  computed: {
    getOpeningDateISO: function() {
      return formatISO(addHours(startOfToday(), this.openTime));
    },
    getClosingDateISO: function() {
      return formatISO(addHours(startOfToday(), this.closeTime));
    },
    getOpeningTimeText: function() {
      return format(addHours(startOfToday(), this.openTime), "p");
    },
    getClosingTimeText: function() {
      return format(addHours(startOfToday(), this.closeTime), "p");
    }
  },
  props: ["gymCode", "backgroundColor"],
  mounted() {
    this.loaded = false;

    axios
      .get(this.baseApiUrl + this.gymCode, {
        params: { from: this.getOpeningDateISO, to: this.getClosingDateISO }
      })
      .then(response => {
        this.apiData = response.data.series[0].values;
        this.graphData.datasets[0].data = this.apiData.map(apiDataValue => {
          if (apiDataValue[1] !== null) {
            return apiDataValue[1];
          }
          return 0;
        });
        this.graphData.labels = this.apiData.map(apiDataValue => {
          return apiDataValue[0];
        });
        this.loaded = true;
      });
  }
};
</script>

<style>
</style>
