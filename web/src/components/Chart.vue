<script type="ts">
import { Line, mixins } from "vue-chartjs";

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ["chartData", "gymCode"],
  options: {
      maintainAspectRatio: true,
  },
  mounted() {
    this.renderChart(this.chartData, this.options );
  }
};
</script>

<style>
</style>
