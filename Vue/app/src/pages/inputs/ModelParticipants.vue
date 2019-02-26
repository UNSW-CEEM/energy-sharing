<template>
    <div>
        <h1>{{ view_name }}</h1>
        <div class="files-dd-container">
            <h4>Solar File:</h4>
            <SimpleDropdown
                    v-model="selected_solar_file"
                    :onchange="get_solar_profiles(selected_solar_file)"
                    :my_options="solar_files_list"
                    :my_placeholder="'Select File'" />
            <h4>Load File:</h4>
            <SimpleDropdown
                    v-model="selected_load_file"
                    :onchange="get_load_profiles(selected_load_file)"
                    :my_options="load_files_list"
                    :my_placeholder="'Select File'"/>
        </div>

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
            <button @click="add_row()">Add Participant</button>
        </table>

        <div class="file-buttons-container">
            <button @click="load_participants_config(selected_config_file)">Load from user file</button>
            <button @click="save_config()">Save to user file</button>
            <button @click="load_participants_config('default_config.csv')">Load from default file</button>
        </div>

    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "Participants",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name:"model_participants",
                is_connected: false,

                // Constants for now
                selected_solar_file: '',
                selected_load_file: '',
                solar_files_list: [],
                load_files_list: [],

                // Constants for now
                selected_config_file: 'user_config.csv',
                // config_files_list: ['default_config.csv'],

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
                        "Solar & Load",
                        "Load",
                        "solar",
                    ],

                    tariff_type_options: [
                        "AGL TOU 1",
                        "Tariff 2",
                        "Another Tariff",
                        "Business TOU"
                    ],

                    battery_options: [
                        "No Battery",
                        "Tesla PowerWall",
                        "RedFlow",
                    ],

                    solar_profiles_list: [],
                    load_profiles_list: [],
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
            this.get_solar_files();
            this.get_load_files();
        },

        methods: {
            add_row(participant_type="", retail_tariff_type="", load_profile="", solar_profile="", solar_scaling=1, battery_type="No Battery") {
                let array_length = this.table_rows.length;
                let participant_default = "participant_" + Number(array_length+1).toString();
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
                            value:participant_type,
                            dropdown_key: "participant_type_options",
                            placeholder:"Type",
                        },
                        {
                            id: 2,
                            name: "retail_tariff_type",
                            tag: "my_dropdown",
                            value:retail_tariff_type,
                            dropdown_key:"tariff_type_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 3,
                            name: "load_profile",
                            tag: "my_dropdown",
                            value:load_profile,
                            dropdown_key:"load_profiles_list",
                            placeholder:"Select One",
                        },
                        {
                            id: 4,
                            name: "solar_profile",
                            tag: "my_dropdown",
                            value:solar_profile,
                            dropdown_key:"solar_profiles_list",
                            placeholder:"Select One",
                        },
                        {
                            id: 5,
                            name: "solar_scaling",
                            tag: "my_number",
                            value:solar_scaling,
                            placeholder:"Input Number",
                        },
                        {
                            id: 6,
                            name: "battery_type",
                            tag: "my_dropdown",
                            value:battery_type,
                            dropdown_key:"battery_options",
                            placeholder:"Select Battery",
                        },
                    ]
                };

                this.table_rows.push(new_row);
            },

            get_solar_files() {
                this.$socket.emit('get_solar_files')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
            },

            load_profiles() {
                this.get_solar_profiles(this.selected_solar_file);
                this.get_load_profiles(this.selected_load_file);
            },

            get_solar_profiles (filename) {
                this.$socket.emit('get_solar_profiles', filename)
            },

            get_load_profiles (filename) {
                this.$socket.emit('get_load_profiles', filename)
            },

            save_config() {
                let table_data = this.combine_table_data();

                let payload = {
                    model_page_name: this.model_page_name,
                    data: table_data,
                };

                let additional_headers = {
                    "selected_solar_file": this.selected_solar_file,
                    "selected_load_file": this.selected_load_file
                };

                this.$socket.emit('save_config', this.model_page_name, this.selected_config_file, payload, additional_headers)
            },

            load_participants_config(file) {

                // this.$socket.emit('load_participants_config', this.model_page_name, this.selected_config_file)
                this.$socket.emit('load_participants_config', this.model_page_name, file)
            },
        },

        sockets: {
            filesChannel: function(response) {
                this.is_connected = true;
                if (response.key === 'solar_files_list') {
                    this.solar_files_list = response.data;
                } else {
                    this.load_files_list = response.data;
                }
            },

            profilesChannel: function(response) {
                this.is_connected = true;
                this.my_options[response.key] = response.data;
            },

            participants_file_channel: function(response) {
                this.is_connected = true;
                this.table_rows = [];

                this.my_options["solar_profiles_list"] = response["solar_profiles_list"]
                this.my_options["load_profiles_list"] = response["load_profiles_list"]

                for (let i = 0; i < response["data"].length; i++) {
                    let data = response["data"][i]["row_inputs"];

                    this.add_row(
                        data["participant_type"],
                        data["retail_tariff_type"],
                        data["load_profile"],
                        data["solar_profile"],
                        data["solar_scaling"],
                        data["battery_type"],
                    );
                }
            }
        }
    }
</script>

<style scoped>
    h1 {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    table {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    button {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .files-dd-container {
        display: flex;
        flex-direction: row;
        width:50%;
        justify-content: space-evenly;
        align-items: center;
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .file-buttons-container {
        /*display: flex;*/
        /*justify-content: space-around;*/
        animation-name: fade-in;
        animation-duration: 2s;
    }

</style>