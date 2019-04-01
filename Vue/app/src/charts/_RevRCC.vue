<template>
    <!-- <LineChart
        class="chart"
        v-if="parsed_data"
        :chartData="parsed_data"
        :options="chart_options"
    /> -->
    <Chart class="mychart" :options="highchartsOptions"></Chart>

    
</template>

<script>
    import LineChart from "./LineChart";
    import {Chart} from 'highcharts-vue'
    import moment from 'moment'

    // Line chart showing revenue at every half hour, for retailer, central battery, central solar

    export default {
        name: "RevRCC",
        components: {LineChart, Chart},
        props: {
            chart_data: {},
        },

        computed:{
            
            highchartsOptions () {
                let data = this.chart_data["revenue_retailer"];
                var total_revenue = [];
                var central_battery_import = [];
                var grid_import_fixed = [];
                var grid_import_variable = [];
                var local_solar_import = [];

                for(var i = 0; i< data.data_points.total_revenue.length; i++){
                    var timestamp = moment(data.timestamps[i]).unix()*1000.0;
                    
                    total_revenue.push([timestamp, Number(data.data_points.total_revenue[i])]);
                    central_battery_import.push([timestamp, Number(data.data_points.central_battery_import_revenue[i])]);
                    grid_import_fixed.push([timestamp, Number(data.data_points.grid_import_revenue_fixed[i])]);
                    grid_import_variable.push([timestamp, Number(data.data_points.grid_import_revenue_variable[i])]);
                    local_solar_import.push([timestamp, Number(data.data_points.local_solar_import_revenue[i])]);
                }
                
                return {
                    chart: {
                    zoomType: 'x'
                    },
                    title: {
                    text: 'Solar and Load'
                    },
                    width: null,

                    subtitle: {
                    text: document.ontouchstart === undefined
                        ? 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    yAxis: {
                    title: {
                        text: '$'
                    }
                    },
                    legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                    },
                    xAxis: {
                    type: 'datetime'
                    },
                    series: [
                        {
                            name: 'Total Revenue',
                            data:total_revenue,
                        },
                        {
                            name: 'Variable Grid Import',
                            data:grid_import_variable,
                        },
                        {
                            name: 'Fixed Grid Import',
                            data:grid_import_fixed,
                        },
                        {
                            name: 'Central Battery Import',
                            data:central_battery_import,
                        },
                        {
                            name: 'Local Solar',
                            data:local_solar_import,
                        },
                        // {
                        //     name: 'Load',
                        //     data: [1,2,3,4],
                        // },

                    ]
                }
            },
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
                        text: "Retailer Revenue",
                        display: true,
                        fontColor: 'white'
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
                
                let data = this.chart_data["revenue_retailer"];
                console.log(data)

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

    .mychart{
        width:100%;
        
    }
</style>