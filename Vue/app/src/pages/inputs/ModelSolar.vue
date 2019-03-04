<template>
    <div class="background">
        <div class="main-container">
            <h1>{{ heading_text }}</h1>
            <span class="input-line" v-for="input in input_data" :key="input.id">
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
    import SaveLoad from '@/mixins/SaveLoadNew.vue';

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
                        value: 1,
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
                        "sample_pv_1.csv",
                        "sample_pv_2.csv",
                        "sample_pv_3.csv",
                    ],

                    sharing_algorithm: [
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

        }
    }
</script>

<style scoped>

    .main-container {
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .noBullets {
        list-style: none;
        background: white;
        margin: 10px;
    }

    h1{

    }

    span{

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