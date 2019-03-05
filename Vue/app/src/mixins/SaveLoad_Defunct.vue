<script>
    export default {
        name: "SaveLoad",

        data () {
            return {

            }
        },

        methods: {
            save_page() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.table_rows
                };
                this.$store.commit('save_page', payload)
            },

            combine_table_data() {
                let data = [];

                for (let i = 0; i < this.table_rows.length; i++) {
                    let row = this.table_rows[i].row_inputs;
                    let row_data = {};

                    for (let j = 0; j < row.length; j++) {
                        row_data[row[j].name] = row[j].value
                    }
                    data.push({
                        row_id: i,
                        row_inputs: row_data
                    })
                }

                return data
            },

            save_page_server() {
                let data = [];

                for (let i = 0; i < this.table_rows.length; i++) {
                    let row = this.table_rows[i].row_inputs;
                    let row_data = [];

                    for (let j = 0; j < row.length; j++) {
                        row_data.push({
                            "name": row[j].name,
                            "value": row[j].value
                        })
                    }
                    data.push({
                        row_id: i,
                        row_inputs: row_data
                    })
                }

                let payload = {
                    model_page_name: this.model_page_name,
                    data: data,
                };
                this.$store.commit('save_server_page', payload)
            },

            load_config() {
                console.log("Loading config (for now from default_config.csv)");
                this.$socket.emit('load_config', this.model_page_name, this.selected_config_file)
            },

            save_config() {
                let table_data = this.combine_table_data();

                let payload = {
                    model_page_name: this.model_page_name,
                    data: table_data,
                };

                this.$socket.emit('save_config', this.model_page_name, this.selected_config_file, payload)
            },
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.table_rows = this.$store.state.frontend_state[this.model_page_name]
            } else {
                for (let i = 0; i< 1; i++) {
                    this.add_row()
                }
            }
        },

        beforeDestroy() {
            this.save_page();
            this.save_page_server();
        },
    }
</script>