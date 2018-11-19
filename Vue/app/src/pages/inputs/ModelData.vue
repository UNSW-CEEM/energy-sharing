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
        <br>
        </span>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    export default {
        name: "Data",

        model_page_name: "model_data",

        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,

                input_data: [
                    {
                        id: 0,
                        name: "data_source",
                        display_text: "Data Source  ",
                        value: "",
                        dropdown_key: "data_source",
                        placeholder: "Select One",
                        tag:"my_dropdown",
                    },
                    {
                        id: 1,
                        name: "scaling_factor",
                        display_text: "Scaling Factor ",
                        value: "",
                        placeholder: "Decimal Scaling Factor",
                        tag:"my_number"
                    },
                    {
                        id: 2,
                        name:"sharing_algorithm",
                        display_text: "Sharing Algorithm ",
                        value: "",
                        dropdown_key: "sharing_algorithm",
                        placeholder: "Select One",
                        tag:"my_dropdown"
                    },
                ],

                my_options: {
                    data_source: {
                        option_one: "Option 1",
                        option_two: "ABC"
                    },
                    sharing_algorithm: {
                        option_one: "Option 1",
                        option_two: "ABC"
                    },
                }
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
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
            }
        }
    }
</script>

<style scoped>

</style>