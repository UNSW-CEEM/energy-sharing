<template>
    <div class="top-nav">

        <!-- <div class="logos">
            CRC for Low Carbon Living
                <img src="/images/ceem-logo.png"/> 
        </div> -->
        
            <div class="logo">
                <font-awesome-icon class="fa-icon" icon="network-wired" />  
            </div>
            <div class="sim-title">
            <!-- <svg viewBox="0 0 200 18"><text text-anchor="middle" x="50%" y="60%" textLength="80%">Energy Sharing Sim</text></svg>     -->
                Energy Sharing Sim
            </div>

            <div class="sponsor-title">

                UNSW Center for Energy and Environmental Markets
            </div>
            <!-- <router-link
                    class="spacing"
                    v-for="routes in links"
                    v-bind:key="routes.id"
                    :to="`${routes.page}`">{{ routes.text }}</router-link> -->

            
        


        
        
        
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
        margin-right: 10px;
    }

    .top-nav{
        display:flex; 
        flex-direction:row;
        justify-content:flex-start;
        align-items:center;
        
    }

    .sponsor-title{
        font-size: 0.8em;
        margin: 0 2vw 0 2vw;
    }
    

    .logo{
        color:rgba(114, 137, 218,1);
        font-size:1.4em;
    }


    .sim-title{
        margin:0 0 0 1vw;
        font-size:1.2em;
        /* font-weight:bold; */
        color:rgba(114, 137, 218,1);
        animation-name: fade-in;
        animation-duration: 2s;
        /* animation: 3s strokefill forwards;  */
        /* fill:rgba(114, 137, 218,1); */
        
    }

    @keyframes strokefill {
        0%		{stroke: rgba(114, 137, 218,1); fill: rgba(0,0,0,0); stroke-dashoffset:  25%; stroke-dasharray: 00% 50%; stroke-width: 0.4; }
        70%	{                       fill: rgba(0,0,0,0);                                                                        }
        80%	{stroke: rgba(114, 137, 218,1);                                                                                             }
        100%	{stroke: rgba(0,0,0,0); fill: rgba(114, 137, 218,1); stroke-dashoffset: -25%; stroke-dasharray: 50% 00%; stroke-width: 0.0; }
    }

    

    



</style>