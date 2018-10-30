<template>
    <div>
        <h2>Side Nav Bar</h2>
        <router-link
            class="myButton"
            v-for="routes in links"
            v-bind:key="routes.id"
            :to="`${routes.page}`">{{ routes.text }}</router-link>
    </div>
</template>

<script>
    export default {
        name: "SideNavBar",
        data () {
            return {
                links: [
                    {
                        id: 0,
                        text: 'Model',
                        page: '/model'
                    },
                    {
                        id: 1,
                        text: 'Data',
                        page: '/data'
                    },
                    {
                        id: 2,
                        text: 'Participants',
                        page: '/participants'
                    },{
                        id: 3,
                        text: 'Tariffs',
                        page: '/tariffs'
                    },{
                        id: 4,
                        text: 'Central Solar',
                        page: '/central_solar'
                    },{
                        id: 5,
                        text: 'Central Battery',
                        page: '/central_battery'
                    },{
                        id: 6,
                        text: 'Financing',
                        page: '/financing'
                    },{
                        id: 7,
                        text: 'Review',
                        page: 'review'
                    },
                    {
                        id: 8,
                        text: 'Sockets',
                        page: '/sockets_tester'
                    }
                ]
            }
        }
    }
</script>

<style scoped>
    .myButton {
        background-color:#63b8ee;
        border-radius:1px;
        border:1px solid #3866a3;
        display:inline-block;
        cursor:pointer;
        color:#14396a;
        font-size:15px;
        padding:10px 10px;
        width: 200px;
        height: 10px;
    }

    .myButton:hover {
        background-color:#468ccf;

    }

    .myButton:active {
        position:relative;
        top:1px;
    }

</style>