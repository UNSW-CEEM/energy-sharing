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

    // Line chart showing revenue at every half hour, for every participant

    export default {
        name: "RevParticipant",
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
                            fontSize: 10,
                        }
                    },
                    title: {
                        fontSize: 20,
                        text: "Participants Revenue",
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
                                fontSize: 10,
                                stepSize: 1,
                                beginAtZero: true
                            }
                        }]
                    },
                },
            }
        },

        methods: {
            parse_data() {
                let data = this.chart_data["revenue_participant"];
                console.log(data);
                console.log(data["timestamps"]);

                let labels = data["timestamps"];
                let datasets = [];

                for (let key in data["data_points"]) {

                    let this_set = {
                        label: key,
                        data: data["data_points"][key],
                        fill: false,
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