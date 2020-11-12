<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">
        {{ gymName }} <small class="text-muted">{{ gymLocation }}</small>
      </h5>
      <p class="card-text">
        Open from {{ this.getOpeningTimeText }} to {{ this.getClosingTimeText }}
      </p>
      <Chart :gymCode="gymCode" :chart-data="graphData" />
    </div>
  </div>
</template>

<script type="ts">
import Vue from "vue";
import Component from "vue-class-component";
import Chart from "./Chart.vue";
import { mapGetters } from "vuex";

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
  getYear
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

      options: {
        format: "DD/MM/YYYY",
        useCurrent: false
      },
      graphData: {
        labels: [],
        datasets: [{}]
      }
    };
  },
  computed: {
    getSelectedDate: function() {
      return this.$store.getters.getDate;
    },
    getOpeningDateISO: function() {
      return formatISO(addHours(this.getSelectedDate, this.openTime));
    },
    getClosingDateISO: function() {
      return formatISO(addHours(this.getSelectedDate, this.closeTime));
    },
    getOpeningTimeText: function() {
      return format(addHours(this.getSelectedDate, this.openTime), "p");
    },
    getClosingTimeText: function() {
      return format(addHours(this.getSelectedDate, this.closeTime), "p");
    }
  },
  props: ["gymCode", "backgroundColor"],
  watch: {
    getSelectedDate: function(val) {
      this.getData();
    }
  },
  methods: {
    getData: function() {
      axios
        .get(this.baseApiUrl + this.gymCode, {
          params: { from: this.getOpeningDateISO, to: this.getClosingDateISO }
        })
        .then(response => {
          if (response.data.series.length != 0) {
            this.apiData = response.data.series[0].values;

            this.graphData = {
              datasets: [
                {
                  backgroundColor: this.backgroundColor,
                  label: "Occupancy",
                  data: 
                    this.apiData.map(apiDataValue => {
                      if (apiDataValue[1] !== null) {
                        return apiDataValue[1];
                      }
                      return 0;
                    })
                  
                }
              ],
              labels: this.apiData.map(apiDataValue => {
                return format(parseISO(apiDataValue[0]), "p");
              })
            };
          } else {
            this.graphData = {
              datasets: [
                {
                  backgroundColor: this.backgroundColor,
                  label: "Occupancy",
                  data: []                  
                }
              ],
              labels: []
            };
          }
        });
    }
  },
  mounted() {
    this.getData();
  }
};
</script>

<style></style>
