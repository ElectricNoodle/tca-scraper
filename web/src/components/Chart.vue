<script type="ts">
import { Line, mixins } from "vue-chartjs";
import chartjsPluginAnnotation from "chartjs-plugin-annotation";

const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["gymCode", "capacity", "options"],
  mounted() {
    this.addPlugin(chartjsPluginAnnotation);
    this.renderChart(this.chartData, this.options);
  },
  watch: {
    chartData() {
      this.renderChart(this.chartData, this.options);
    },
  },
};
</script>