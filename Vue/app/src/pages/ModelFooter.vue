<template>
    <div class="footercontainer">
        <!-- <div class="status" v-if="!sleeping"> Status: {{ status }} </div>         -->
        <modal height="80%"  width="80%" name="status">
            <div class="status" v-if="!sleeping"> Status: {{ status }} </div>
        </modal>
    </div>
</template>

<script>
    export default {
        name: "ModelFooter",

        data() {
            return {
                is_connected: false,
                sleeping: true,
                status:'ready',
                status: "",
            }
        },

        watch:{
            status(){
                if(this.status =='running') {
                    console.log('RUNNING!')
                    this.$modal.show('status')
                }
                if(this.status =='finished') {
                    console.log('RUNNING!')
                    this.$modal.hide('status')
                }
            }
        },

        sockets: {
            status_message_channel: function (response) {
                this.is_connected = true;
                this.sleeping = false;
                this.status = response.data.message;
            },
            status_channel: function (response) {
                
                this.status = response.data.status;
                console.log('New Running Status Update', response, this.is_running);
                
            }
        },

        computed: {
            completed_pages: {
                get() {
                    return this.$store.state.frontend_state.completed_pages;
                }
            },
            total_pages: {
                get() {
                    return this.$store.state.frontend_state.total_pages;
                }
            }
        },

        methods: {

        }
    }
</script>

<style scoped>
.status{
    display:flex;
    flex-direction:row;
    justify-content: center;
    align-items: center;
    width:100%;
    height:100%;
}

.footercontainer{
    height:0px;
}
</style>