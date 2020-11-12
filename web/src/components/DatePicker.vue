<template>
  <datepicker
    :v-model="selectedDate"
    name="datePicker"
    @input="setDate"
    maximum-view="month"
    minimum-view="day"
    :placeholder="placeholder"
    format="yyyy-MM-dd"
  ></datepicker>
</template>

<script type="ts">
import Component from "vue-class-component";
import Datepicker from "vuejs-datepicker";

import {
  format,
  startOfToday,
} from "date-fns";

import { set } from "date-fns";

export default {
  components: {
    Datepicker
  },
  data() {
      return {
          placeholder: format(startOfToday(), 'yyyy-MM-dd')
      }
  },
  computed: {
    selectedDate: function() {
      return this.$store.getters.getDate;
    }
  },
  methods: {
    setDate(date) {
      date = set(date, { hours: 0, minutes: 0, seconds: 0 });
      this.$store.commit("SET_DATE", date);
    }
  }
};
</script>

<style></style>