<!--FOCUS ON ME AND MY COMPONENTS-->
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
        name: "CentralBattery",
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
                        name: "capacity",
                        display_text: "Capacity (kWh) ",
                        value: "",
                        placeholder: "kWh",
                        tag:"my_number"
                    },
                    {
                        id: 1,
                        name: "max_discharge",
                        display_text: "Max Discharge (kW) ",
                        value: "",
                        placeholder: "kW",
                        tag:"my_number"
                    },
                    {
                        id: 2,
                        name: "cycle_efficiency",
                        display_text: "Cycle Efficiency (%) ",
                        value: "",
                        placeholder: "%",
                        tag:"my_number"
                    },
                    {
                        id: 3,
                        name:"dispatch_algorithm",
                        display_text: "Dispatch Algorithm ",
                        value: "",
                        dropdown_key: "dispatch_algorithm",
                        placeholder: "Select One",
                        tag:"my_dropdown"
                    },
                ],

                my_options: {
                    dispatch_algorithm: [
                        "Option 1",
                        "ABC"
                    ]
                }
            }
        },

    }
</script>

<style scoped>

</style>