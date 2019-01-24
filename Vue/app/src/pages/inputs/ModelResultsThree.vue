<template>
    <div class="main-chart-container">
        <div class="sub-chart-container"
             v-for="chart in chart_boxes"
             :key="chart.id"
             :style="chart.position_styling"
        >
            <TPBChart
                v-if="chart.chart_type==='TPBChart' && chart_data"
                :chart_data="chart_data"
            />
        </div>
    </div>
</template>

<script>

    import TPBChart from "../../charts/TPBChart";

    export default {
        name: "ModelResultsThree",
        components: {TPBChart},

        data () {
            return  {
                chart_data: false,
                chart_boxes: [
                    {
                        id: 0,
                        chart_type: 'TPBChart',
                        position_styling: {
                            'grid-column-start': 1,
                            'grid-column-end': 3,
                            'grid-row-start': 1,
                            'grid-row-end': 4,
                        }
                    },
                    {
                        id: 1,
                        chart_type: 'TPBChart',
                        position_styling: {
                            'grid-column-start': 3,
                            'grid-column-end': 5,
                            'grid-row-start': 1,
                            'grid-row-end': 4,
                        }
                    }
                ],
            }
        },

        sockets: {
            chart_results_channel: function (response) {
                this.chart_data = response.data;
            }
        }
    }
</script>

<style scoped>

    .main-chart-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(3, 1fr);
        grid-column-gap: 20px;
        grid-row-gap: 20px;
    }

    .sub-chart-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

</style>