<template>
    <div>
        <h2>Nav Bar</h2>
        <nav>
            <router-link
                class="spacing"
                v-for="routes in links"
                v-bind:key="routes.id"
                :to="`${routes.page}`">{{ routes.text }}</router-link>
        </nav>
    </div>
</template>

<script>
    export default {
        name: "TopNavBar",
        data () {
            return {
                links: [
                    {
                        id: 0,
                        text: 'Home',
                        page: '/'
                    },
                    {
                        id: 1,
                        text: 'About',
                        page: '/about'
                    },
                    {
                        id: 2,
                        text: 'Contact',
                        page: '/contact'
                    },
                    {
                        id: 3,
                        text: 'Data',
                        page: '/data'
                    },
                    {
                        id: 4,
                        text: 'Model',
                        page: '/model'
                    }
                ]
            }
        }
    }
</script>

<style>
    .spacing {
        Margin-right: 10px;
    }
</style>