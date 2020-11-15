<script type="ts">
import { Line, mixins } from "vue-chartjs";
import chartjsPluginAnnotation from "chartjs-plugin-annotation";

const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["gymCode", "capacity"],
  mounted() {
    this.addPlugin(chartjsPluginAnnotation);

    this.renderChart(this.chartData, {
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
        annotations: [
          {
            drawTime: 'beforeDatasetsDraw',
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
              fontSize: 14,
            },
          },
        ],
      },
    });
  },
};
</script>