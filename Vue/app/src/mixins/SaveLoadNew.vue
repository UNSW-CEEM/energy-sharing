<script>
    export default {
        name: "SaveLoadSimple",

        data () {
            return {

            }
        },

        methods: {
            save_page_simple() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.input_data
                };

                this.$store.commit('save_page', payload)
            },

            load_page_simple() {
                if (this.model_page_name in this.$store.state.frontend_state) {
                    this.input_data = this.$store.state.frontend_state[this.model_page_name]
                }
            },

            combine_table_data() {

            },

            save_page_server() {

            },

            load_config() {

            },

            save_config() {

            },

        },

        created() {

        },

        beforeDestroy() {
            this.save_page_simple();
        },
    }
</script>