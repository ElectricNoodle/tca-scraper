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
        times: {
          weekday: {
            open: 7,
            close: 22
          },
          weekend: {
            open: 8,
            close: 20
          }
        }
      },
      PST: {
        name: "The Prop Store",
        location: "Glasgow",
        times: {
          weekday: {
            open: 10,
            close: 22
          },
          weekend: {
            open: 9,
            close: 20
          }
        }
      },
      BRI: {
        name: "The Mothership",
        location: "Bristol",
        times: {
          weekday: {
            open: 7,
            close: 22
          },
          weekend: {
            open: 8,
            close: 20
          }
        }
      },
      UNC: {
        name: "The Church",
        location: "Bristol",
        times: {
          weekday: {
            open: 12,
            close: 22
          },
          weekend: {
            open: 9,
            close: 20
          }
        }
      }
    }
  },
  getters: {
    getDate: state => {
      return state.date
    }
  },
  mutations: {
    SET_DATE(state, date) {
      state.date = date
    }
  }
});

new Vue({
  render: h => h(App),
  store: store
}).$mount("#app");
