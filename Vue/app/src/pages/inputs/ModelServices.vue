<template>
    <div class="background">
        

            <div class="container">
                <div class="container-header">Central Battery</div>
                <span class="input-line"
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

                </span>
            
            
            <!-- <h1>Central Solar</h1>
            <span class="input-line">
                {{ solar_sharing_algorithm.display_text }}
                <SimpleDropdown
                    v-model="solar_sharing_algorithm.value"
                    :my_options="my_options[solar_sharing_algorithm.dropdown_key]"
                    :my_placeholder="solar_sharing_algorithm.placeholder"
                />
            </span> -->
        </div>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "central_services",
        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "central_services",
                // heading_text: "Central Services",

                input_data: [
                    {
                        id: 0,
                        name: "capacity",
                        display_text: "Capacity (kWh) ",
                        value: 10,
                        placeholder: "kWh",
                        tag:"my_number"
                    },
                    {
                        id: 1,
                        name: "max_discharge",
                        display_text: "Max Discharge (kW) ",
                        value: 5,
                        placeholder: "kW",
                        tag:"my_number"
                    },
                    {
                        id: 2,
                        name: "cycle_efficiency",
                        display_text: "Cycle Efficiency (%) ",
                        value: 99,
                        placeholder: "%",
                        tag:"my_number"
                    },
                    // {
                    //     id: 3,
                    //     name:"dispatch_algorithm",
                    //     display_text: "Dispatch Algorithm ",
                    //     value: "ToU Arbitrage",
                    //     dropdown_key: "dispatch_algorithm",
                    //     placeholder: "Select One",
                    //     tag:"my_dropdown"
                    // },
                ],

                solar_sharing_algorithm: {
                    id: 4,
                    name: "sharing_algorithm",
                    display_text: "Central Solar Sharing Algorithm",
                    value: "",
                    dropdown_key: "solar_sharing_algorithm",
                    placeholder: "Select One",
                    tag: "my_dropdown"
                },

                my_options: {
                    dispatch_algorithm: [
                        "ToU Arbitrage",
                        // "NEM Sync"
                    ],

                    solar_sharing_algorithm: [
                            "Fractional Allocation",
                            "Quota Allocation",
                    ],
                }
            }
        },

        created() {
            this.load_page_simple();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {

        },
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";

    .container{
        background-color:$container-bg;
        color:$container-text;
        width:75vw;
        display:flex;
        flex-direction:column;
        align-items:center;

        animation-name: fade-in;
        animation-duration: 1s;
    }

    .container-header{
        background-color:$heading-bg;
        color:$heading-text;
        width:100%;
        font-size:1.2em;

    }


    .background{
        height:95vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
    }

    .input-line {
        width:30vw;
        display:flex;
        flex-direction:row;
        justify-content:space-between;
        align-items:center;
        margin: 1vh 0 1vh 0;
    }

    .view-title {

    }

    .input-line {

    }
</style>