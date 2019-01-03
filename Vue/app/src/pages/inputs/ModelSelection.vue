<template>
    <div class="model">
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
                        placeholder: "select network",
                        tag:"my_dropdown"
                    },
                ],

                my_options: {

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
                for(let i = 0; i < this.input_data.length; i++) {
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
.input-line{
    display:flex;
    flex-direction: row;
    justify-content:space-between;
    align-items:center;
    width: 20vw;
    animation-name: fade-in;
    animation-duration: 2s;
}

h1{
    animation-name: fade-in;
    animation-duration: 2s;
}


</style>