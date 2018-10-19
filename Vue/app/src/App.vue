<template>
    <div id="app">
        <h1>Energy Sharing</h1>
        <TopNavBar/>
        <router-view/>
    </div>
</template>

<script>
    import TopNavBar from './pages/TopNavBar'
    export default {
        name: 'app',
        components: {
            TopNavBar
        },
        data () {
            return  {

            }
        },
    }
</script>

<style lang="less">
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #nav {
        padding: 30px;
        a {
            font-weight: bold;
            color: #2c3e50;
            &.router-link-exact-active {
                color: #42b983;
            }
        }
    }
</style>
