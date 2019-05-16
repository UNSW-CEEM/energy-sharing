<template>
    <div class="content">
        <div class="heading">Battery Info</div>
        <table class="battery-table">
            <tr class="row">
            <th>Battery ID</th><th>Capacity (kWh)</th><th>Max Charge kW</th><th>Cycle Efficiency</th><th>Max DoD</th><th>Max SoC</th><th>Max Cycles</th><th>Cost</th>
            </tr>
            <tr class="row"><td>pw_26</td><td>26</td><td>9.848</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>26000</td></tr>
            <tr class="row"><td>pw_52</td><td>52</td><td>19.697</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>52000</td></tr>
            <tr class="row"><td>pw_78</td><td>78</td><td>29.545</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>78000</td></tr>
            <tr class="row"><td>pw_104</td><td>104</td><td>39.394</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>104000</td></tr>
            <tr class="row"><td>pw_scale</td><td>1</td><td>0.378787879</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td></tr>
            <tr class="row"><td>powerwall2_1</td><td>13.2</td><td>5</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>12500</td></tr>
            <tr class="row"><td>powerwall2_2</td><td>26.4</td><td>10</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>24000</td></tr>
            <tr class="row"><td>powerwall2_3</td><td>39.6</td><td>15</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>34500</td></tr>
            <tr class="row"><td>powerwall2_4</td><td>52.8</td><td>20</td><td>0.89</td><td>1</td><td>0.9</td><td>7300</td><td>45000</td></tr>
        </table>
    </div>
</template>

<script>
    import { required } from 'vuelidate/lib/validators';

    export default {
        name: "BatteryInfo",
        props: [],

        data () {
            return {

            }
        }
    }
</script>

<style lang="scss" scoped>

@import "./src/variables.scss";

.content{
    width:100%;
    height:100%;
    display:flex;
    flex-direction:column;
    justify-content: space-around;
    align-items: center;
    color:$container-text;
    
}



.battery-table{
    width:90%;
}

.heading{
    font-size:1.5em;
    font-weight:bold;
    color:$heading-text;
}


</style>