<template>
    <div class="graphs">
        <div class="graph-heading">
            <h1>{{ view_name }}</h1>
        </div>

        <div class="run-button" @click="run_model()">
            <span v-if="!results_received">Run Model</span>
            <span v-if="results_received">Run Model</span>
        </div>
    </div>
</template>

<script>
    import LineChart from '@/charts/LineChart.vue';
    import BarChart from '@/charts/BarChart.vue';

    export default {
        name: "Review",

        components: {
            LineChart,
            BarChart
        },

        data () {
            return {
                view_name: this.$options.name,
                results_received: false,

                chart_one_loaded: false,
                chart_one_data: null,
                chart_one_options: null,

                chart_two_loaded: false,
                chart_two_data: null,
                chart_two_options: {
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

        
        sockets: {
            sim_channel: function(response) {
                this.results_received = true;
                this.sim_result = response.data;
                this.chart_one_data = this.parse_energy_flows(this.sim_result["energy_flows"]);
                this.chart_two_data = this.parse_participants_bill(this.sim_result["total_participant_bill"]);
                this.chart_one_loaded = true;
                this.chart_two_loaded = true;
            }
        },
        methods: {
            run_model() {
                let params = this.$store.state.model_parameters;
                this.$socket.emit('run_model', params);
                console.log(params);
                this.$router.push('results');
            },

            parse_energy_flows(data) {
                console.log(data)
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
                console.log(labels, data_points);
                return response
            },
        },

        async mounted () {

        }
    }
</script>

<style scoped>
    .graphs {
        display: flex;
        flex-direction:column;
        justify-content:space-between;
        align-items:center;
        /*margin-top:2vh;*/
    }

    .graph-heading {
        grid-column-start: 1;
        grid-column-end: 3;
    }

    .graph{
        width:70vw !important;
    }

    /* .left-graph {
        background: aliceblue;
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 2;
    } */

    .run-button{
        background-color:rgba(114, 137, 218,1);
        cursor:pointer;
        color:black;
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 0 3vh 0;
        border-radius:3px;
    }

    .run-test-button{
        background-color:rgba(114, 137, 218,1);
        cursor:pointer;
        color:black;
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 0 3vh 0;
        border-radius:3px;
    }

    canvas{

        width:100% !important;
        max-height:50vh !important;

    }

    

    
</style>