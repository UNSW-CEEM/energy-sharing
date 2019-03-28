<template>
    <div class="background">
        <div class="main-container">
            <h1 class="view-title">{{ view_name }}</h1>
            <!-- <p>Beta Note: 'Luomi' model requires one of each tariff completed. (DUOS, NUOS, TUOS and Retail)</p> -->
            
            <div class="container">
                <div class="container-header">
                    Retail Tariffs
                </div>
                <div class="container-content">
                    <Chart class="mychart" :options="retailChartOptions"></Chart>
                    <div class="slider">
                        <vue-slider v-model="input_data.tariffs.tou_times" :process="colorizer" :min="1" :max="24" :interval="1"></vue-slider>
                    </div>

                    <div class="tariffs">
                        <div class="input">
                            Off-Peak Tariff <input v-model="input_data.tariffs.retail.off_peak_tariff"/>
                        </div>
                        <div class="input">
                            Shoulder Tariff <input v-model="input_data.tariffs.retail.shoulder_tariff"/>
                        </div>
                        <div class="input">
                            Peak Tariff <input v-model="input_data.tariffs.retail.peak_tariff"/>
                        </div>
                    </div>
                
                </div>
            </div>

            <div class="container">
                <div class="container-header">
                    Network Tariffs
                </div>
                <div class="container-content">
                    <Chart class="mychart" :options="networkChartOptions"></Chart>
                    <div class="slider">
                        <vue-slider v-model="input_data.tariffs.tou_times" :process="colorizer" :min="1" :max="24" :interval="1"></vue-slider>
                    </div>

                    <div class="tariffs">
                        <div class="tariff-label">TUOS</div>
                        <div class="input">
                            Off-Peak Tariff <input v-model="input_data.tariffs.tuos.off_peak_tariff"/>
                        </div>
                        <div class="input">
                            Shoulder Tariff <input v-model="input_data.tariffs.tuos.shoulder_tariff"/>
                        </div>
                        <div class="input">
                            Peak Tariff <input v-model="input_data.tariffs.tuos.peak_tariff"/>
                        </div>
                    </div>
                    <div class="tariffs">
                        <div class="tariff-label">DUOS</div>
                        <div class="input">
                            Off-Peak Tariff <input v-model="input_data.tariffs.duos.off_peak_tariff"/>
                        </div>
                        <div class="input">
                            Shoulder Tariff <input v-model="input_data.tariffs.duos.shoulder_tariff"/>
                        </div>
                        <div class="input">
                            Peak Tariff <input v-model="input_data.tariffs.duos.peak_tariff"/>
                        </div>
                    </div>
                    <div class="tariffs">
                        <div class="tariff-label">NUOS</div>
                        <div class="input">
                            Off-Peak Tariff <input v-model="input_data.tariffs.nuos.off_peak_tariff"/>
                        </div>
                        <div class="input">
                            Shoulder Tariff <input v-model="input_data.tariffs.nuos.shoulder_tariff"/>
                        </div>
                        <div class="input">
                            Peak Tariff <input v-model="input_data.tariffs.nuos.peak_tariff"/>
                        </div>
                    </div>

                </div>
            </div>

            <table class="tariffs-table">
                <tr>
                    <th v-for="header in table_headers" :key="header.header_id" :value="header.name">
                        {{ header.name }}
                    </th>
                </tr>
                <tr>
                    <td v-for="header in table_headers" :key="header.header_id">
                        {{ header.additional_text }}
                    </td>
                </tr>
                <tr v-for="row in input_data.table_rows" :key="row.row_id">
                    <td v-for="input in row.row_inputs" :key="input.col_id">
                        <SimpleNumberInput
                            v-if="input.tag==='my_number'"
                            v-model="input.value"
                            :my_placeholder="input.placeholder"/>
                        <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                            v-model="input.value"
                            :my_options="input_data.my_options[input.dropdown_key]"
                            :my_placeholder="input.placeholder"/>
                    </td>
                    <!--<td><button>Remove Row</button></td>-->
                </tr>
            </table>
            <button @click="add_row()">Add Row</button>

            <div class="file-buttons-container">
                <!--<button @click="load_config(input_data.selected_config_file)" v-if="input_data.selected_config_file">-->
                    <!--Load User Config-->
                <!--</button>-->
                <!--<button @click="save_config('user_config.csv')">Save User Config</button>-->
                <button @click="load_config('default_config.csv')">Load Default</button>
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
        name: "Tariffs",

        components: {
            SimpleNumberInput,
            SimpleDropdown,
            Chart,
            VueSlider
        },

        mixins: [SaveLoad],

        data () {
            return {

                
                
                
                colorizer: dotsPos => [
                    [dotsPos[0], dotsPos[1], { backgroundColor: 'pink' }],
                    [dotsPos[1], dotsPos[2], { backgroundColor: 'blue' }],
                    [dotsPos[2], dotsPos[3], { backgroundColor: 'pink' }],
                ],

                view_name: this.$options.name,
                model_page_name: "model_tariffs",

                input_data: {


                    tariffs:{
                        local_solar:{
                            energy:0, //Not UI Implemented
                            retail:0, //Not UI Implemented
                            duos:0, //Not UI Implemented
                            tuos:0, //Not UI Implemented
                        },
                        central_battery:{
                            local_solar_import_energy:0,//Not UI Implemented
                            local_solar_import_retail:0,//Not UI Implemented
                            local_solar_import_duos:0,//Not UI Implemented
                            local_solar_import_tuos:0,//Not UI Implemented
                            local_solar_import_nuos:0,//Not UI Implemented
                            energy:0, //Not UI Implemented
                            retail:0, //Not UI Implemented
                            duos:0, //Not UI Implemented
                            nuos:0, //Not UI Implemented
                            profit:0, //Not UI Implemented
                            tuos:0,//Not UI Implemented

                        },
                        feed_in_tariff:{
                            energy:0, //Not UI Implemented
                            
                        },
                        retail:{
                            peak_tariff: 0.3,
                            shoulder_tariff: 0.2,
                            off_peak_tariff:0.1,
                            block_1_tariff:0, //Not UI Implemented
                            block_2_tariff:0, //NOT UI Implemented
                            block_1_volume:0, //Not UI Implemented
                            block_2_volume:0, //Not UI Implemented
                            daily_charge:0, //Not UI Implemented
                            tou_weekday_only:false, //Not UI Implemented and needs backend check. Leave false for now.
                        },

                        tuos:{
                            peak_tariff: 0.2,
                            shoulder_tariff: 0.1,
                            off_peak_tariff:0.1,
                            daily_charge:0, // Not UI Implemented
                            demand_charge: 0, // Not UI Implemented
                            tou_weekday_only:false, //Not UI Implemented and needs backend check. Leave false for now.
                        },

                        duos:{
                            peak_tariff: 0.4,
                            shoulder_tariff: 0.3,
                            off_peak_tariff:0.1,
                            daily_charge:0, // Not UI Implemented
                            demand_charge:0, // Not UI Implemented
                            tou_weekday_only:false, // Not UI Implemented and needs backend check. Leave false for now.
                        },

                        nuos:{
                            peak_tariff: 0.5,
                            shoulder_tariff: 0.1,
                            off_peak_tariff:0.1,
                            demand_charge:0, // Not UI Implemented
                            daily_charge:0, //Not UI Implemented
                            tou_weekday_only:false, // Not UI Implemented and needs backend check. Leave false for now.
                        },

                        tou_times: [7, 11, 15,18],
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

            shoulder_1_times(){
                return {
                    start: this.input_data.tariffs.tou_times[0],
                    end: this.input_data.tariffs.tou_times[1]
                }
            },
            peak_times(){
                return {
                    start:this.input_data.tariffs.tou_times[1],
                    end:this.input_data.tariffs.tou_times[2]
                }
            },
            shoulder_2_times(){
                return {
                    start: this.input_data.tariffs.tou_times[2],
                    end: this.input_data.tariffs.tou_times[3]
                }
            },

            retailChartOptions () {
                var data = [];

                for(var hour = 0; hour < 24; hour++){
                    var tariff = Number(this.input_data.tariffs.retail.off_peak_tariff);
                    // If it's in the shoulder 1 range, set tariff appropriately. 
                    if(hour >= this.shoulder_1_times.start && hour < this.shoulder_1_times.end){
                        tariff = Number(this.input_data.tariffs.retail.shoulder_tariff);
                    }
                    // If it's in the shoulder 2 range, set tariff appropriately. 
                    if(hour >= this.shoulder_2_times.start && hour < this.shoulder_2_times.end){
                        tariff = Number(this.input_data.tariffs.retail.shoulder_tariff);
                    }
                    if(hour >= this.peak_times.start && hour < this.peak_times.end){
                        tariff = Number(this.input_data.tariffs.retail.peak_tariff);
                    }
                    data.push(tariff);
                }

                return {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Retail Time of Use Tariff'
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
                        name: 'Network Tariff',
                        // data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
                        data: data,

                    }]
                }
            },
            networkChartOptions () {
                var tuos = [];
                var duos = [];
                var nuos = [];

                for(var hour = 0; hour < 24; hour++){
                    var tuos_tariff = Number(this.input_data.tariffs.tuos.off_peak_tariff);
                    var duos_tariff = Number(this.input_data.tariffs.duos.off_peak_tariff);
                    var nuos_tariff = Number(this.input_data.tariffs.nuos.off_peak_tariff);
                    
                    // If it's in the shoulder 1 range, set tariff appropriately. 
                    if(hour >= this.shoulder_1_times.start && hour < this.shoulder_1_times.end){
                        tuos_tariff = Number(this.input_data.tariffs.tuos.shoulder_tariff);
                        duos_tariff = Number(this.input_data.tariffs.duos.shoulder_tariff);
                        nuos_tariff = Number(this.input_data.tariffs.nuos.shoulder_tariff);
                    }
                    // If it's in the shoulder 2 range, set tariff appropriately. 
                    if(hour >= this.shoulder_2_times.start && hour < this.shoulder_2_times.end){
                        tuos_tariff = Number(this.input_data.tariffs.tuos.shoulder_tariff);
                        duos_tariff = Number(this.input_data.tariffs.duos.shoulder_tariff);
                        nuos_tariff = Number(this.input_data.tariffs.nuos.shoulder_tariff);
                    }
                    if(hour >= this.peak_times.start && hour < this.peak_times.end){
                        tuos_tariff = Number(this.input_data.tariffs.tuos.peak_tariff);
                        duos_tariff = Number(this.input_data.tariffs.duos.peak_tariff);
                        nuos_tariff = Number(this.input_data.tariffs.nuos.peak_tariff);
                    }
                    tuos.push(tuos_tariff);
                    duos.push(duos_tariff);
                    nuos.push(nuos_tariff);
                }

                return {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Network Time of Use Tariff'
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
                    series: [
                        {
                        name: 'TUOS',
                        data: tuos,
                        },
                        {
                        name: 'DUOS',
                        data: duos,
                        },
                        {
                        name: 'NUOS',
                        data: nuos,
                        },
                    ]
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
                this.load_config('default_config.csv')
            }
        },

        methods: {
            add_row(tariff_type="", tariff_name="", fit_input="", peak_charge="", shoulder_charge="", offpeak_charge="") {

                let array_length = this.input_data.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            col_id: 0,
                            name:"tariff_type",
                            tag:"my_dropdown",
                            dropdown_key: "tariff_type_options",
                            value: tariff_type,
                            placeholder:"Select Tariff Type",
                        },
                        {
                            col_id: 1,
                            name:"tariff_name",
                            tag:"my_number",
                            value: tariff_name,
                            placeholder:"Name",
                        },
                        {
                            col_id: 2,
                            name:"fit_input",
                            tag:"my_number",
                            value: fit_input,
                            placeholder:"$"
                        },
                        {
                            col_id: 3,
                            name:"peak_charge",
                            tag:"my_number",
                            value: peak_charge,
                            placeholder:"$",
                        },
                        {
                            col_id: 4,
                            name:"shoulder_charge",
                            tag:"my_number",
                            value: shoulder_charge,
                            placeholder:"$",
                        },
                        {
                            col_id: 5,
                            name:"offpeak_charge",
                            tag:"my_number",
                            value: offpeak_charge,
                            placeholder:"$",
                        },
                    ]
                };

                this.input_data.table_rows.push(new_row);
            },

            load_config(filename) {
                this.$socket.emit('load_config', this.model_page_name, filename)
            },

            save_config(filename) {
                this.input_data.selected_config_file = filename
                // this.save_page_simple();
                // let created_data = this.create_config_file(this.model_page_name);
                // let payload = {
                //     model_page_name: this.model_page_name,
                //     data: created_data,
                // };
                //
                // this.$socket.emit('save_config', this.model_page_name, this.selected_config_file, payload)
            }
        },

        sockets: {
            tariffs_file_channel: function(response) {
                console.log("tariffs: ", response);

                this.input_data.table_rows = [];
                for (let i = 0; i < response.length; i++) {
                    let params = response[i]["row_inputs"];
                    this.add_row(
                        params["tariff_type"],
                        params["tariff_name"],
                        params["fit_input"],
                        params["peak_charge"],
                        params["shoulder_charge"],
                        params["offpeak_charge"],
                    );
                }
            }
        }
    }
</script>

<style scoped>
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
    }

    .tariffs .input{
        margin: 1vw 0 1vw 0;
    }

    .tariff-label{
        font-weight: bold;
        padding-right:2vw;
        
    }

    .container{
        border: 1px solid grey;
        border-radius:4px;
        display:flex;
        flex-direction:column;
        justify-content: flex-start;
        align-items:center;
        margin: 3vh 0 3vh 0;
        /* background-color:grey; */
    }

    .container-header{
        background-color:grey;
        width:100%;
    }

    
</style>