<template>
    <div class="chart-box" v-bind:style="position_styling">
        <h1 class="chart-heading">{{ chart_props.chart_heading }}</h1>
        <BarChart
            class="chart"
            v-if="chart_props.chart_type==='BarChart'"
            :chartData="chart_props.chart_data"
            :options="chart_props.chart_options"
        />
    </div>
</template>

<script>
    import BarChart from "./BarChart";
    import LineChart from "./LineChart";

    export default {
        name: "ChartBox",
        components: {LineChart, BarChart},
        props: {
            chart_props: {},
        },

        data () {
            return {
                position_styling: {
                    'grid-column-start': this.chart_props.col_s,
                    'grid-column-end': this.chart_props.col_e,
                    'grid-row-start': this.chart_props.row_s,
                    'grid-row-end': this.chart_props.row_e,
                },
            }
        }
    }
</script>

<style scoped>
    .chart-box {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
    }

    .chart-heading {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 10%;
    }

    .chart {
        display: flex;
        width: 100%;
        height: 90%;
    }


</style>