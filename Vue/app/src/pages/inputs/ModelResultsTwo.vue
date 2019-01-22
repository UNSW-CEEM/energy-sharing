<template>
    <div class="main-chart-container">
        <ChartBox
            v-for="chart in chart_boxes"
            :key="chart.id"
            :chart_props="chart.chart_props"
        />
    </div>
</template>

<script>
    import ChartBox from "../../charts/ChartBox";

    export default {
        name: "ModelResultsTwo",
        components: {ChartBox},

        data () {
            return {
                chart_boxes: [
                    {
                        id: 0,
                        chart_props: {
                            col_s:1,
                            col_e:3,
                            row_s:1,
                            row_e:4,
                            chart_type: 'BarChart',
                            chart_heading: "Chart Heading One",
                            chart_data: {
                                datasets: [
                                    {
                                        backgroundColor: ['#F87979', '#BEBEBE'],
                                        data: [68, 32]
                                    },
                                ]
                            },

                            chart_options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                cutoutPercentage: 90,
                                tooltips: {
                                    enabled: false
                                }
                            },
                        }
                    },
                    {
                        id: 0,
                        chart_props: {
                            col_s:3,
                            col_e:5,
                            row_s:1,
                            row_e:4,
                            chart_type: 'BarChart',
                            chart_heading: "Chart Heading Two",
                            chart_data: {
                                datasets: [
                                    {
                                        backgroundColor: ['#F87979', '#BEBEBE'],
                                        data: [68, 32]
                                    },
                                ]
                            },

                            chart_options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                cutoutPercentage: 90,
                                tooltips: {
                                    enabled: false
                                }
                            },
                        }
                    }
                ],
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
</style>