<template>
    <div class="background">
        <div class="main-container">
            <h1>{{ view_name }}</h1>
            <span class="input-line">
                {{ input_data.model_dropdown.display_text }}
                <SimpleDropdown
                    v-model="input_data.model_dropdown.value"
                    v-on:input="save_model_selection(input_data.model_dropdown.value)"
                    :my_options="model_type_options"
                    :my_placeholder="input_data.model_dropdown.placeholder"/>
            </span>
            <span class="input-line">
                {{ input_data.network_dropdown.display_text }}
                <SimpleDropdown
                    v-model="input_data.network_dropdown.value"
                    :my_options="input_data.selected_model_options"
                    :my_placeholder="input_data.network_dropdown.placeholder"/>
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

                input_data: {
                    selected_model: "",
                    selected_model_options: [],

                    model_dropdown: {
                        name: "model_type",
                        value: "",
                        display_text: "Model",
                        placeholder: "select model",
                    },

                    network_dropdown: {
                        name: "network_type",
                        display_text: "Network Type ",
                        value: "",
                        dropdown_key:"network_type",
                        placeholder: "select model",
                    },
                },

                network_options: {
                    luomi: [
                        "Embedded Network",
                        "Peer to Peer Retail",
                    ],

                    mike: [
                        "Apartment",
                    ]
                },

                model_type_options: [
                    "mike",
                    "luomi",
                ],
            }
        },

        created() {
            this.load_page_simple();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            // frontend "global"ish variable. Set in the store. May be used for hiding financing page.
            save_model_selection(selection) {
                this.input_data.selected_model_options = this.network_options[selection];

                if (this.input_data.network_dropdown.value === "") {
                    this.input_data.network_dropdown.value = this.input_data.selected_model_options[0]
                }

                let payload = {
                    model_page_name: "selected_model",
                    data: selection
                };

                this.$store.commit('save_page', payload)
            },
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