<template>
    <div>
        <h1>{{ view_name }}</h1>
        <table>
            <tr>
                <th
                    v-for="header in table_headers"
                    :key="header.header_id"
                    :value="header.name">{{ header.name }}</th>
            </tr>
            <tr>
                <td v-for="header in table_headers" :key="header.header_id">
                    {{ header.additional_text }}
                </td>
            </tr>
            <tr v-for="row in table_rows" :key="row.row_id">
                <td v-for="input in row.row_inputs" :key="input.col_id">

                    <SimpleNumberInput
                            v-if="input.tag==='my_number'"
                            v-model="input.value"
                            :my_placeholder="input.placeholder"/>

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
        name: "Tariffs",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_tariffs",

                selected_config_file: 'default_config.csv',

                table_headers: [
                    {header_id: 0, name: "Tariff Type", additional_text:"Select"},
                    {header_id: 1, name: "Tariff Name", additional_text:"Label"},
                    {header_id: 2, name: "Solar FiT", additional_text:"$/kWh"},
                    {header_id: 3, name: "Peak", additional_text:"$/kWh"},
                    {header_id: 4, name: "Shoulder", additional_text:"$/kWh"},
                    {header_id: 5, name: "Off-Peak", additional_text:"$/kWh"},
                ],

                table_rows: [],

                my_options:{
                     tariff_type_options: [
                        "Retail",
                        "TUOS",
                        "DUOS",
                        "NUOS",
                    ],
                }
            }
        },

        computed: {

        },

        methods: {
            add_row(tariff_type="", tariff_name="", fit_input="", peak_price="", shoulder_price="", off_peak_price="") {

                let array_length = this.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            col_id: 0,
                            field_name:"Tariff Type",
                            tag:"my_dropdown",
                            dropdown_key: "tariff_type_options",
                            value: tariff_type,
                            placeholder:"Select Tariff Type",
                        },
                        {
                            col_id: 1,
                            field_name:"tariff_name",
                            tag:"my_number",
                            value: tariff_name,
                            placeholder:"Name",
                        },
                        {
                            col_id: 2,
                            field_name:"fit_input",
                            tag:"my_number",
                            value: fit_input,
                            placeholder:"$"
                        },
                        {
                            col_id: 3,
                            field_name:"peak_price",
                            tag:"my_number",
                            value: peak_price,
                            placeholder:"$",
                        },
                        {
                            col_id: 4,
                            field_name:"shoulder_price",
                            tag:"my_number",
                            value: shoulder_price,
                            placeholder:"$",
                        },
                        {
                            col_id: 5,
                            field_name:"off_peak_price",
                            tag:"my_number",
                            value: off_peak_price,
                            placeholder:"$",
                        },
                    ]
                };

                this.table_rows.push(new_row);
            },
        },

        sockets: {
            tariffs_file_channel: function(response) {
                this.is_connected = true;
                this.table_rows = [];
                for (let i = 0; i < response.length; i++) {
                    let params = response[i]["row_inputs"];
                    this.add_row(
                        params["tariff_type"],
                        params["tariff_name"],
                        params["fit_input"],
                        params["peak_price"],
                        params["shoulder_price"],
                        params["off_peak_price"],
                    );
                }
            }
        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
    }

    .file-buttons-container {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    h1 {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    table {
        animation-name: fade-in;
        animation-duration: 2s;
    }
</style>