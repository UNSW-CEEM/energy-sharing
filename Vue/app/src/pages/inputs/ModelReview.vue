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
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "Review",
        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                results_received: false,

                parsed_parameters: {},
            }
        },

        sockets: {

        },

        methods: {
            run_model() {
                this.parse_simple_pages();
                this.parse_all_table_pages();

                this.$socket.emit('run_model', this.parsed_parameters);
                this.$router.push('results');
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
        animation-duration: 1s;
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