<template>
    <div class="graphs">
        <div class="graph-heading">
            <h1>{{ view_name }}</h1>
        </div>

        <div class="run-button" @click="run_model()">
            <span v-if="!results_received">Run Model</span>
            <span v-if="results_received">Rerun Model</span>
        </div>
    </div>
</template>

<script>

    export default {
        name: "Review",

        components: {

        },

        data () {
            return {
                view_name: this.$options.name,
                results_received: false,
            }
        },

        
        sockets: {

        },
        methods: {
            run_model() {
                let params = this.$store.state.model_parameters;
                this.$socket.emit('run_model', params);
                // console.log(params);
                this.$router.push('results');
            },
        }
    }
</script>

<style scoped>

    .graphs {
        display: flex;
        flex-direction:column;
        justify-content:space-between;
        align-items:center;
    }

    .graph-heading {
        grid-column-start: 1;
        grid-column-end: 3;
    }

    .run-button{
        background-color:rgba(114, 137, 218,1);
        cursor:pointer;
        color:black;
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 0 3vh 0;
        border-radius:3px;
    }

</style>