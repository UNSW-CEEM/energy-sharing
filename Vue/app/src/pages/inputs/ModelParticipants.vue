<template>
    <div class="background">
        <div class="main-container">
            <h1 class="view-title">{{ view_name}}</h1>
            <div class="files-select-container">
                <h4 class="load-title">Load File:</h4>
                <SimpleDropdown
                        v-model="input_data.selected_load_file"
                        v-on:input="get_load_profiles(input_data.selected_load_file)"
                        :my_options="input_data.load_files_list"
                        :my_placeholder="'Select File'"/>

                <h4 class="solar-title">Solar File:</h4>
                <SimpleDropdown
                        v-model="input_data.selected_solar_file"
                        v-on:input="get_solar_profiles(input_data.selected_solar_file)"
                        :my_options="input_data.solar_files_list"
                        :my_placeholder="'Select File'" />
            </div>

            <table class="participants-table">
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

            <button @click="add_row()">Add Participant</button>

            <div class="file-buttons-container">
                <!--<button @click="load_participants_config(input_data.selected_config_file)">Load User Config</button>-->
                <!--<button @click="save_config()">Save User Config</button>-->
                <button @click="load_participants_config('default_config.csv')">Load from default file</button>
            </div>
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

                input_data: {
                    selected_solar_file: '',
                    selected_load_file: '',
                    selected_config_file: 'user_config.csv',

                    solar_files_list: [],
                    load_files_list: [],

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
                            "Central Battery"
                        ],

                        solar_profiles_options: [],
                        load_profiles_options: [],
                    },

                },

                table_headers: [
                    {id: 0, name: "Participant ID", additional_text:"ID"},
                    {id: 1, name: "Participant Type", additional_text:"Type"},
                    {id: 2, name: "Tariff Type", additional_text:"Select One"},
                    {id: 3, name: "Load Data", additional_text:"Select One"},
                    {id: 4, name: "Solar Data", additional_text:"Select One"},
                    {id: 5, name: "Solar Scaling", additional_text:"Input Number"},
                    {id: 6, name: "Battery", additional_text:"Select One"},
                ],
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            } else {
                this.add_row()
            }
            this.get_solar_files();
            this.get_load_files();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            add_row(participant_id="", participant_type="", retail_tariff_type="", load_profile="", solar_profile="", solar_scaling=1, battery_type="No Battery") {
                let array_length = this.input_data.table_rows.length
                // let participant_default = "participant_" + Number(array_length+1).toString();
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            id: 0,
                            name: "participant_id",
                            tag: "my_number",
                            value:participant_id,
                            placeholder:participant_id,
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
                            dropdown_key:"load_profiles_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 4,
                            name: "solar_profile",
                            tag: "my_dropdown",
                            value:solar_profile,
                            dropdown_key:"solar_profiles_options",
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

                this.input_data.table_rows.push(new_row);
            },

            get_solar_files() {
                this.$socket.emit('get_solar_files')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
            },

            get_solar_profiles (filename) {
                this.$socket.emit('get_solar_profiles', filename)
            },

            get_load_profiles (filename) {
                this.$socket.emit('get_load_profiles', filename)
            },

            save_config() {
                console.log("Re-implement Me");
            },

            load_participants_config(file) {
                this.$socket.emit('load_participants_config', this.model_page_name, file)
            },
        },

        sockets: {
            filesChannel: function(response) {
                 if (response.key === 'solar_files_list') {
                    this.input_data.solar_files_list = response.data;
                } else {
                    this.input_data.load_files_list = response.data;
                }
            },

            profilesChannel: function(response) {
                this.input_data.my_options[response.key] = response.data;
            },

            participants_file_channel: function(response) {
                this.input_data.table_rows = [];
                this.input_data.selected_solar_file = response["data"][0]["row_inputs"]["selected_solar_file"];
                this.input_data.selected_load_file = response["data"][0]["row_inputs"]["selected_load_file"];

                this.input_data.my_options["solar_profiles_options"] = response["solar_profiles_options"];
                this.input_data.my_options["load_profiles_options"] = response["load_profiles_options"];

                for (let i = 0; i < response["data"].length; i++) {
                    let data = response["data"][i]["row_inputs"];

                    this.add_row(
                        data["participant_id"],
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
    .main-container {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    .view-title {

    }

    .participants-table {

    }

    button {

    }

    .files-select-container {
        display: flex;
        flex-direction: row;
        width:50%;
        justify-content: space-evenly;
        align-items: center;

    }

    .file-buttons-container {

    }

</style>