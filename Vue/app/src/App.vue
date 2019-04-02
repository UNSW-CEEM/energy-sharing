<template>
    <div id="app">
        <TopNavBar class="topnav"/>
        <div class="main-content">
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
    import 'typeface-ubuntu/index.css'
    
    import 'typeface-muli/index.css' 
    import 'typeface-abel/index.css' 
    import 'typeface-maven-pro/index.css' 
    import 'typeface-cantarell/index.css' 
    import 'typeface-concert-one/index.css' 
    import 'typeface-orbitron/index.css' 
    import 'typeface-russo-one/index.css' 
    import 'typeface-armata/index.css' 
    import 'typeface-montserrat-alternates/index.css' 

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

<style lang="scss">
    
    @import "./src/variables.scss";
    body{
        background-color: $bg;
        color: $text;
        margin: 0 0 0 0;
    }
    
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        // font-family: 'Armata', sans-serif;
        // font-family: 'Ubuntu', sans-serif;

        // font-family: 'Muli', sans-serif;
        // font-family: 'Maven Pro', sans-serif;
        // font-family: 'Cantarell', sans-serif;
        
        // font-family: 'Orbitron', sans-serif;
        
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        
        color:#E9E9E9;
        margin: 0 0 0 0;
        
    }
    

    .main-content {
        display: flex;
        flex-direction:row;
        height:95vh;
    }

    

    .topnav {
        height:5vh;
        background-color:$nav-bg;
    }

    .sidenav {
        
        // border-radius:5px;
        background-color:$nav-bg;
        width:20vw;
    }

    .main {
        width:80vw;
        background: rgb(219, 219, 219);
        
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        // background-color: #36393F;
        background-color:#2F323A;
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
