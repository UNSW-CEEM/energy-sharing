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

                parsed_parameters: {},
            }
        },

        sockets: {

        },

        methods: {
            run_model() {
                this.parse_tables();

                this.$socket.emit('run_model', this.parsed_parameters);
                this.$router.push('results');
            },

            parse_tables() {
                let f_data = this.$store.state.frontend_state["model_financing"];
                if (f_data) { this.parse_table_page(f_data, "model_financing") }

                let p_data = this.$store.state.frontend_state["model_participants"];
                if (p_data) { this.parse_table_page(p_data, "model_participants") }

                let t_data = this.$store.state.frontend_state["model_tariffs"];
                if (t_data) { this.parse_table_page(t_data, "model_tariffs") }
            },

            parse_table_page(data, model_page_name) {
                // console.log("Participants Params: ", data);

                let parsed_data = [];

                for (let i = 0; i < data.table_rows.length; i++) {
                    let row = data.table_rows[i].row_inputs;
                    let row_data = [];

                    for (let j = 0; j < row.length; j++) {
                        row_data.push({
                            "name": row[j].name,
                            "value": row[j].value
                        })
                    }
                    parsed_data.push({
                        row_id: i,
                        row_inputs: row_data
                    })
                }

                this.parsed_parameters[model_page_name] = parsed_data;
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