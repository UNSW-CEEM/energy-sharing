<template>
    <div class="background">
       

         <div class="main-container" >
            
            <div class="info-box">
                <div class="info-box-heading">
                    Save Config
                </div>
                <div class="info-box-content">
                    <div class="save-button" v-on:click="saveToFile()"> Save</div>
                </div>
            </div>

            <div class="info-box">
                <div class="info-box-heading">
                    Load Config
                </div>
                <div class="info-box-content">
                    <div> 
                        <label class="text-reader">
                            <input type="file" @change="loadTextFromFile">
                        </label>
                    </div>
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
                this.download('config.json', params_string);
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

   

    .save-button{
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

</style>