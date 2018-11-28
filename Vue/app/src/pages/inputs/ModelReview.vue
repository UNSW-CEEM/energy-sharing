<template>
    <div class="graphs">
        <div class="graph-heading">
            <h4>{{ view_name }}</h4>
            <button @click="run_model()" v-if="!results_received">Run Model</button>
            <button @click="run_model()" v-if="results_received">Rerun Model</button>
        </div>
        <div class="left-graph">
            <h4>Left Graph</h4>
            <p>{{ raw_energy_flows }}</p>
        </div>
        <div class="right-graph">
            <h4>Right Graph</h4>
            <p>{{ raw_parti_bill}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Review",
        data () {
            return {
                view_name: this.$options.name,
                isConnected: false,
                raw_energy_flows: "No energy Data Yet",
                raw_parti_bill: "No Participant Data Yet",
                results_received: false,
            }
        },
        sockets: {
            sim_channel: function(response) {
                this.isConnected = true;
                this.results_received = true;
                this.sim_result = response.data;
                this.raw_energy_flows = this.sim_result["energy_flows"];
                this.raw_parti_bill = this.sim_result["total_participant_bill"];
                console.log(this.sim_result);
            }
        },
        methods: {
            sendSavedState() {
                var this_data = this.$store.state.model_parameters;
                console.log("Sending some json: ", this_data);
                this.isConnected = true;
                this.$socket.emit('exampleJSON', this_data);
            },

            run_model() {
                let params = this.$store.state.model_parameters;
                this.$socket.emit('run_model', params)
            }
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