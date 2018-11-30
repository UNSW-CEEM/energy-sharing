<template>
    <div>
        <h1>{{ view_name }}</h1>
        <span
            v-for="input in input_data"
            :key="input.id">{{ input.display_text }}

            <SimpleNumberInput
                v-if="input.tag==='my_number'"
                v-model="input.value"
                :my_placeholder="input.placeholder"/>

            <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                v-model="input.value"
                :my_options="my_options[input.dropdown_key]"
                :my_placeholder="input.placeholder"/>

            <button @click="">{{ input.button_text }}</button>
        <br>
        </span>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    export default {
        name: "Data",

        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_data",
                is_connected: false,

                input_data: [
                    {
                        id: 0,
                        name: "solar_data_source",
                        display_text: "Solar Data Sources",
                        value: "",
                        dropdown_key: "solar_files_list",
                        placeholder: "Select One",
                        tag:"my_dropdown",
                        button_text:"Add",
                        add_function: "",
                    },
                    {
                        id: 1,
                        name: "load_data_source",
                        display_text: "Load Data Sources",
                        value: "",
                        dropdown_key: "load_files_list",
                        placeholder: "Select One",
                        tag:"my_dropdown",
                        button_text:"Add",
                        add_function: "",
                    },
                ],

                my_options: {
                    solar_files_list: [],
                    load_files_list: [],
                }
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
            this.get_solar_files()
            this.get_load_files()
        },

        beforeDestroy() {
            this.save_page()
            this.save_page_server()
        },

        methods: {
            save_page() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.input_data
                };
                this.$store.commit('save_page', payload)
            },

            save_page_server() {
                let data = [];
                for(var i = 0; i < this.input_data.length; i++) {
                    data.push({
                        "name": this.input_data[i].name,
                        "value": this.input_data[i].value
                    })
                }
                let payload = {
                    model_page_name: this.model_page_name,
                    data: data,
                };
                this.$store.commit('save_server_page', payload)
            },

            add_solar_source() {

            },

            add_load_source() {

            },

            get_solar_files() {
                console.log("Getting solar files")
                this.$socket.emit('get_solar_files')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
            },

        },

        sockets: {
            connect: function() {
                console.log("This client connected");
                this.is_connected = true;
            },

            disconnect: function() {
                this.is_connected = false;
            },

            filesChannel: function(response) {
                console.log("received response: ", response)
                this.is_connected = true;
                this.my_options[response.key] = response.data;
            },
        }
    }
</script>

<style scoped>
h1{
    animation-name: fade-in;
    animation-duration: 2s;
}

span{
    animation-name: fade-in;
    animation-duration: 2s;
}
</style>