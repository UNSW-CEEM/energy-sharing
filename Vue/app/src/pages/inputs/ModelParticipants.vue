<!--FOCUS ON ME AND MY COMPONENTS-->
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
        <button @click="load_config()">Load from config file</button>
        <button @click="save_config()">Save to config file</button>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    export default {
        name: "Participants",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name:"model_participants",

                table_headers: [
                    {id: 0, name: "Participant ID", additional_text:"ID"},
                    {id: 1, name: "Participant Type", additional_text:"Type"},
                    {id: 2, name: "Tariff Type", additional_text:"Select One"},
                    {id: 3, name: "Load Data", additional_text:"Select One"},
                    {id: 4, name: "Solar Data", additional_text:"Select One"},
                    {id: 5, name: "Solar Scaling", additional_text:"Input Number"},
                    {id: 6, name: "Battery", additional_text:"Select One"},
                ],

                table_rows: [],

                my_options: {
                    participant_type_options: [
                        "PV & Load",
                        "Load",
                        "PV",
                    ],

                    tariff_type_options: [
                        "AGL TOU 1",
                        "Tariff 2",
                        "Another Tariff",
                    ],

                    battery_options: [
                        "Battery Option 1",
                        "Battery Option 2",
                    ],

                    solar_data_files: [],

                    load_data_options: [],

                },
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.table_rows = this.$store.state.frontend_state[this.model_page_name]
            } else {
                this.add_row()
            }
        },

        beforeDestroy() {
            this.save_page()
            this.save_page_server()
        },

        methods: {
            add_row() {
                let array_length = this.table_rows.length;
                let participant_default = "Participant " + array_length.toString();
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            id: 0,
                            name: "participant_id",
                            tag: "my_number",
                            value:participant_default,
                            placeholder:participant_default,
                        },
                        {
                            id: 1,
                            name: "participant_type",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key: "participant_type_options",
                            placeholder:"Type",
                        },
                        {
                            id: 2,
                            name: "tariff_type",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"tariff_type_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 3,
                            name: "load_data",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"load_data_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 4,
                            name: "solar_data",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"solar_data_files",
                            placeholder:"Select One",
                        },
                        {
                            id: 5,
                            name: "solar_scaling",
                            tag: "my_number",
                            value:"",
                            placeholder:"Input Number",
                        },
                        {
                            id: 6,
                            name: "battery_type",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"battery_options",
                            placeholder:"Select Battery",
                        },
                    ]
                };

                this.table_rows.push(new_row);
            },

            save_page() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.table_rows
                };
                this.$store.commit('save_page', payload)
            },

            save_page_server() {
                let data = [];

                for(var i = 0; i < this.table_rows.length; i++) {
                    let row = this.table_rows[i].row_inputs;
                    let row_data = []

                    for( var j = 0; j < row.length; j++) {
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

            },

            save_config() {

            }
        }
    }
</script>

<style scoped>
h1{
    animation-name: fade-in;
    animation-duration: 2s;
}

table{
    animation-name: fade-in;
    animation-duration: 2s;
}

button{
    animation-name: fade-in;
    animation-duration: 2s;
}
</style>