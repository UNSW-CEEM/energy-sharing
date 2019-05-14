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
        name: "CustomerBills",
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
                        text: "Customer Bill $",
                        display: true,
                        fontColor: 'white',
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                fontColor: "white",
                                fontSize: 18,
                                beginAtZero: true
                            }
                        }],
                        xAxes: [{
                            ticks: {
                                fontColor: "white",
                                fontSize: 12,
                                beginAtZero: true,
                                autoSkip: false,
                            }
                                  
                        }]
                    },

                    // Straight from chart.js docs/examples
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                var label = data.datasets[tooltipItem.datasetIndex].label || '';

                                if (label) {
                                    label += ': $';
                                }
                                label += Math.round(tooltipItem.yLabel * 100) / 100;
                                return label;
                            }
                        }
                    }
                },
            }
        },

        methods: {
            parse_data() {
                let data = this.chart_data["customer_totals"];
                // console.log(data);
                let labels = [];
                let data_points = [];

                for (let key in data) {
                   labels.push(key.replace("cust_total$_", ""));
                   data_points.push(data[key])
                }

                this.parsed_data = {
                    labels: labels,
                    datasets: [{
                        label: "Customer Bill $",
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