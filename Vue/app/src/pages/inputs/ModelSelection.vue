<template>
    <div class="background">
        <div class="main-container">
            <h1>{{ view_name }}</h1>
            <span class="input-line"
                v-for="input in input_data"
                :key="input.id">
                {{ input.display_text }}

                <SimpleNumberInput
                    v-if="input.tag==='my_number'"
                    v-model="input.value"
                    :my_placeholder="input.placeholder"/>

                <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                    v-model="input.value"
                    :my_options="my_options[input.dropdown_key]"
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
        name: "Model",

        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_selection",

                input_data: [
                    {
                        id: 0,
                        name: "model_type",
                        display_text: "Model ",
                        value: "",
                        dropdown_key:"model_type",
                        placeholder: "select model",
                        tag:"my_dropdown"
                    },
                    {
                        id: 1,
                        name: "network_type",
                        display_text: "Network Type ",
                        value: "",
                        dropdown_key:"network_type",
                        placeholder: "please select a model",
                        tag:"my_dropdown"
                    },
                ],

                my_options: {

                    network_options: {
                        "": [],

                        luomi_network_options: [
                            "Embedded Network",
                            "Peer to Peer Retail",
                        ],

                        mike: [
                            "Apartment",
                        ]
                    },

                    network_type:
                    [
                        "Apartment",
                        "Embedded Network",
                        "Peer to Peer Retail",
                    ],

                    model_type: [
                        "mike",
                        "luomi",
                        
                    ]
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
            save_model_selection(selection) {
                console.log("This");
            }
        }
    }
</script>

<style scoped>
    .main-container {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    .input-line {
        display:flex;
        flex-direction: row;
        justify-content:space-between;
        align-items:center;
        width: 20vw;
    }

</style>