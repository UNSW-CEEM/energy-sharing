<template>
    <div class="background">
        <div class="main-container" v-if="selected_model==='mike'">
            <h1>{{ view_name }}</h1>
            <table class="financing-table">
                <tr>
                    <th v-for="header in table_headers" :key="header.header_id" :value="header.name">
                        {{ header.name }}
                    </th>
                </tr>
                <tr>
                    <td v-for="header in table_headers" :key="header.header_id">
                        {{ header.additional_text }}
                    </td>
                </tr>
                <tr v-for="row in input_data.table_rows" :key="row.row_id">
                    <td v-for="input in row.row_inputs" :key="input.col_id">
                        <SimpleNumberInput
                                v-if="input.tag==='my_number'"
                                v-model="input.value"
                                :my_placeholder="input.placeholder"/>
                        <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                                        v-model="input.value"
                                        :my_options="input_data.my_options[input.dropdown_key]"
                                        :my_placeholder="input.placeholder"/>
                    </td>
                </tr>
            </table>
            <button @click="add_row()">Add Row</button>

             <div class="file-buttons-container">
                 <!--<button @click="load_config(input_data.selected_config_file)">Load User Config</button>-->
                 <!--<button @click="save_config()">Save User Config</button>-->
                 <button @click="load_config('default_config.csv')">Load Default</button>
            </div>
        </div>
        <div class="main-container" v-else>
            <h1>No Financing for Luomi Model Currently</h1>
        </div>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "Financing",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_financing",

                selected_model: false,

                input_data: {
                    selected_config_file: 'default_config.csv',

                    table_rows: [],

                    my_options: {
                        who_pays: {
                            option_one: "Retailer",
                            option_two: "TNSP",
                            option_three: "DNSP",
                            option_four: "Scheme Operator",
                            option_five: "Participants",
                        }
                    },
                },

                table_headers: [
                    {id: 0, name: "Component", additional_text:"Name"},
                    {id: 1, name: "CAPEX", additional_text:"$"},
                    {id: 2, name: "Who Pays", additional_text:"Who"},
                    {id: 3, name: "Discount Rate", additional_text:"%"},
                    {id: 4, name: "Amortization", additional_text:"years"},
                    {id: 5, name: "OPEX", additional_text:"$"},
                    
                ],
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            } else {
                for (let i = 0; i< 1; i++) {
                    this.add_row()
                }
            }
            this.selected_model = this.$store.state.frontend_state["selected_model"];
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            add_row(component = "", capex = "", capex_payer = "", discount_rate = "", amortization = "", opex = "") {
                let array_length = this.input_data.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            id: 0,
                            name: "component",
                            tag: "my_number",
                            value: component,
                            placeholder: "Name",
                        },
                        {
                            id: 1,
                            name: "capex",
                            tag: "my_number",
                            value: capex,
                            placeholder: "$",
                        },
                        {
                            id: 2,
                            name: "capex_payer",
                            tag: "my_dropdown",
                            value: capex_payer,
                            dropdown_key: "who_pays",
                            placeholder: "Select Payer",
                        },
                        {
                            id: 3,
                            name: "discount_rate",
                            tag: "my_number",
                            value: discount_rate,
                            placeholder: "%",
                        },
                        {
                            id: 4,
                            name: "amortization",
                            tag: "my_number",
                            value: amortization,
                            placeholder: "Years",
                        },
                        {
                            id: 5,
                            name: "opex",
                            tag: "my_number",
                            value: opex,
                            placeholder: "$",
                        },

                    ]
                };

                this.input_data.table_rows.push(new_row);
            },

            load_config(filename) {
                this.$socket.emit('load_config', this.model_page_name, filename)
            }
        },
        sockets: {
            financing_file_channel: function(response) {
                this.input_data.table_rows = [];
                for (let i = 0; i < response.length; i++) {
                    let params = response[i]["row_inputs"];
                    this.add_row(
                        params["component"],
                        params["capex"],
                        params["capex_payer"],
                        params["discount_rate"],
                        params["amortization"],
                        params["opex"],
                    );
                }
            }
        },
    }
</script>

<style scoped>
    .main-container {
        animation-name: fade-in;
        animation-duration: 1s;
        width: 100%;
        height: 100%;
    }
    .file-buttons-container {

    }

    view-title {

    }

    .financing-table{

    }

</style>