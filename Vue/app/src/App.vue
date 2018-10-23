<template>
    <div id="app">
        <div class="container">
            <TopNavBar class="topnav"/>
            <SideNavBar class="sidenav"/>
            <router-view class="main"/>

            <div class="footer">
                <h4>This Is My Footer</h4>
            </div>

        </div>
    </div>
</template>

<script>
    import SideNavBar from './pages/SideNavBar';
    import TopNavBar from './pages/TopNavBar';
    export default {
        name: 'app',
        components: {
            SideNavBar,
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
        /*color: #2c3e50;*/
    }

    .container {
        display: grid;
        grid-gap: 10px;
        grid-template-columns: repeat(10, 1fr);
        grid-template-rows: 100px 500px 50px;
        height: 100vh;
    }

    .topnav {
        grid-column-start: 1;
        grid-column-end: 11;
        background: #3bbced;
        padding: 20px;
        /*min-width:100vw;*/
    }

    .sidenav {
        grid-column-start: 1;
        grid-column-end: 3;
        background: green;
    }

    .main {
        grid-column-start: 3;
        grid-column-end: 11;
        background: #3bbced;
    }

    .footer {
        grid-column-start: 1;
        grid-column-end: 11;
        background: green;
    }

    .one {
        background: #3bbced;
    }

</style>
