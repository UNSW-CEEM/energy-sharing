<!--FOCUS ON ME AND MY COMPONENTS-->
<template>
    <div>
        <h1>{{ view_name }}</h1>
         <table style="width:100%">
            <tr>
                <th>Name</th>
                <th>kWh</th>
                
            </tr>

            <tr v-for="row in rows">
                <td>{{row.name}}</td>
                <input v-model="row.kWh">
            </tr>

        </table> 
        
        <button v-on:click="add_row()">ADD</button>
    </div>
</template>

<script>

    export default {
        name: "Participants",
        components: {
        },
        methods:{
            add_row(){
                this.rows.push({
                    kWh:2,
                    name:"Luke"
                })
            }
        },
        data () {
            return {
                view_name: this.$options.name,
                rows:[{
                    kWh:1,
                    name:'Luke'
                }],
            }
        }
    }
</script>

<style scoped>

</style>