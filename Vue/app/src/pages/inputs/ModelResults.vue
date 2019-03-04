<template>
    <div class="main-chart-container">
        <div class="chart-menu">
            <router-link
                class="my-route-button"
                v-for="chart in chart_boxes"
                v-bind:key="route.id"
                :to="`${route.page}`"
            > {{ chart.chart_type }} </router-link>
        </div>

        <select v-model="selected_chart">
            <option v-for="chart in chart_boxes" :value="chart"> {{chart.chart_type}} </option>
        </select>
        <div class="sub-chart-container"
             v-if="selected_chart"
             :style="selected_chart.position_styling"
        >
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

                routes: [],

                chart_boxes: [
                    {
                        id: 0,
                        chart_type: 'RevRCC',
                        position_styling: {
                            'grid-column-start': 1,
                            'grid-column-end': 3,
                            'grid-row-start': 1,
                            'grid-row-end': 4,
                        }
                    },
                    {
                        id: 1,
                        chart_type: 'RevParticipant',
                        position_styling: {
                            'grid-column-start': 3,
                            'grid-column-end': 5,
                            'grid-row-start': 1,
                            'grid-row-end': 4,
                        }
                    }
                ],
            }
        },

        sockets: {
            chart_results_channel: function (response) {
                this.chart_data = response.data;
            }
        }
    }
</script>

<style scoped>

    .main-chart-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(3, 1fr);
        grid-column-gap: 20px;
        grid-row-gap: 20px;
    }

    .sub-chart-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

</style>