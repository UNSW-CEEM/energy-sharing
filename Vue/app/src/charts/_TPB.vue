<template>
    <BarChart
        class="chart"
        v-if="parsed_data"
        :chartData="parsed_data"
        :options="chart_options"
    />
</template>

<script>

    import BarChart from "./BarChart";

    export default {
        name: "TPBChart",
        components: {BarChart},
        props: {
            chart_data: {},
        },

        data () {
            return {
                parsed_data: false,
                chart_options: {
                    maintainAspectRatio: false,
                    legend: {
                        display: false,
                        labels: {
                            fontColor: "white",
                            fontSize: 10,
                        }
                    },
                    title: {
                        fontSize: 20,
                        text: "Total Participants Bill",
                        display: true,
                        fontColor: 'white',
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
                let data = this.chart_data["total_participant_bill"];
                console.log(data);
                let labels = [];
                let data_points = [];

                for (let key in data) {
                   labels.push(key);
                   data_points.push(data[key])
                }

                this.parsed_data = {
                    labels: labels,
                    datasets: [{
                        label: "Total Participant Bill",
                        backgroundColor:'#43B581',
                        responsive:true,
                        data: data_points,

                    }]
                };
            }
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