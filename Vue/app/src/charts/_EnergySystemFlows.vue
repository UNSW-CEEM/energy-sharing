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

    // Line chart showing revenue at every half hour, for every participant

    export default {
        name: "EnergySystemFlows",
        components: {LineChart, Chart},
        props: {
            chart_data: {},
        },

        computed:{
            
            highchartsOptions () {
                let data = this.chart_data["energy_flows"];

                var central_battery_export = [];
                var gross_participant_central_battery_import = [];
                var gross_participant_grid_import = [];
                var gross_participant_local_solar_import = [];
                var net_network_export = [];
                var net_participant_export = [];
                var unallocated_battery_load = [];
                var unallocated_local_solar = [];

                
                for(var i =0; i< data.length; i++){
                    // var time = moment(data[""]).unix() * 1000.0;
                    var time = i;
                    central_battery_export.push([time, Number(data[i].central_battery_export)]);
                    gross_participant_central_battery_import.push([time, Number(data[i].gross_participant_central_battery_import)]);
                    gross_participant_grid_import.push([time, Number(data[i].gross_participant_grid_import)]);
                    gross_participant_local_solar_import.push([time, Number(data[i].gross_participant_local_solar_import)]);
                    net_network_export.push([time, Number(data[i].net_network_export)]);
                    net_participant_export.push([time, Number(data[i].net_participant_export)]);
                    unallocated_battery_load.push([time, Number(data[i].unallocated_battery_load)])
                    unallocated_local_solar.push([time, Number(data[i].unallocated_local_solar)])

                }

               
                
                return {
                    chart: {
                    zoomType: 'x'
                    },
                    title: {
                    text: 'Participant Energy Generation / Consumption'
                    },
                    width: null,

                    subtitle: {
                    text: document.ontouchstart === undefined
                        ? 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    yAxis: {
                    title: {
                        text: 'kWh'
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
                            name: 'Central Battery Export',
                            data:central_battery_export,
                        },
                        {
                            name: 'Gross Participant Central Battery Import',
                            data:gross_participant_central_battery_import,
                        },
                        {
                            name: 'Gross Participant Grid Import',
                            data:gross_participant_grid_import,
                        },
                        {
                            name: 'Gross Participant Local Solar Import',
                            data:gross_participant_local_solar_import,
                        },
                        {
                            name: 'Net Network Export',
                            data:net_network_export,
                        },
                        {
                            name: 'Net Participant Export',
                            data:net_participant_export,
                        },
                        {
                            name: 'Unallocated Battery Load',
                            data:unallocated_battery_load,
                        },
                        {
                            name: 'Unallocated Local Solar',
                            data:unallocated_local_solar,
                        },
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
                        text: "System Energy Flows",
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
                let data = this.chart_data["revenue_participant"];

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