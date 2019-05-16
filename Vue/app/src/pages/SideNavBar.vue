<template>
    <div class="sidebar-options">
        <h4>{{model}}</h4>
            <router-link class="myButton" v-for="routes in links" v-bind:key="routes.id" :to="`${routes.page}`">
                <span>
                    <font-awesome-icon class="fa-icon" v-bind:icon="routes.icon" />
                    {{ routes.text }}
                </span>
            </router-link>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    export default {
        name: "SideNavBar",
        data () {
            return {
                // TODO I think these links should be moved to the state. And retrieved from there.
                
            }
        },

        computed: {

            model(){
                return this.$store.state.model;
            },

            links(){

                return  [
                    {
                        id: 0,
                        text: 'Model',
                        page: '/model',
                        storage_key: "model",
                        icon:"plane-departure"
                    },
                    {
                        id: 1,
                        text: 'Load Data',
                        page: '/data_load',
                        storage_key: "load_data",
                        icon:"table"
                    },
                    {
                        id: 2,
                        text: 'Solar Data',
                        page: '/data_solar',
                        storage_key: "data_solar",
                        icon:"table"
                    },
                    {
                        id: 3,
                        text: 'Arrangement',
                        page: this.model =="luomi" ? '/participants': '/participants_mike',
                        storage_key: "participants",
                        icon:"user"
                    },{
                        id: 4,
                        text: 'Tariffs',
                        page: this.model =="luomi" ? '/tariffs' : '/tariffs_mike',
                        storage_key: "tariffs",
                        icon:"exchange-alt"
                    },{
                        id: 5,
                        text: 'Batteries',
                        page: this.model =="luomi" ? '/central_services': '/battery_mike',
                        storage_key: "central_services",
                        icon:"battery-full"
                    },
                    // {
                    //     id: 6,
                    //     text: 'Financing',
                    //     page: '/financing',
                    //     storage_key: "financing",
                    //     icon:"money-check-alt"
                    // },
                    {
                        id: 7,
                        text: 'Review',
                        page: 'review',
                        storage_key: "review",
                        icon:"search"
                    },
                    {
                        id: 8,
                        text: 'Results',
                        page: this.model =="luomi" ? '/results': '/results_mike',
                        storage_key: "review",
                        icon:"poll"
                    },
                    {
                        id: 9,
                        text: 'Save / Load',
                        page: '/save_config',
                        storage_key: "save_config",
                        icon:"save"
                    },
                ]
            }
        },

        methods: {
        }
    }
</script>

<style scoped>

    .sidebar-options{
        justify-content:center;
        height:100%;
        /* padding-top: 15vh; */
        
    }
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
        height: 5vh;

        background-color:#F8F8F8;
        
        display:flex;
        flex-direction:row;
        justify-content:center;
        align-items:center;
        border-bottom:1px solid #D0D1D2;
        /* width:100%; */
        
        
    }

    .myButton span {
        display:flex;
        width:85%;
        justify-content:flex-start;
        align-items: center;
    }

    .myButton span .fa-icon {
        margin: 0 1vw 0 0;
    }

    

    .myButton:hover {
        /* background-color:rgb(196, 196, 196); */
        background-color:#262930;

    }

    .myButton:active {
        position:relative;
        top:1px;
    }

    .router-link-active{
        /* background-color:#42464D; */
        background-color:#262930;
        color:#1CA6DB;
        
    }

    
</style>