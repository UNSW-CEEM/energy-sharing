<template>
    <div class="background">
        <modal width="40%" height="40%" name="clear">
            <div class="modal-content">
                <div class="info-box-heading">
                    Clear
                </div>

                <div class="info-box-content">
                    Are you sure you want to clear all settings and start again?
                </div>

                <div class="modal-button-line">
                    <div class="deny-button" v-on:click="$modal.hide('clear')">Don't Clear</div>
                    <div class="confirm-button" v-on:click="clear_params()">Clear</div>
                </div>
            </div>
        </modal>

        <modal width="40%" height="40%" name="load-success">
            <div class="modal-content">
                <div class="info-box-heading">
                    Success
                </div>

                <div class="info-box-content">
                    The configuration file was successfully loaded.
                </div>

                <div class="modal-button-line">
                    <div class="confirm-button" v-on:click="$modal.hide('load-success')">Close</div>
                </div>
            </div>
        </modal>

         <div class="main-container" >
            
            <div class="info-box">
                <div class="info-box-heading">
                    Save Configuration
                </div>
                
                <div class="info-box-content">
                    <div class="config-name">
                        <span class="config-name-label">File Name</span>
                        <input v-model="config_name">
                    </div>
                    <div class="confirm-button" v-on:click="saveToFile()"> Save</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-heading">
                    Load Configuration
                </div>
                <div class="info-box-content">
                    <div> 
                        <label class="text-reader">
                            <input type="file" @change="loadTextFromFile">
                        </label>
                    </div>
                </div>
            </div>

             <div class="info-box">
                <div class="info-box-heading">
                    Clear Configuration
                </div>
                <div class="info-box-content">
                    <div class="confirm-button" v-on:click="$modal.show('clear')"> Clear</div>
                </div>
            </div>

        </div>
       
    </div>
</template>

<script>
    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "SaveConfig",
        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                config_name:'Simulation 1'
            }
        },
        

        computed:{
           
        },

        sockets: {

        },

        methods: {
           loadTextFromFile(ev) {
                console.log('Loading text from file!');
                const file = ev.target.files[0];
                const reader = new FileReader();
                var self = this;
                reader.onload = function(e) {
                    // console.log(e.target.result);
                    var params = JSON.parse(e.target.result);
                    // console.log(params)
                    self.$store.commit('load_config', params)
                    self.$store.commit('model', params.model_selection.selected_model)
                    self.$modal.show('load-success')
                }
                
                //This will trigger the above onload function and then allow processing. 
                reader.readAsText(file);
                
                
                // var file_text = reader.result;
                
                // console.log('file_text:',file_text);
                // var params = JSON.parse(file_text);
                // console.log('params:\n',params);
                // this.$store.commit('load_config', params)
            },

            saveToFile(){
                var params_string = JSON.stringify(this.$store.state.frontend_state);
                this.download(this.config_name+'.json', params_string);
            },

            download(filename, text) {
                console.log('Downloading!')
                var pom = document.createElement('a');
                pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
                pom.setAttribute('download', filename);

                if (document.createEvent) {
                    var event = document.createEvent('MouseEvents');
                    event.initEvent('click', true, true);
                    pom.dispatchEvent(event);
                }
                else {
                    pom.click();
                }
            },
            clear_params(){
                this.$store.commit('clear_params')
                this.$modal.hide('clear');
            }

        },
        mounted(){
           
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

   

    .confirm-button{
        background-color:$button-primary;
        color:$button-text;
        cursor:pointer;
        
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 1vw 3vh 1vw;
        border-radius:3px;
    }

    .deny-button{
        background-color:$button-warning;
        color:$button-text;
        cursor:pointer;
        
        padding: 1vh 3vw 1vh 3vw;
        margin: 1vh 1vw 3vh 1vw;
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
        margin: 3vh 0 3vh 0;
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

    .modal-content{
        display:flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        color:$container-text;
        height:100%;
    }

    .modal-button-line{
        display:flex;
        flex-direction:row;
    }

    .config-name{
        display:flex;
        flex-direction:row;
        justify-content:center;
        align-items:center;
        margin: 0 0 2vh 0;
    }
    .config-name-label{
        font-size:0.8em;
        margin: 0 1vw 0 1vw;
    }

</style>