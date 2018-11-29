<template>
    <div class="graphs">
        <div class="graph-heading">
            <h4>{{ view_name }}</h4>
            <button @click="run_model()" v-if="!results_received">Run Model</button>
            <button @click="run_model()" v-if="results_received">Rerun Model</button>
        </div>
        <div class="left-graph">
            <LineChart
                v-if="chart_one_loaded"
                :chartdata="chart_one_data"
                :options="chart_one_options"/>
        </div>
        <div class="right-graph">
            <BarChart
                v-if="chart_two_loaded"
                :chartdata="chart_two_data"
                :options="chart_two_options"/>
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
                chart_two_options: null,
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
                this.$socket.emit('run_model', params)
            },

            parse_energy_flows(data) {
                console.log(data)
            },

            parse_participants_bill(data) {
                console.log(data);
            },
        }
    }
</script>

<style scoped>
    .graphs {
        background: darkslategrey;
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 100px 400px;
    }

    .graph-heading {
        background: slateblue;
        grid-column-start: 1;
        grid-column-end: 3;
    }

    .left-graph {
        background: aliceblue;
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 2;
    }

    .right-graph {
        background: beige;
        grid-column-start: 2;
        grid-column-end: 3;
        grid-row-start: 2;
    }
</style>