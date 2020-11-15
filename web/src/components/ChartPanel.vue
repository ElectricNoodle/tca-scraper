<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">
        {{ gymName }} <small class="text-muted">{{ gymLocation }}</small>
      </h5>
      <p class="card-text">
        <font-awesome-icon icon="clock" />
        {{ this.getOpeningTimeText }} to {{ this.getClosingTimeText }}
        <font-awesome-icon icon="user" /> {{ this.capacity }}
      </p>
      <Chart
        v-if="loaded"
        :gymCode="gymCode"
        :capacity="capacity"
        :chart-data="graphData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script type="ts">
import Vue from "vue";
import Component from "vue-class-component";
import Chart from "./Chart.vue";
import { mapGetters } from "vuex";

import { library } from "@fortawesome/fontawesome-svg-core";
import { faClock, faUser } from "@fortawesome/free-solid-svg-icons";
library.add(faClock);
library.add(faUser);

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const axios = require("axios").default;
import {
  format,
  yesterday,
  today,
  startOfToday,
  endOfToday,
  formatISO,
  parseISO,
  addHours,
  getDay,
  getMonth,
  getYear,
  isWeekend,
} from "date-fns";

export default {
  components: {
    Chart,
    FontAwesomeIcon,
  },
  data() {
    return {
      baseApiUrl: this.$store.state.baseApiUrl,
      loaded: false,
      gymName: this.$store.state.gymData[this.gymCode].name,
      gymLocation: this.$store.state.gymData[this.gymCode].location,
      apiData: null,
      capacity: 0,
      options: {
        format: "DD/MM/YYYY",
        useCurrent: false,
      },
      graphData: {
        labels: [],
        datasets: [{}],
      },
    };
  },
  computed: {
    chartOptions: function () {
      return {
        scales: {
          yAxes: [
            {
              ticks: {
                suggestedMax: this.capacity + 5,
              },
            },
          ],
        },
        annotation: {
          drawTime: "beforeDatasetsDraw",
          annotations: [
            {
              display: true,
              type: "line",
              mode: "horizontal",
              scaleID: "y-axis-0",
              borderColor: "#e63946",
              value: this.capacity,
              borderDash: [4, 4],
              label: {
                content: this.capacity,
                enabled: true,
                position: "top",
                xAdjust: 15,
                backgroundColor: "#e63946",
                fontSize: 12,
              },
            },
          ],
        },
      };
    },
    getOpenTime: function () {
      return isWeekend(this.getSelectedDate)
        ? this.$store.state.gymData[this.gymCode].times.weekend.open
        : this.$store.state.gymData[this.gymCode].times.weekday.open;
    },
    getCloseTime: function () {
      return isWeekend(this.getSelectedDate)
        ? this.$store.state.gymData[this.gymCode].times.weekend.close
        : this.$store.state.gymData[this.gymCode].times.weekday.close;
    },
    getSelectedDate: function () {
      return this.$store.getters.getDate;
    },
    getOpeningDateISO: function () {
      return formatISO(addHours(this.getSelectedDate, this.getOpenTime));
    },
    getClosingDateISO: function () {
      return formatISO(addHours(this.getSelectedDate, this.getCloseTime));
    },
    getOpeningTimeText: function () {
      return format(addHours(this.getSelectedDate, this.getOpenTime), "p");
    },
    getClosingTimeText: function () {
      return format(addHours(this.getSelectedDate, this.getCloseTime), "p");
    },
  },
  props: ["gymCode", "backgroundColor"],
  watch: {
    getSelectedDate: function (val) {
      this.getData();
    },
  },
  methods: {
    getData: function () {
      axios
        .get(this.baseApiUrl + this.gymCode, {
          params: { from: this.getOpeningDateISO, to: this.getClosingDateISO },
        })
        .then((response) => {
          if (response.data.occupancy != 0) {
            this.capacity = response.data.capacity;
            this.apiData = response.data.occupancy;

            this.graphData = {
              datasets: [
                {
                  backgroundColor: this.backgroundColor,
                  label: "Occupancy",
                  data: this.apiData.map((apiDataValue) => {
                    if (apiDataValue[1] !== null) {
                      return apiDataValue[1];
                    }
                    return 0;
                  }),
                },
              ],
              labels: this.apiData.map((apiDataValue) => {
                return format(parseISO(apiDataValue[0]), "p");
              }),
            };
          } else {
            this.graphData = {
              datasets: [
                {
                  backgroundColor: this.backgroundColor,
                  label: "Occupancy",
                  data: [],
                },
              ],
              labels: [],
            };
          }

          this.loaded = true;
        });
    },
  },
  mounted() {
    this.getData();
  },
};
</script>

<style></style>
