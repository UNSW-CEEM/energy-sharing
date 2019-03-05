<template>
    <div class="background">
        <div class="main-container">
            <h1 class="view-title">{{ view_name }}</h1>
            <table class="tariffs-table">
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
                <button @click="load_config(input_data.selected_config_file)">Load User Config</button>
                <button @click="save_config()">Save User Config</button>
                <button @click="load_config('default_config.csv')">Load Default</button>
            </div>

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

                input_data: {
                    selected_config_file: 'user_config.csv',

                    table_rows: [],

                    my_options: {
                        tariff_type_options: [
                            "Retail",
                            "TUOS",
                            "DUOS",
                            "NUOS",
                        ],
                    }
                },

                table_headers: [
                    {header_id: 0, name: "Tariff Type", additional_text:"Select"},
                    {header_id: 1, name: "Tariff Name", additional_text:"Label"},
                    {header_id: 2, name: "Solar FiT", additional_text:"$/kWh"},
                    {header_id: 3, name: "Peak", additional_text:"$/kWh"},
                    {header_id: 4, name: "Shoulder", additional_text:"$/kWh"},
                    {header_id: 5, name: "Off-Peak", additional_text:"$/kWh"},
                ],
            }
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            } else {
                this.add_row()
            }
        },

        methods: {
            add_row(tariff_type="", tariff_name="", fit_input="", peak_price="", shoulder_price="", off_peak_price="") {

                let array_length = this.input_data.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            col_id: 0,
                            name:"tariff_type",
                            tag:"my_dropdown",
                            dropdown_key: "tariff_type_options",
                            value: tariff_type,
                            placeholder:"Select Tariff Type",
                        },
                        {
                            col_id: 1,
                            name:"tariff_name",
                            tag:"my_number",
                            value: tariff_name,
                            placeholder:"Name",
                        },
                        {
                            col_id: 2,
                            name:"fit_input",
                            tag:"my_number",
                            value: fit_input,
                            placeholder:"$"
                        },
                        {
                            col_id: 3,
                            name:"peak_price",
                            tag:"my_number",
                            value: peak_price,
                            placeholder:"$",
                        },
                        {
                            col_id: 4,
                            name:"shoulder_price",
                            tag:"my_number",
                            value: shoulder_price,
                            placeholder:"$",
                        },
                        {
                            col_id: 5,
                            name:"off_peak_price",
                            tag:"my_number",
                            value: off_peak_price,
                            placeholder:"$",
                        },
                    ]
                };

                this.input_data.table_rows.push(new_row);
            },

            load_config(filename) {
                this.$socket.emit('load_config', this.model_page_name, filename)
            },

            save_config() {
                // this.save_page_simple();
                // let created_data = this.create_config_file(this.model_page_name);
                // let payload = {
                //     model_page_name: this.model_page_name,
                //     data: created_data,
                // };
                //
                // this.$socket.emit('save_config', this.model_page_name, this.selected_config_file, payload)
            }
        },

        sockets: {
            tariffs_file_channel: function(response) {
                console.log("tariffs: ", response);

                this.input_data.table_rows = [];
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
        animation-duration: 1s;
    }

    h1 {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    table {
        animation-name: fade-in;
        animation-duration: 1s;
    }
</style>