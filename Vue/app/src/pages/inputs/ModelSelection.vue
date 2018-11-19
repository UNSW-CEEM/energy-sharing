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
        name: "Model",

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
                        name: "simulation",
                        display_text: "Simulation ",
                        value: "",
                        dropdown_key:"simulation_type",
                        placeholder: "select simulation",
                        tag:"my_dropdown"
                    },
                    {
                        id: 1,
                        name: "network_type",
                        display_text: "Network Type ",
                        value: "",
                        dropdown_key:"network_type",
                        placeholder: "select network",
                        tag:"my_dropdown"
                    },
                ],

                my_options: {

                    network_type:
                    [
                        "Option 1",
                        "ABC"
                    ],

                    simulation_type: [
                        "Sim 1",
                        "Sim 2"
                    ]
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

</style>