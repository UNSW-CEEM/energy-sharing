<template>
    <div class="background">
        <div class="main-container">
            <h1 class="view-title">{{ heading_text }}</h1>
            <span class="input-line" v-for="input in input_data.input_rows" :key="input.id">
                {{ input.display_text }}
                <SimpleNumberInput
                    v-if="input.tag==='my_number'"
                    v-model="input.value"
                    :my_placeholder="input.placeholder"/>

                <SimpleDropdown v-else-if="input.name==='central_solar_data'"
                    v-model="input.value"
                    v-on:input="get_solar_profiles(input.value)"
                    :my_options="input_data.my_options[input.dropdown_key]"
                    :my_placeholder="input.placeholder"/>

                <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                    v-model="input.value"
                    :my_options="input_data.my_options[input.dropdown_key]"
                    :my_placeholder="input.placeholder"/>
            </span>
         </div>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "Central_Solar",
        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "central_solar",
                heading_text: "Central Solar",

                input_data: {
                    selected_solar_file: '',

                    input_rows: [
                        {
                            id: 0,
                            name: "central_solar_data",
                            display_text: "Central Solar Data",
                            value: "",
                            dropdown_key: "solar_files_list",
                            placeholder: "Select One",
                            tag: "my_dropdown",
                        },
                        {
                            id: 1,
                            name: "central_solar_profile",
                            display_text: "Central Solar Profile",
                            value: "",
                            dropdown_key: "solar_profiles_options",
                            placeholder: "Select One",
                            tag: "my_dropdown",
                        },
                        {
                            id: 2,
                            name: "scaling_factor",
                            display_text: "Scaling Factor",
                            value: 1,
                            placeholder: "Decimal Scaling Factor",
                            tag: "my_number"
                        },
                        {
                            id: 3,
                            name: "sharing_algorithm",
                            display_text: "Sharing Algorithm",
                            value: "",
                            dropdown_key: "sharing_algorithm",
                            placeholder: "Select One",
                            tag: "my_dropdown"
                        },
                    ],

                    my_options: {
                        solar_files_list: [],

                        solar_profiles_options: [],

                        sharing_algorithm: [
                            "Fractional Allocation",
                            "Quota Allocation",
                        ],
                    }
                },
            }
        },

        created() {
            this.load_page_simple();
            this.get_solar_files();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            get_solar_files() {
                this.$socket.emit('get_solar_files')
            },

            get_solar_profiles (filename) {
                console.log("Retrieving: ", filename);
                this.$socket.emit('get_solar_profiles', filename)
            },
        },

        sockets: {
            filesChannel: function(response) {
                 if (response.key === 'solar_files_list') {
                    this.input_data.my_options[response.key] = response.data;
                }
            },

            profilesChannel: function(response) {
                this.input_data.my_options[response.key] = response.data;
            },
        }
    }
</script>

<style scoped>

    .main-container {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    .noBullets {
        list-style: none;
        background: white;
        margin: 10px;
    }

    .input-line{
        display:flex;
        flex-direction:row;
        justify-content:space-between;
        align-items:center;
        margin: 1vh 0 1vh 0;
        width:30vw;
    }


</style>