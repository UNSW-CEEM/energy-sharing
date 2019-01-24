<template>
    <div class="main-chart-container">
        <ChartBox
            v-if="data_ready"
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
                data_ready: false,

                chart_boxes: [
                    {
                        id: 0,
                        chart_key: "total_participant_bill",
                        chart_parsing_function: this.parse_participants_bill,
                        chart_props: {
                            col_s:1,
                            col_e:3,
                            row_s:1,
                            row_e:4,
                            chart_type: 'BarChart',
                            chart_heading: "Total Participants Bill",
                            chart_data: null,
                            chart_options: {
                                maintainAspectRatio: false,
                                legend: {
                                    labels: {
                                        fontColor: "white",
                                        fontSize: 10,
                                    }
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
                    {
                        id: 1,
                        chart_key: "energy_flows",
                        chart_parsing_function: this.parse_participants_bill,
                        chart_props: {
                            col_s:3,
                            col_e:5,
                            row_s:1,
                            row_e:4,
                            chart_type: 'BarChart',
                            chart_heading: "Twotal Participants Bill",
                            chart_data: null,
                            chart_options: {
                                maintainAspectRatio: false,
                                legend: {
                                    labels: {
                                        fontColor: "white",
                                        fontSize: 10,
                                    }
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
                ],
            }
        },

        methods: {
            get_chart_id(key) {
                for (let i = 0; i < this.chart_boxes.length; i++) {
                    if (this.chart_boxes[i].chart_key === key) {
                        return this.chart_boxes[i].id;
                    }
                }
                return false;
            },

            parse_participants_bill(data) {
                let labels = [];
                let data_points = [];

                for (let key in data) {
                   labels.push(key);
                   data_points.push(data[key])
                }

                let response = {

                    labels: labels,
                    datasets: [{
                        label: "Total Participant Bill",
                        backgroundColor:'#43B581',
                        responsive:true,
                        data: data_points,

                    }]
                };

                return response;
            },
        },

        async mounted() {

        },

        sockets: {
            chart_results_channel: function (response) {

                for (let key in response.data) {
                    console.log(key);
                    let chart_id = this.get_chart_id(key);
                    console.log(chart_id);
                    if (chart_id) {
                        let results_data = response.data[key];
                        let chart = this.chart_boxes[chart_id];

                        chart.chart_props.chart_data = chart.chart_parsing_function(results_data);
                    }
                }

                this.data_ready = true;
            }
        },
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