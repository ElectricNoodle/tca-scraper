import Vue from "vue";
import App from "./App.vue";
import Vuex from "vuex";

import {
  startOfToday,
} from "date-fns";

Vue.config.productionTip = false;

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    baseApiUrl: process.env.VUE_APP_API_URL,
    date: startOfToday(),
    gymData: {
      GLA: {
        name: "The Newsroom",
        location: "Glasgow",
        open: 7,
        close: 22
      },
      PST: {
        name: "The Prop Store",
        location: "Glasgow",
        open: 12,
        close: 22
      },
      BRI: {
        name: "The Mothership",
        location: "Bristol",
        open: 7,
        close: 22
      },
      UNC: {
        name: "The Church",
        location: "Bristol",
        open: 12,
        close: 22
      }
    }
  },
  getters: {
    getDate : state => {
      return state.date
    }
  },
  mutations: {
    SET_DATE (state, date) {
      state.date = date
    }
  }
});

new Vue({
  render: h => h(App),
  store: store
}).$mount("#app");
