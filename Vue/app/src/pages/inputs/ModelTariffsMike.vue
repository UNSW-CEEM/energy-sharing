<template>
    <div class="background">
        <div class="main-container">
            <!-- <h1 class="view-title">{{ view_name }}</h1> -->
            
            <div class="container">
                <div class="container-header">
                    Import Component
                </div>
                <div class="container-content">
                    <Chart class="mychart" :options="static_imports_chart_options"></Chart>
                    <div class="slider">
                        <vue-slider v-model="input_data.tariffs.static_imports.tou_times" :process="colorizer" :min="1" :max="24" :interval="1"></vue-slider>
                        <button v-on:click="add_time_period('static_imports')">Add Time Period</button>

                    </div>
                    <div class="tariffs">
                        <div class="input">
                            <div v-for="(tariff, index) in input_data.tariffs.static_imports.period_rates">
                                <span class="units">Period {{index + 1}}</span>
                                <input v-model.number="input_data.tariffs.static_imports.period_rates[index]"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container">
                <div class="container-header">
                    Solar Import Component
                </div>
                <div class="container-content">
                    <Chart class="mychart" :options="static_solar_imports_chart_options"></Chart>
                    <div class="slider">
                        <vue-slider v-model="input_data.tariffs.static_solar_imports.tou_times" :process="colorizer" :min="1" :max="24" :interval="1"></vue-slider>
                        <button v-on:click="add_time_period('static_solar_imports')">Add Time Period</button>

                    </div>
                    <div class="tariffs">
                        <div class="input">
                            <div v-for="(tariff, index) in input_data.tariffs.static_solar_imports.period_rates">
                                <span class="units">Period {{index + 1}}</span>
                                <input v-model.number="input_data.tariffs.static_solar_imports.period_rates[index]"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container">
                <div class="container-header">
                    Export Component
                </div>
                <div class="container-content">
                    <Chart class="mychart" :options="static_exports_chart_options"></Chart>
                    <div class="slider">
                        <vue-slider v-model="input_data.tariffs.static_exports.tou_times" :process="colorizer" :min="1" :max="24" :interval="1"></vue-slider>
                        <button v-on:click="add_time_period('static_exports')">Add Time Period</button>
                    </div>
                    <div class="tariffs">
                        <div class="input">
                            <div v-for="(tariff, index) in input_data.tariffs.static_exports.period_rates">
                                <span class="units">Period {{index + 1}}</span>
                                <input v-model.number="input_data.tariffs.static_exports.period_rates[index]"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container">
                <div class="container-header">
                    Daily Block Tariff Component
                </div>
                <div class="container-content">
                    <div class="tariffs">
                        <div class="input">
                            <div>
                                <span class="units">Block 1 Rate </span>
                                <input v-model.number="input_data.tariffs.block_rate_1"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                        <div class="input">
                            <div>
                                <span class="units">Block 1 Threshold</span>
                                <input v-model.number="input_data.tariffs.high_1"/> 
                                <span class="units">(kWh)</span>
                            </div>
                        </div>
                        <div class="input">
                            <div>
                                <span class="units">Block 2 Rate </span>
                                <input v-model.number="input_data.tariffs.block_rate_2"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                        <div class="input">
                            <div>
                                <span class="units">Block 2 Threshold</span>
                                <input v-model.number="input_data.tariffs.high_2"/> 
                                <span class="units">(kWh)</span>
                            </div>
                        </div>
                        <div class="input">
                            <div>
                                <span class="units">Block 3 Rate </span>
                                <input v-model.number="input_data.tariffs.block_rate_3"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="container">
                <div class="container-header">
                    Metering Service Charge Component
                </div>
                <div class="container-content">
                    <div class="tariffs">
                        <div class="input">
                            <div>
                                <span class="units">Metering Service Charge</span>
                                <input v-model.number="input_data.tariffs.metering_sc_non_cap"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        
        <div class="container">
                <div class="container-header">
                    Solar Component
                </div>
                <div class="container-content">
                    <div class="tariffs">
                        <div class="input">
                            <div>
                                <span class="units">Feed-in Tariff Flat Rate</span>
                                <input v-model.number="input_data.tariffs.fit_flat_rate"/> 
                                <span class="units">($/kWh)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        

        
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';
    import {Chart} from 'highcharts-vue'
    import VueSlider from 'vue-slider-component'
    import 'vue-slider-component/theme/antd.css'


    export default {
        name: "TariffsMike",

        components: {
            SimpleNumberInput,
            SimpleDropdown,
            Chart,
            VueSlider
        },

        mixins: [SaveLoad],

        data () {
            return {

                colorizer(dotsPos){
                    return [
                        [dotsPos[0], dotsPos[1], { backgroundColor: '#15E462' }],
                        [dotsPos[1], dotsPos[2], { backgroundColor: '#1ca6db' }],
                        [dotsPos[2], dotsPos[3], { backgroundColor: '#15E462' }],
                        [dotsPos[3], dotsPos[4], { backgroundColor: '#1ca6db' }],
                        [dotsPos[4], dotsPos[5], { backgroundColor: '#15E462' }],
                        [dotsPos[5], dotsPos[6], { backgroundColor: '#1ca6db' }],
                        [dotsPos[6], dotsPos[7], { backgroundColor: '#15E462' }],
                        [dotsPos[7], dotsPos[8], { backgroundColor: '#1ca6db' }],
                    ]
                },

                view_name: this.$options.name,
                model_page_name: "model_tariffs_mike",

                input_data: {

                    tariffs:{
                        daily_fixed_rate: 1,
                        block_rate_1:0,
                        block_rate_2:0,
                        block_rate_3:0,
                        high_1:1,
                        high_2:2,
                        metering_sc_non_cap: 0,
                        fit_flat_rate:0,
                        
                        static_imports: {
                            tou_times: [7,15],
                            period_rates:[0.2,0.4,0.2],
                            
                        },

                        static_solar_imports:{
                            tou_times: [7,15],
                            period_rates:[0.2,0.4,0.2],
                        },

                        static_exports:{
                            tou_times: [7,15],
                            period_rates:[0.2,0.4,0.2],
                        },

                        
                    },

                    selected_config_file: false,

                    table_rows: [],

                    my_options: {
                        tariff_type_options: [
                            "Retail",
                            "TUOS",
                            "DUOS",
                            "NUOS",
                        ],
                    }
                },

                table_headers: [
                    {header_id: 0, name: "Tariff Type", additional_text:"Select"},
                    {header_id: 1, name: "Tariff Name", additional_text:"Label"},
                    {header_id: 2, name: "Solar FiT", additional_text:"$/kWh"},
                    {header_id: 3, name: "Peak", additional_text:"$/kWh"},
                    {header_id: 4, name: "Shoulder", additional_text:"$/kWh"},
                    {header_id: 5, name: "Off-Peak", additional_text:"$/kWh"},
                ],
            }
        },

        watch:{
            tariffs(){
                this.input_data.tariffs = tariffs;
            }
        },

        mounted(){
            // console.log('CHILDREN',this.$children[0])
            //This is required to make the chart responsive - otherwise we hit the bug that it doesn't fit div size until window resize.
            // this.$children[0].chart.setSize();
        },

        computed:{

            static_imports_chart_options () {
                var data = [];

                for(var hour = 0; hour < 24; hour++){
                    var tariff = null;
                    for (var i = this.input_data.tariffs.static_imports.tou_times.length-1; i >= 0; i--){
                        var tariff_hour = this.input_data.tariffs.static_imports.tou_times[i];
                        if(hour < tariff_hour){
                            tariff = Number(this.input_data.tariffs.static_imports.period_rates[i]);
                        }
                        
                    }
                    if(tariff == null){
                        tariff = tariff = this.input_data.tariffs.static_imports.period_rates[this.input_data.tariffs.static_imports.period_rates.length-1];
                    }
                   
                    data.push(tariff);
                }

                return {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Time of Use Tariff'
                    },
                    subtitle: {
                        text: 'Drag Slider to Adjust Times'
                    },
                    xAxis: {
                        labels:{
                            step:1,
                        },
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: '$/kWh'
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f} $/kWh</b></td></tr>',
                        footerFormat: '</table>',
                        shared: true,
                        useHTML: true
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [{
                        name: 'Retail Tariff',
                        // data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
                        data: data,

                    }]
                }
            },

            static_solar_imports_chart_options () {
                var data = [];

                for(var hour = 0; hour < 24; hour++){
                    var tariff = null;
                    for (var i = this.input_data.tariffs.static_solar_imports.tou_times.length-1; i >= 0; i--){
                        var tariff_hour = this.input_data.tariffs.static_solar_imports.tou_times[i];
                        if(hour < tariff_hour){
                            tariff = Number(this.input_data.tariffs.static_solar_imports.period_rates[i]);
                        }
                        
                    }
                    if(tariff == null){
                        tariff = tariff = this.input_data.tariffs.static_solar_imports.period_rates[this.input_data.tariffs.static_solar_imports.period_rates.length-1];
                    }
                   
                    data.push(tariff);
                }

                return {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Time of Use Tariff'
                    },
                    subtitle: {
                        text: 'Drag Slider to Adjust Times'
                    },
                    xAxis: {
                        labels:{
                            step:1,
                        },
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: '$/kWh'
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f} $/kWh</b></td></tr>',
                        footerFormat: '</table>',
                        shared: true,
                        useHTML: true
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [{
                        name: 'Retail Tariff',
                        // data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
                        data: data,

                    }]
                }
            },

            static_exports_chart_options () {
                var data = [];

                for(var hour = 0; hour < 24; hour++){
                    var tariff = null;
                    for (var i = this.input_data.tariffs.static_exports.tou_times.length-1; i >= 0; i--){
                        var tariff_hour = this.input_data.tariffs.static_exports.tou_times[i];
                        if(hour < tariff_hour){
                            tariff = Number(this.input_data.tariffs.static_exports.period_rates[i]);
                        }
                        
                    }
                    if(tariff == null){
                        tariff = tariff = this.input_data.tariffs.static_exports.period_rates[this.input_data.tariffs.static_exports.period_rates.length-1];
                    }
                   
                    data.push(tariff);
                }

                return {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Time of Use Tariff'
                    },
                    subtitle: {
                        text: 'Drag Slider to Adjust Times'
                    },
                    xAxis: {
                        labels:{
                            step:1,
                        },
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: '$/kWh'
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f} $/kWh</b></td></tr>',
                        footerFormat: '</table>',
                        shared: true,
                        useHTML: true
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [{
                        name: 'Retail Tariff',
                        // data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
                        data: data,

                    }]
                }
            },
            
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            } else {
                console.log('ModelTariffsMike.vue/created() Mike Model Tariffs not in the frontend state object!')
            }
        },

        methods: {
            add_time_period(tariff_type){
                this.input_data.tariffs[tariff_type].tou_times.push(24);
                this.input_data.tariffs[tariff_type].period_rates.push(0);
            },

        },

        sockets: {
            tariffs_file_channel: function(response) {
            console.log("tariffs: ", response);

            }
        }
    }
    
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";

    .noBullets {
        list-style: none;
    }

    .file-buttons-container {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    h1 {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    table {
        animation-name: fade-in;
        animation-duration: 1s;
    }

    .main-container{
        /* overflow:auto; */
    }

    .background{
        overflow:auto;
    }

    .slider{
        padding-left:90px;
        padding-right: 20px;
        margin: 1.5vh 0 1.5vh 0;
    }

    .mychart{
        width:100%;
        margin: 0 auto;
    }

    .tariffs{
        display:flex;
        flex-direction:row;
        justify-content:space-around;
        align-items:center;
        margin: 1.5vh 0 1.5vh 0;
        font-size:0.8em;
        width:100%;
        
    }

    .tariffs .input{
        margin: 1vw 0 1vw 0;
        display:flex;
        flex-direction:row;
        justify-content:space-around;
        align-items:center;
        width:100%;
        flex-wrap: wrap;
    }
    .tariffs .input * {
        padding: 1vh 0 1vh 0;
    }

    .tariffs input{
        width:1.7vw;
        margin-left:0.6vw;
    }

    .tariff-label{
        font-weight: bold;
        padding-right:2vw;
    }

    .container{
        // border: 1px solid grey;
        // border-radius:4px;
        display:flex;
        flex-direction:column;
        justify-content: flex-start;
        align-items:center;
        margin: 3vh 0 3vh 0;
        width:70vw;
        background-color:$container-bg;
        color:$container-text;

        animation-name: fade-in;
        animation-duration: 1s;
    }

    .container-content{
        width:100%;
    }

    .container-header{
        background-color:$heading-bg;
        color:$heading-text;
        width:100%;
        font-size:1.2em;
    }

    .units{
        font-size:0.8em;
        margin-left:0.6vw;
    }

    .key{
        display:flex;
        flex-direction:row;
        justify-content:flex-start;
        align-items:center;
        margin-top:2vh;
    }

    .key .peak{
        background-color:#1ca6db;
        padding: 0.5vh 0.5vw 0.5vh 0.5vw;
        border-radius:4px;
        margin: 0 1vw 0 0;
    }

    .key .shoulder{
        background-color:pink;
        color:grey;
        padding: 0.5vh 0.5vw 0.5vh 0.5vw;
        border-radius:4px;
        margin: 0 1vw 0 0;
    }

    .key .offpeak{
        background-color:white;
        padding: 0.5vh 0.5vw 0.5vh 0.5vw;
        border-radius:4px;
        margin: 0 1vw 0 0;
    }

    
</style>