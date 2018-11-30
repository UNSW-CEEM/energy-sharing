<template>
    <div class="top-nav">

        <!-- <div class="logos">
            CRC for Low Carbon Living
                <img src="/images/ceem-logo.png"/> 
        </div> -->
        
        <span>
            <div class="sim-title">
            <svg viewBox="0 0 200 18"><text text-anchor="middle" x="50%" y="60%" textLength="80%">Energy Sharing Sim</text></svg>    
            </div>
            <router-link
                    class="spacing"
                    v-for="routes in links"
                    v-bind:key="routes.id"
                    :to="`${routes.page}`">{{ routes.text }}</router-link>

            
        </span>


        
        
        
    </div>

    
</template>

<script>
    export default {
        name: "TopNavBar",
        data() {
            return {
                links: [
                    // {
                    //     id: 0,
                    //     text: 'Home',
                    //     page: '/'
                    // },
                    // {
                    //     id: 1,
                    //     text: 'About',
                    //     page: '/about'
                    // },
                    // {
                    //     id: 2,
                    //     text: 'Contact',
                    //     page: '/contact'
                    // },
                ]
            }
        }
    }
</script>

<style>
    .spacing {
        Margin-right: 10px;
    }

    .top-nav{
        display:flex; 
        flex-direction:row;
        justify-content:space-around;
        align-items:center;
    }

    


    .sim-title{
        font-size:0.5em;
        /* font-weight:bold; */
        color:rgb(197, 197, 197);
        /* animation-name: fade-in;
        animation-duration: 2s; */
        animation: 3s strokefill forwards; 
        fill:rgba(114, 137, 218,1);
        
    }

    @keyframes strokefill {
        0%		{stroke: rgba(114, 137, 218,1); fill: rgba(0,0,0,0); stroke-dashoffset:  25%; stroke-dasharray: 00% 50%; stroke-width: 0.4; }
        70%	{                       fill: rgba(0,0,0,0);                                                                        }
        80%	{stroke: rgba(114, 137, 218,1);                                                                                             }
        100%	{stroke: rgba(0,0,0,0); fill: rgba(114, 137, 218,1); stroke-dashoffset: -25%; stroke-dasharray: 50% 00%; stroke-width: 0.0; }
    }

    

    



</style>