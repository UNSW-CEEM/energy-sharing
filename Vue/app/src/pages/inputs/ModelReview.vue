<template>
    <div class="background">
        <div class="model-title">
            <h1>{{ view_name }}</h1>
        </div>
        <div class="main-container" v-if="parsed">
            

            <div class="info-box">
                <div class="info-box-heading">
                    Data Sources
                </div>
                <div class="info-box-content">
                    <div> Selected solar file: {{parsed_parameters.model_data_sources.selected_solar_file |checkBlank}}</div>
                    <div> Selected load file: {{parsed_parameters.model_data_sources.selected_solar_file |checkBlank}}</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-heading">
                    Participants
                </div>
                <div class="info-box-content">
                    <table>
                        <tr><th>Participant ID</th><th>Participant Type</th><th>Retail Tariff</th><th>Load Profile</th><th>Solar Profile</th><th>Solar Scaling</th><th>Battery</th></tr>
                        
                        <tr v-for="p in parsed_parameters.model_participants" :key="p.row_id">
                            <td v-for="attribute in p.row_inputs" :key="attribute.name">
                                 {{attribute.value |checkBlank}}
                            </td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="info-box">
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

                this.$socket.emit('run_model', this.parsed_parameters);
                this.$router.push('results');
            },
        },
        mounted(){
            console.log('Mounting')
            this.parse_simple_pages();
            this.parse_all_table_pages();
            this.parsed_parameters = this.get_params();
            console.log('Parsed Params',this.parsed_parameters)
            this.parsed = true;
        }
    }
</script>

<style scoped>

    .main-container {
        display: flex;
        flex-direction:column;
        justify-content:space-between;
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
        background-color:rgba(114, 137, 218,1);
        cursor:pointer;
        color:black;
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 0 3vh 0;
        border-radius:3px;
    }

    .info-box{
        width: 80%;
        border: 1px solid grey;
        display:flex;
        flex-direction: column;
        justify-content:flex-start;
        border-radius:4px;
        margin:2vh 0 2vh 0;
    }

    .info-box-heading{
        background-color:grey;
        width:100%;
    }

    .info-box-content{
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
    }

</style>