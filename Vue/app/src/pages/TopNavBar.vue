<template>
    <div>
        <span>
            <p>Energy Sharing</p>
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