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
        name: "CentralSolar",

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

                    data_source: [
                        "Option 1",
                        "ABC",
                    ],

                    sharing_algorithm: [
                        "Option 1",
                        "ABC",
                    ],

                }
            }
        },
        computed: {

        },
        methods: {

        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
        background: white;
        margin: 10px;
    }


</style>