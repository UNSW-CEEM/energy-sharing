<template>
    <div>
        <h1>Local Energy Sharing Simulator</h1>
        <p>Click 'Model' on the left to get started. </p>
        
        <modal height="80%"  width="80%" name="hello-world">
            <div class="modal-content">
                <h1>Local Energy Sharing Simulator</h1>
                <div class="logos">
                    <img class="logo" src="/images/ceem-logo.png">
                    <img class="logo" src="/images/crc-logo.png">
                    <img class="logo" src="/images/unsw-logo.jpg">
                </div>

                <div class="get-started-button" v-on:click="hide">Get Started</div>
            </div>
        </modal>
    </div>
    
</template>



<script>
    
    export default {
        name: 'Home',
        methods:{
            show(){
                //modal is a plugin found here: https://www.npmjs.com/package/vue-js-modal
                this.$modal.show('hello-world');
            },
            hide(){
                this.$modal.hide('hello-world');
            }
        },
        mounted(){
            this.$modal.show('hello-world');
        }
    }

</script>

<style>



.modal-content{
    display:flex;
    flex-direction:column;
    justify-content:space-around;
    align-items: center;
    width:100%;
    height:100%;
    color:black;
    
}
.logos{
    display:flex;
    flex-direction:row;
    justify-content: space-around;
    align-items: center;
}

.logos .logo{
    width:20%;
}

.get-started-button{
    cursor:pointer;
    background-color:rgba(114, 137, 218,1);
    padding:1.2vh 4vw 1.2vh 4vw;
    border-radius:3px;
    font-weight: bold;
}

.modal-content h1{
    font-weight: lighter;
}





</style>
