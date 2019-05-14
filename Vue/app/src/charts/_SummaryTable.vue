<template>
    <div class="summary-container">
        <table>
        <tr class="border_bottom"><th>Item</th> <th>Value</th></tr>
        <tr v-for="(value, name) in parsed_data"><td>{{ name | generate_label}}</td> <td>{{value}}</td></tr>
        </table>
        <div class="spacer">.</div>
    </div>
</template>

<script>

    import BarChart from "./BarChart";

    export default {
        name: "CustomerBills",
        components: {BarChart},
        props: {
            chart_data: {},
            
        },

        data () {
            return {
                parsed_data: false,
                
            }
        },

        methods: {
            parse_data() {
                let data = this.chart_data["scenario_info"];
                this.parsed_data = data;
            },
            
        },

        filters:{
            generate_label(key){
                var labels = {
                    central_battery_SOH:"Central Battery SOH",
                    central_battery_capacity_kWh:"Central Battery Capacity (kWh)",
                    central_battery_cycles: "Central Battery Cycles",
                    checksum_total_payments$:"Total Payments Checksum",
                    cp_ratio: "CP Ratio",
                    eno$_bat_capex_repay:"ENO CAPEX Battery Repayment ($)",
                    eno$_demand_charge: "ENO Demand Charge ($)",
                    eno$_energy_bill: "ENO Energy Bill ($)",
                    eno$_npv_building: "ENO Building NPV",
                    eno$_receipts_from_residents: "ENO Receipts from Residents ($)",
                    eno$_total_payment:"ENO Total Repayment",
                    eno_net$: "ENO Net Dollars ($)",
                    export_kWh:"Export kWh",
                    import_kWh:"Import kWh",
                    pv_ratio: "PV Ratio",
                    retailer_bill$: "Retailer Bill ($)",
                    retailer_receipt$: "Retailer Receipt ($)",
                    'self-consumption':"Self Consumption (kWh)",
                    "self-consumption_OLD":"Self Consumption Older Definition (kWh)",
                    'self-sufficiency': "Self Sufficiency",
                    'self-sufficiency_OLD':"Self Sufficiency (Older Definition)",
                    solar_retailer_profit:"Solar Retailer Profit ($)",
                    total$_building_costs:"Total Building Costs ($)",
                    total_battery_losses: "Total Battery Losses (kWh)",
                    total_building_load: "Total Building Load (kWh)"
                }
                if (key in labels){
                    return labels[key]
                }else{
                    return key;
                }
            }
        },

        mounted () {
            this.parse_data();
        },
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";
    .chart {
        height: 100%;
        width: 100%;
    }

    .summary-container{
        max-height:100%;
        overflow:auto;
        width:100%;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
    }

    th{
        color:$heading-text;
    }
    table{
        background-color:$container-bg;
        margin:2vh 0 0 2vh;
        width:75vw;
    }
    tr {
        color:black;
        /* border:1px solid grey; */
        // background-color:grey;
        // border: 1px solid grey;
    }
    td{
        // border-bottom: 1px solid grey;
    }

    tr.border_bottom td{
        border-bottom: 1px solid grey;
    }

    .spacer{
        color:$bg;
    }
    
</style>