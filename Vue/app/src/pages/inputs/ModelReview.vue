<template>
    <div class="background">
        <div class="main-container">
            <div class="model-title">
                <h1>{{ view_name }}</h1>
            </div>

            <div class="run-button" @click="run_model()">
                <span v-if="!results_received">Run Model</span>
                <span v-if="results_received">Run Model</span>
            </div>
        </div>
    </div>
</template>

<script>
    import SaveLoad from '@/mixins/SaveLoadNew.vue';

    export default {
        name: "Review",
        mixins: [SaveLoad],

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
                this.$router.push('results');

                this.send_to_model()
            },
        }
    }
</script>

<style scoped>

    .main-container {
        display: flex;
        flex-direction:column;
        justify-content:space-between;
        align-items: center;
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .model-title {

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