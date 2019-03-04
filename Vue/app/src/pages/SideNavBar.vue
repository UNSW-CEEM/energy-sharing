<template>
    <div >
        <h2>Inputs</h2>
            <router-link class="myButton" v-for="routes in links" v-bind:key="routes.id" :to="`${routes.page}`">
            <span>
                <font-awesome-icon class="fa-icon" v-bind:icon="routes.icon" />
                {{ routes.text }}
            </span>
            </router-link>
    </div>
</template>

<script>
    export default {
        name: "SideNavBar",
        data () {
            return {
                // TODO I think these links should be moved to the state. And retrieved from there.
                links: [
                    {
                        id: 0,
                        text: 'Model',
                        page: '/model',
                        storage_key: "model",
                        icon:"plane-departure"
                    },
                    {
                        id: 1,
                        text: 'Load Upload',
                        page: '/data_load',
                        storage_key: "load_data",
                        icon:"table"
                    },
                    {
                        id: 2,
                        text: 'Solar Upload',
                        page: '/data_solar',
                        storage_key: "data_solar",
                        icon:"table"
                    },
                    {
                        id: 3,
                        text: 'Participants',
                        page: '/participants',
                        storage_key: "participants",
                        icon:"user"
                    },{
                        id: 4,
                        text: 'Tariffs',
                        page: '/tariffs',
                        storage_key: "tariffs",
                        icon:"exchange-alt"
                    },{
                        id: 5,
                        text: 'Central Solar',
                        page: '/central_solar',
                        storage_key: "central_solar",
                        icon:"solar-panel"
                    },{
                        id: 6,
                        text: 'Central Battery',
                        page: '/central_battery',
                        storage_key: "central_battery",
                        icon:"battery-full"
                    },{
                        id: 7,
                        text: 'Financing',
                        page: '/financing',
                        storage_key: "financing",
                        icon:"money-check-alt"
                    },{
                        id: 8,
                        text: 'Review',
                        page: 'review',
                        storage_key: "review",
                        icon:"search"
                    },
                    {
                        id: 9,
                        text: 'Results',
                        page: 'results',
                        storage_key: "review",
                        icon:"poll"
                    },
                ]
            }
        },

        methods: {
        }
    }
</script>

<style scoped>
    .list-item {
        display:flex;
        flex-direction:row;
    }

    .fa-icon {
        width:3vw;
    }


    .myButton {
        border-radius:1px;

        cursor:pointer;
        color:grey;
        text-decoration:none;
        font-size:1.1em;
        padding:10px 10px;
        height: 10px;
        
        display:flex;
        flex-direction:row;
        justify-content:center;
        align-items:center;
        /* width:100%; */
        
        
    }

    .myButton span {
        display:flex;
        width:80%;
        justify-content:flex-start;
        align-items: center;
    }

    .myButton span .fa-icon {
        margin: 0 1vw 0 0;
    }

    

    .myButton:hover {
        background-color:#36393F;

    }

    .myButton:active {
        position:relative;
        top:1px;
    }

    .router-link-active{
        background-color:#42464D;
    }

    
</style>