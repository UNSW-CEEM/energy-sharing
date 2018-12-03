<!--FOCUS ON ME AND MY COMPONENTS-->
<template>
    <div>
        <h1>{{ view_name }}</h1>
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
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    export default {
        name: "Central Battery",
        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "central_battery",

                input_data: [
                    {
                        id: 0,
                        name: "capacity",
                        display_text: "Capacity (kWh) ",
                        value: 9.8,
                        placeholder: "kWh",
                        tag:"my_number"
                    },
                    {
                        id: 1,
                        name: "max_discharge",
                        display_text: "Max Discharge (kW) ",
                        value: 3.2,
                        placeholder: "kW",
                        tag:"my_number"
                    },
                    {
                        id: 2,
                        name: "cycle_efficiency",
                        display_text: "Cycle Efficiency (%) ",
                        value: 0.95,
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
                        "ToU Arbitrage",
                        "NEM Sync"
                    ]
                }
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
        },

        beforeDestroy() {
            this.save_page();
            this.save_page_server();
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
        },
    }
</script>

<style scoped>

.input-line{
    width:30vw;
    display:flex;
    flex-direction:row;
    justify-content:space-between;
    align-items:center;
    margin: 1vh 0 1vh 0;
}

h1{
    animation-name: fade-in;
    animation-duration: 2s;
}


span{
    animation-name: fade-in;
    animation-duration: 2s;
}
</style>