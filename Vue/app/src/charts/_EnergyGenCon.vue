<template>
    <LineChart
        class="chart"
        v-if="parsed_data"
        :chartData="parsed_data"
        :options="chart_options"
    />
</template>

<script>

    import LineChart from "./LineChart";

    export default {
        name: "EnergyGenCon",
        components: {LineChart},
        props: {
            chart_data: {},
        },

        data () {
            return {
                parsed_data: false,
                chart_options: {
                    maintainAspectRatio: false,
                    legend: {
                        position: 'right',
                        labels: {
                            fontColor: "white",
                            fontSize: 12,
                        }
                    },
                    title: {
                        fontSize: 20,
                        text: "Energy Generated & Consumed",
                        display: true,
                        fontColor: 'white'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                fontColor: "white",
                                fontSize: 18,
                                stepSize: 1,
                                beginAtZero: true
                            }
                        }],
                        xAxes: [{
                            ticks: {
                                fontColor: "white",
                                fontSize: 12,
                                stepSize: 1,
                                beginAtZero: true
                            }
                        }]
                    },
                },

                preset_colours: [
                    'rgb(0, 0, 0, 1)',
                    'rgb(50, 0, 0, 1)',
                    'rgb(100, 0, 0, 1)',
                    'rgb(150, 0, 0, 1)',
                    'rgb(200, 0, 0, 1)',
                    'rgb(250, 0, 0, 1)',
                    'rgb(0, 50, 0, 1)',
                    'rgb(0, 100, 0, 1)',
                    'rgb(0, 150, 0, 1)',
                    'rgb(0, 200, 0, 1)',
                    'rgb(0, 250, 0, 1)',
                    'rgb(0, 0, 50, 1)',
                    'rgb(0, 0, 100, 1)',
                    'rgb(0, 0, 150, 1)',
                    'rgb(0, 0, 200, 1)',
                    'rgb(0, 0, 250, 1)'
                ]
            }
        },

        methods: {
            parse_data() {
                let data = this.chart_data["energy_gencon"];

                let labels = data["timestamps"];
                let datasets = [];

                for (let key in data["data_points"]) {
                    let index = datasets.length;

                    let this_set = {
                        label: key,
                        data: data["data_points"][key],
                        fill: false,
                        borderColor: this.preset_colours[index],
                        borderWidth: 4,
                    };
                    datasets.push(this_set)
                }

                this.parsed_data = {
                    labels: labels,
                    datasets: datasets
                };
            },
        },

        mounted () {
            this.parse_data();
        },
    }
</script>

<style scoped>
    .chart {
        height: 100%;
        width: 100%;
    }
</style>