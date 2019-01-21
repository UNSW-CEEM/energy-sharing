<template>
    <div id="app">
        <div class="container">
            <TopNavBar class="topnav"/>
            <SideNavBar class="sidenav"/>
            <router-view class="main"/>
            <ModelFooter class="footer"/>
        </div>
    </div>
</template>

<script>
    import SideNavBar from './pages/SideNavBar';
    import TopNavBar from './pages/TopNavBar';
    import ModelFooter from './pages/ModelFooter';

    export default {
        name: 'app',
        components: {
            ModelFooter,
            SideNavBar,
            TopNavBar,
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
    body{
        background-color:#202225;
        color:#cfcfcf;

    }

    select{
        // width: 220px;
        // border: 0;
        // position: relative;
        // z-index: 99;
        
        
    }

    .container {
        display: grid;
        grid-gap: 10px;
        grid-template-columns: repeat(10, 1fr);
        grid-template-rows: 5vh 85vh 5vh;
        // height: 100vh;
        
    }

    .topnav {
        grid-column-start: 1;
        grid-column-end: 11;
        // background-color:blue;
        max-height:30px;
        // background: #3bbced;
        // padding: 20px;
        /*min-width:100vw;*/
        // margin-bottom: 1px solid black;
        
    }

    .sidenav {
        grid-column-start: 1;
        grid-column-end: 3;
        background: rgb(219, 219, 219);
        border-radius:5px;
        background-color:#2F3136;
    }

    .main {
        grid-column-start: 3;
        grid-column-end: 11;
        background: rgb(219, 219, 219);
        border-radius:5px;

        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        background-color: #36393F;
    }

    .footer {
        grid-column-start: 1;
        grid-column-end: 11;
        background: rgb(219, 219, 219);
        border-radius:5px;
        background-color:#2F3136;
    }

    .one {
        background: #3bbced;
    }


    @keyframes fade-in {
        from {
            opacity:0;
        }
        to {
            opacity:1;
        }
    }

</style>
