<template>
    <div class="main-chart-container">
        <div class="chart-nav-container">
            <button
                    class="chart-button"
                    v-for="chart in chart_boxes"
                    v-model="selected_chart"
                    v-on:click="select_chart(chart)"
                    v-bind:class="{selected_button: is_selected(chart)}">{{ chart.link_text }}
            </button>
        </div>

        <div class="sub-chart-container" v-if="selected_chart">
            <TPB
                v-if="selected_chart.chart_type==='TPB' && chart_data"
                :chart_data="chart_data"
            />
            <RevParticipant
                v-if="selected_chart.chart_type==='RevParticipant' && chart_data"
                :chart_data="chart_data"
            />
            <RevRCC
                v-if="selected_chart.chart_type==='RevRCC' && chart_data"
                :chart_data="chart_data"
            />
            <EnergyCC/>
            <EnergyGenCon/>
        </div>

    </div>
</template>

<script>

    import TPB from "../../charts/_TPB";
    import RevParticipant from "../../charts/_RevParticipant";
    import RevRCC from "../../charts/_RevRCC";
    import EnergyCC from "../../charts/_EnergyCC";
    import EnergyGenCon from "../../charts/_EnergyGenCon";

    export default {
        name: "ModelResults",
        components: {EnergyGenCon, EnergyCC, RevRCC, RevParticipant, TPB},

        data () {
            return  {
                chart_data: false,
                selected_chart: false,
                chart_boxes: [
                    {
                        id: 0,
                        link_text: "Revenue - RCC",
                        chart_type: 'RevRCC',
                    },
                    {
                        id: 1,
                        link_text: "Revenue - Participant",
                        chart_type: 'RevParticipant',
                    },
                    {
                        id: 2,
                        link_text: "Revenue - Total Participant",
                        chart_type: 'TPB',
                    },
                    {
                        id: 3,
                        link_text: "Energy - Central",
                        chart_type: 'RevParticipant',
                    },
                    {
                        id: 4,
                        link_text: "Energy - Generated/Consumed",
                        chart_type: 'RevRCC',
                    },
                ],
            }
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
                this.select_chart(this.chart_boxes[0]);
                this.chart_data = response.data;
            }
        }
    }
</script>

<style scoped>

    .main-chart-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
    }

    .chart-nav-container {
        width: 100%;
        height: 5%;
        align-items: center;
        justify-content: center;
        display: flex;
        flex-direction: row;
        background-color:#2F3136;
    }

    .chart-button {
        width: 15%
    }

    .selected_button {
        background-color: blue;
    }

    .sub-chart-container {
        display: flex;
        width: 100%;
        height: 95%;
    }

</style>