<script>
    export default {
        name: "SaveLoadSimple",

        data () {
            return {
                parsed_parameters: {},
            }
        },

        methods: {
            get_params(){
                return this.parsed_parameters;
            },
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

            parse_simple_pages() {
                console.log("Parsing Simple Pages")
                let select_data = this.$store.state.frontend_state["model_selection"];
                if (select_data ) { this.parsed_parameters["model_selection"] = this.parse_selection_page(select_data)}

                let central_services = this.$store.state.frontend_state["central_services"];
                if (central_services) { this.parsed_parameters["central_services"] = central_services }

                let tariffs_page = this.$store.state.frontend_state["model_tariffs"]
                if(tariffs_page){
                    this.parsed_parameters["tariffs"] = tariffs_page.tariffs;
                }

                // let solar_data = this.$store.state.frontend_state["model_solar"];
                // if (solar_data) { this.parsed_parameters["model_solar"] = solar_data }
            },

            parse_all_table_pages() {
                let f_data = this.$store.state.frontend_state["model_financing"];
                if (f_data) {
                    this.parsed_parameters["model_financing"] = this.parse_table_page(f_data)
                }

                let p_data = this.$store.state.frontend_state["model_participants"];
                if (p_data) {
                    this.parsed_parameters["model_participants"] = this.parse_table_page(p_data);
                    this.parsed_parameters["model_data_sources"] = this.parse_data_sources(p_data);
                }

                let t_data = this.$store.state.frontend_state["model_tariffs"];
                if (t_data) {
                    console.log("MODEL TARIFFS", t_data)
                    this.parsed_parameters["model_tariffs"] = this.parse_table_page(t_data)
                }
            },

            parse_table_page(data) {
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

                return parsed_data;
            },

            parse_data_sources(data) {
                let parsed_data = {
                    selected_solar_file: data["selected_solar_file"],
                    selected_load_file: data["selected_load_file"]
                };
                console.log(parsed_data);
                return parsed_data;
            },

            // Custom saver for this page due to additional dropdown logic
            parse_selection_page(data) {
                let parsed_data = [];
                parsed_data.push(data.model_dropdown);
                parsed_data.push(data.network_dropdown);

                console.log("Selection Page Data", parsed_data);
                return parsed_data;
            }

            // create_config_file(model_key) {
            //     let data = this.$store.state.frontend_state[model_key];
            //     console.log(data);
            //     let parsed_data = [];
            //
            //     for (let i = 0; i < data.table_rows.length; i++) {
            //         let row = this.table_rows[i].row_inputs;
            //         let row_data = {};
            //
            //         for (let j = 0; j < row.length; j++) {
            //             row_data[row[j].name] = row[j].value
            //         }
            //         data.push({
            //             row_id: i,
            //             row_inputs: row_data
            //         })
            //     }
            //
            //     return parsed_data
            // },
        },
    }
</script>