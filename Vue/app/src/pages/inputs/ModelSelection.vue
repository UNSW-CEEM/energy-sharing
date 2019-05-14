<template>
    <div class="background">
        <div class="main-container">
            <!-- <h1>{{ view_name }}</h1> -->

            <div class="model">
                <div class="header">
                    <div class="title">
                        LUOMI
                    </div>
                    <div class="author">
                        by Naomi Stringer, Luke Marshall
                    </div>
                </div>

                <div class="picture">
                    <font-awesome-icon class="fa-icon" icon="industry" />  
                </div>

                <div class="description">
                    This model is commonly used to model small embedded networks and local energy sharing schemes with small numbers of participants. It allows for a central battery, and solar and load data for each participant. 
                </div>
                <div class="selected" v-if="input_data.selected_model=='luomi'">
                    Selected ✓
                </div>
                <div v-else class="not-selected" v-on:click="select_model('luomi')">
                    Select
                </div>
                
            </div>

            <div class="model">
                <div class="header">
                    <div class="title">
                        Apartment Model
                    </div>
                    <div class="author">
                        by Mike Roberts
                    </div>
                </div>

                <div class="picture">
                    <font-awesome-icon class="fa-icon" icon="building" />  
                </div>

                <div class="description">
                    This model is designed to handle large embedded networks in apartment blocks and high density residential complexes. It allows for the calculation of energy flows between many participants, and the sharing of a central solar and battery resource.
                </div>
                <div class="selected" v-if="input_data.selected_model=='mike'">
                    Selected ✓
                </div>
                <div v-else class="not-selected" v-on:click="select_model('mike')">
                    Select
                </div>
                
            </div>
           
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
                    selected_model: "mike",
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

                

               
            }
        },

        created() {
            this.load_page_simple();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            select_model(model){
                this.input_data.selected_model= model;
                this.$store.commit('model', model)
            },
            // frontend "global"ish variable. Set in the store. May be used for hiding financing page.
            // save_model_selection(selection) {
            //     this.input_data.selected_model_options = this.network_options[selection];

            //     if (this.input_data.network_dropdown.value === "") {
            //         this.input_data.network_dropdown.value = this.input_data.selected_model_options[0]
            //     }

            //     let payload = {
            //         model_page_name: "selected_model",
            //         data: selection
            //     };

            //     this.$store.commit('save_page', payload)
            // },
        }
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";
    .main-container {
        animation-name: fade-in;
        animation-duration: 1s;
        display:flex;
        flex-direction:row;
        justify-content:space-around;
        align-items:center;
        height:100%;
        width:100%;
        
    }

    .model{
        border-radius:2px;
        /* border: 1px solid grey; */
        height:80vh;
        width: 35vw;
        display:flex;
        flex-direction:column;
        justify-content: space-between;
        align-items:center;
        background-color:#F8F8F8;
        
        /* color:#9F86FF; */
        /* background-color:#3E327B; */
    }

    .title{
        font-size:1.7em;
        font-weight:bold;
        color:rgba(28, 166, 219,1);
    }
    .author{
        font-size:0.8em;
        color:rgba(28, 166, 219,1);
    }

    .header{
        /* background-color:#e0e0e0; */
        width:100%;
        padding-bottom:0.5vh;
    }

    .description{
        color:grey;
        text-align:left;
        margin: 0 2vw 0 2vw;
    }

    .selected{
        background-color: #6BEE9C;
        background-color: $tertiary;
        padding:1vh 1vw 1vh 1vw;
        border-radius:2px;
        margin: 0 0 2vh 0;
        cursor:pointer;
        color:white;
    }

    .not-selected{
        background-color: $secondary;
        padding:1vh 1vw 1vh 1vw;
        border-radius:2px;
        margin: 0 0 2vh 0;
        cursor:pointer;
        color:white;
    }

    .input-line {
        display:flex;
        flex-direction: row;
        justify-content:space-between;
        align-items:center;
        width: 20vw;
    }

    .picture{
        font-size:6em;
        background-color:$container-text;
        width:15vw;
        height:15vw;

        display:flex;
        justify-content:center;
        align-items:center;
        
        border-radius:100px;
    }

</style>