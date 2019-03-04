<template>
    <div class="main-container">
        <h1>{{ view_name }}</h1>
        <table class="financing-table">
            <tr>
                <th
                    v-for="header in table_headers"
                    :key="header.header_id"
                    :value="header.name">{{ header.name }}</th>
            </tr>
            <tr>
                <td
                    v-for="header in table_headers"
                    :key="header.header_id">{{ header.additional_text }}</td>
            </tr>
            <tr
                v-for="row in table_rows"
                :key="row.row_id">
                <td v-for="input in row.row_inputs"
                :key="input.col_id"
                >
                    <!-- If a simple input use this component.-->
                    <SimpleNumberInput
                            v-if="input.tag==='my_number'"
                            v-model="input.value"
                            :my_placeholder="input.placeholder"/>
                    <!-- If a dropdown use this component.-->
                    <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                                    v-model="input.value"
                                    :my_options="my_options[input.dropdown_key]"
                                    :my_placeholder="input.placeholder"/>
                </td>
            </tr>
            <button @click="add_row()">Add Row</button>
        </table>

         <div class="file-buttons-container">
            <button @click="load_config()">Load from config file</button>
            <button @click="save_config()">Save to config file</button>
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
                is_connected: false,

                selected_config_file: 'default_config.csv',

                table_headers: [
                    {id: 0, name: "Component", additional_text:"Name"},
                    {id: 1, name: "CAPEX", additional_text:"$"},
                    {id: 2, name: "Who Pays", additional_text:"Who"},
                    {id: 3, name: "Discount Rate", additional_text:"%"},
                    {id: 4, name: "Amortization", additional_text:"years"},
                    {id: 5, name: "OPEX", additional_text:"$"},
                    
                ],

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
            }
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

        methods: {
            add_row(component = "", capex = "", capex_payer = "", discount_rate = "", amortization = "", opex = "") {
                let array_length = this.table_rows.length;
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

                this.table_rows.push(new_row);
            },
        },
        sockets: {
            financing_file_channel: function(response) {
                this.is_connected = true;
                this.table_rows = [];
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
    .file-buttons-container {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    view-title {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .financing-table{
        animation-name: fade-in;
        animation-duration: 2s;
    }

</style>