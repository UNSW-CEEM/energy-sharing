<template>
    <div class="main-chart-container">
        <!-- <h1>Mike Model Results</h1> -->
        <div class="chart-nav-container">
            <div  class="chart-choice"
                    v-for="chart in input_data.chart_boxes"
                    v-on:click="select_chart(chart)"
                    v-bind:class="{selected_button: is_selected(chart)}"
                    >
                    {{ chart.link_text }}
            </div>
            <div class="chart-choice" ><a :href="download_link">Download</a></div>
        </div>

        <div class="sub-chart-container" v-if="selected_chart">
            <SummaryTable
                v-if="selected_chart.chart_type==='SummaryTable' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />
            <CustomerTotals
                v-if="selected_chart.chart_type==='CustomerTotals' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />
            <CustomerSolarBills
                v-if="selected_chart.chart_type==='CustomerSolarBills' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />
            <CustomerBills
                v-if="selected_chart.chart_type==='CustomerBills' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />
            <!-- <RevParticipant
                v-if="selected_chart.chart_type==='RevParticipant' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />
            <RevRCC
                v-if="selected_chart.chart_type==='RevRCC' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            /> -->
            <!--<EnergyCC-->
                <!--v-if="selected_chart.chart_type==='EnergyCC' && chart_data"-->
                <!--:chart_data="chart_data"-->
            <!--/>-->
            <!-- <EnergyGenCon
                v-if="selected_chart.chart_type==='EnergyGenCon' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            />

            <EnergySystemFlows
                v-if="selected_chart.chart_type==='EnergySystemFlows' && input_data.chart_data"
                :chart_data="input_data.chart_data"
            /> -->
        </div>
    </div>
</template>

<script>

    import TPB from "../../charts/_TPB";
    import RevParticipant from "../../charts/_RevParticipant";
    import RevRCC from "../../charts/_RevRCC";
    import EnergyCC from "../../charts/_EnergyCC";
    import EnergyGenCon from "../../charts/_EnergyGenCon";
    import EnergySystemFlows from "../../charts/_EnergySystemFlows";
    import CustomerTotals from "../../charts/_CustomerTotals";
    import CustomerSolarBills from "../../charts/_CustomerSolarBills";
    import CustomerBills from "../../charts/_CustomerBills";
    import SummaryTable from "../../charts/_SummaryTable";
    import moment from 'moment'

    import SaveLoad from '@/mixins/SaveLoad.vue';

    export default {
        name: "ModelResultsMike",
        components: {EnergyGenCon, EnergyCC, RevRCC, RevParticipant, TPB, EnergySystemFlows, CustomerTotals, CustomerSolarBills, CustomerBills, SummaryTable},

        mixins: [SaveLoad],

        computed:{
            download_link(){
                return "http://localhost:5000/download/mike?time="+moment().format();
            }
        },

        data () {
            return  {
                model_page_name: "model_results_mike",
                selected_chart: false,
                
                input_data: {
                    chart_data: false,
                    // selected_chart: false,
                    chart_boxes: [
                        {
                            id: 0,
                            link_text: "Summary Table",
                            chart_type: 'SummaryTable',
                        },
                        {
                            id: 1,
                            link_text: "Customer Totals",
                            chart_type: 'CustomerTotals',
                        },
                        {
                            id: 2,
                            link_text: "Customer Solar Bills",
                            chart_type: 'CustomerSolarBills',
                        },
                        {
                            id: 3,
                            link_text: "Customer Bills",
                            chart_type: 'CustomerBills',
                        },
                        // {
                        //     id: 1,
                        //     link_text: "Bill - Participant",
                        //     chart_type: 'RevParticipant',
                        // },
                        // {
                        //     id: 2,
                        //     link_text: "Revenue - Total Participant",
                        //     chart_type: 'TPB',
                        // },
                        // {
                        //     id: 3,
                        //     link_text: "Energy - Central",
                        //     chart_type: 'EnergyCC',
                        // },
                        // {
                        //     id: 3,
                        //     link_text: "Energy - Generated/Consumed",
                        //     chart_type: 'EnergyGenCon',
                        // },
                        // {
                        //     id: 4,
                        //     link_text: "Energy - System Flows",
                        //     chart_type: 'EnergySystemFlows',
                        // },
                    ],
                },
            }
        },

        created() {
            this.load_page_simple();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        methods: {
            select_chart(chart) {
                this.selected_chart = chart;
            },

            is_selected(chart) {
                if (this.selected_chart===chart) {
                    return true;
                }
                return false;
            }
        },

        sockets: {
            chart_results_channel: function (response) {
                this.select_chart(this.input_data.chart_boxes[0]);
                this.input_data.chart_data = response.data;
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";
    .main-chart-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        max-width:80vw;
    }

    .chart-nav-container {
        width: 100%;
        height: 10vh;
        align-items: center;
        justify-content: center;
        display: flex;
        flex-direction: row;
        
        // background-color:green;
    }

    .chart-choice {
        /* width: 15%; */
        background-color:grey;
        // margin: 1vh 1vw 1vh 1vw;
        cursor:pointer;
        padding: 0vh 1vw 0vh 1vw;
        // border-radius:4px;
        width:100%;
        height:100%;
        border-right: 1px solid $bg;
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
    }



    a{
        text-decoration: none;
        color:white;
    }

    a:visited{
        color:#cfcfcf;
    }

    .selected_button {
        background-color: #42464D;
        color: white;
    }

    .sub-chart-container {
        display: flex;
        width: 100%;
        height: 95%;
    }

</style>