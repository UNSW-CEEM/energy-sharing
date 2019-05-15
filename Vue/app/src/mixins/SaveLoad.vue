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
                this.parse_simple_pages();
                this.parse_all_table_pages();
                this.parse_mike_tariffs();
                this.parse_mike_config_options();
                
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

            parse_mike_config_options(){
                var options = {
                    'scenario': 1,
                    'arrangement':'en_pv',
                    'pv_cap_id': 'W_max_yield',
                    'pv_capex_scaleable':false,
                    'en_capex_id':'capex_med',
                    'a_term':20,
                    'a_rate':0.06,
                    'pv_scaleable':false,
                    'pv_kW_peak':'',
                    'notes':'',
                    'tariffs':{
                        'cp':'TIDNULL',
                        // 'all_residents':'STC_20',
                        'parent': 'EA305_TOU12',
                        'network_tariff':'EA305',
                    },
                    'common_property_load_profile':null,
                    'common_property_solar_profile':null,
                    'central_solar_profile':null,
                }

                let select_data = this.$store.state.frontend_state["model_participants_mike"];
                if(select_data){
                    options['arrangement'] = select_data['selected_arrangement'];
                    options['common_property_load_profile'] = select_data['central_load_profile'];
                    options['common_property_solar_profile'] = select_data['common_property_solar_profile'];
                    options['central_solar_profile'] = select_data['central_solar_profile'];
                }

                select_data = this.$store.state.frontend_state["battery_mike"];
                if(select_data){
                    if(select_data['central_battery_type'] && select_data['central_dispatch_strategy']){
                        options['central_battery_id'] = select_data['central_battery_type']
                        options['central_battery_strategy'] = select_data['central_dispatch_strategy']
                    }
                    for(var participant in select_data['participant_batteries']){
                        var pbd = select_data['participant_batteries'][participant];
                        if(pbd.capacity_kWh && pbd.type && pbd.dispatch_strategy ){
                            options[participant+'_battery_id'] = pbd.type;
                            options[participant+'_battery_strategy'] = pbd.dispatch_strategy;
                            options[participant+'_battery_capacity_kWh'] = Number(pbd.capacity_kWh)
                        }
                    }
                }

                this.parsed_parameters["study_parameters_mike"] = options;
            },
            


            parse_mike_tariffs(){
                let select_data = this.$store.state.frontend_state["model_tariffs_mike"];
                console.log("SaveLoad.vue/parse_mike_tariffs()", select_data)
                let output = {
                    name:'user_interface',
                    daily_fixed_rate: 1,
                    static_imports:[],
                    static_solar_imports:[],
                    static_exports:[],
                }
                
                if(select_data){
                    for(var i = 0; i< select_data.tariffs.static_imports.period_rates.length; i++){
                        output.static_imports.push({
                            start_hr: i==0 ? 0: select_data.tariffs.static_imports.tou_times[i-1],
                            end_hr: i== select_data.tariffs.static_imports.tou_times.length? 24: select_data.tariffs.static_imports.tou_times[i],
                            price: select_data.tariffs.static_imports.period_rates[i]
                        })
                    }

                    for(var i = 0; i< select_data.tariffs.static_solar_imports.period_rates.length; i++){
                        output.static_solar_imports.push({
                            start_hr: i==0 ? 0: select_data.tariffs.static_solar_imports.tou_times[i-1],
                            end_hr: i==select_data.tariffs.static_solar_imports.tou_times.length? 24: select_data.tariffs.static_solar_imports.tou_times[i],
                            price: select_data.tariffs.static_solar_imports.period_rates[i]
                        })
                    }

                    for(var i = 0; i< select_data.tariffs.static_exports.period_rates.length; i++){
                        output.static_exports.push({
                            start_hr: i==0 ? 0: select_data.tariffs.static_exports.tou_times[i-1],
                            end_hr: i==select_data.tariffs.static_exports.tou_times.length ? 24 : select_data.tariffs.static_exports.tou_times[i],
                            price: select_data.tariffs.static_exports.period_rates[i]
                        })
                    }
                }

                // output = 
                //     {
                //         'name':'user_interface',
                //         'daily_fixed_rate': 1,
                //         'static_imports':[
                //             {
                //                 'start_hr':7,
                //                 'end_hr':10,
                //                 'price':0.3
                //             },
                //             {
                //                 'start_hr':10,
                //                 'end_hr':15,
                //                 'price':0.5
                //             },
                //             {
                //                 'start_hr':15,
                //                 'end_hr':18,
                //                 'price':0.3
                //             },
                //         ],
                //         'static_solar_imports':[],
                //         'static_exports':[]
                //     }
                

                
                this.parsed_parameters["model_tariffs_mike"] = [output]; //put it in an array - can theoretically have more than one config (ie one per participant - but we will leave for now. )
            },

            parse_simple_pages() {
                console.log("Parsing Simple Pages")
                let select_data = this.$store.state.frontend_state["model_selection"];
                if (select_data ) { 
                    // this.parsed_parameters["model_selection"] = this.parse_selection_page(select_data)
                    this.parsed_parameters["model_selection"] = {
                        model_type: select_data.selected_model,
                        network_type:null,
                    }
                }

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

                let pm_data = this.$store.state.frontend_state["model_participants_mike"];
                if (pm_data) {
                    this.parsed_parameters["model_participants_mike"] = this.parse_table_page(pm_data);
                    this.parsed_parameters["model_data_sources_mike"] = this.parse_data_sources(pm_data);
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