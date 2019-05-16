<template>
    <div class="background">
        <!-- <div class="model-title">
            <h1>{{ view_name }}</h1>
        </div> -->

        <modal  width="40%" name="notready">
            <div class="info-box-heading">
                    Error
            </div>
            <div class="not-ready-container">
                
                <div class="message">{{not_ready_message}} </div>
                <div class="close-button" v-on:click="close_not_ready_modal()"> Close </div>
            </div>
        </modal>
        <div class="main-container" v-if="parsed">
            

            <div class="info-box">
                <div class="info-box-heading">
                    Data Sources
                </div>
                <div class="info-box-content">
                    <div> Selected solar file: {{selected_solar_file |checkBlank}}</div>
                    <div> Selected load file: {{selected_load_file |checkBlank}}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-heading">
                    Participants
                </div>
                <div class="info-box-content">
                    <table v-if='parsed_parameters.model_selection.model_type=="mike"'>
                        <tr><th>Participant ID</th><th>Tariff</th><th>Load Profile</th><th>Solar Profile</th></tr>
                        
                        <tr v-for="p in parsed_parameters.model_participants_mike" :key="p.row_id">
                            <td v-for="attribute in p.row_inputs" :key="attribute.name">
                                 {{attribute.value |checkBlank}}
                            </td>
                        </tr>
                        
                    </table>
                    <table v-else>
                        <tr><th>Participant ID</th><th>Participant Type</th><th>Retail Tariff</th><th>Load Profile</th><th>Solar Profile</th></tr>
                        
                        <tr v-for="p in parsed_parameters.model_participants" :key="p.row_id">
                            <td v-for="attribute in p.row_inputs" :key="attribute.name">
                                 {{attribute.value |checkBlank}}
                            </td>
                        </tr>
                        
                    </table>
                </div>
            </div>

            <div class="info-box" v-if="parsed_parameters.central_services">
                <div class="info-box-heading">
                    Central Services (Battery)
                </div>
                <div class="info-box-content">
                    <table>
                        <tr><th>Label</th><th>Value</th></tr>
                        <tr v-for="service in parsed_parameters.central_services" :key="service.name">
                            <td>{{service.display_text}}</td>
                            <td>{{service.value | checkBlank }}</td>
                        </tr>
                    </table>
                    <!-- {{parsed_parameters.central_services}} -->
                </div>
            </div>

            
        </div>
        <div class="run-button" @click="run_model()">
            <span v-if="!results_received">Run Model</span>
            <span v-if="results_received">Run Model</span>
        </div>
    </div>
</template>

<script>
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "Review",
        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                parsed:false,
                results_received: false,
                not_ready_message:''

                // parsed_parameters: {},
            }
        },
        filters:{
            checkBlank(item){
                if(!item || item == ""){
                    return "N/A"
                }else{
                    return item
                }
            }
        },

        computed:{
            selected_solar_file(){
                if(this.parsed_parameters.model_data_sources){
                    return this.parsed_parameters.model_data_sources.selected_solar_file;
                }else if(this.parsed_parameters.model_data_sources_mike){
                    return this.parsed_parameters.model_data_sources_mike.selected_solar_file;
                }else{
                    return "No File Selected"
                }
                
            },

            selected_load_file(){
                if(this.parsed_parameters.model_data_sources){
                    return this.parsed_parameters.model_data_sources.selected_load_file;
                }else if(this.parsed_parameters.model_data_sources_mike){
                    return this.parsed_parameters.model_data_sources_mike.selected_load_file;
                }else{
                    return "No File Selected"
                }
            }
        },

        sockets: {

        },

        methods: {
            run_model() {
                // this.parse_simple_pages();
                // this.parse_all_table_pages();
                var status = this.get_readiness_status()
                if(status.ready){
                    this.$socket.emit('run_model', this.parsed_parameters);
                    if(this.parsed_parameters.model_selection.model_type=="mike"){
                        this.$router.push('results_mike');
                    }else{
                        this.$router.push('results');
                    }
                }else{
                    this.not_ready_message = status.message
                    this.$modal.show('notready')
                }
                
                
            },
            close_not_ready_modal(){
                this.$modal.hide('notready')
            },
        },
        mounted(){
            console.log('Mounting')
            
            this.parsed_parameters = this.get_params();
            console.log('Parsed Params',this.parsed_parameters)
            this.parsed = true;
        }
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";

    .main-container {
        display: flex;
        flex-direction:column;
        // justify-content:space-around;
        align-items: center;
        animation-name: fade-in;
        animation-duration: 1s;
        width: 100%;
        height: 100%;
        overflow:auto;
    }

    .model-title {

    }

    .run-button{
        background-color:$button-primary;
        color:$button-text;
        cursor:pointer;
        
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 0 3vh 0;
        border-radius:3px;
    }

    .info-box{
        width: 80%;
        /* border: 1px solid grey; */
        display:flex;
        flex-direction: column;
        justify-content:flex-start;
        /* border-radius:4px; */
        margin:2vh 0 2vh 0;
        background-color: $container-bg;
        color:$container-text;
    }

    .info-box-heading{
        background-color:$heading-bg;
        color:$heading-text;
        font-size:1.2em;
        width:100%;
        text-align:center;
    }

    .info-box-content{
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
    }

    .not-ready-container{
        display:flex;
        flex-direction:column;
        justify-content:space-around;
        align-items:center;
        width:100%;
        height:100%;
       
    }

    .not-ready-container .message{
        color:$container-text;
        padding: 0 3vh 0 3vh;
        text-align:center;
    }

    .not-ready-container .close-button{
        background-color:$button-primary;
        padding: 1vh 1vw 1vh 1vw;
        border-radius:4px;
        cursor:pointer;
    }

</style>