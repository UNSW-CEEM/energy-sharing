<template>
    <div class="background">
        <!-- <div class="view-title">{{ view_name}}</div> -->
        
        <div class="main-container">
            
            
            <div class="config-info">
                <div class="config-heading">Input Data</div>
                <div class="config-content">
                    <div class="config-selected">
                        <span>Selected Load File: {{input_data.selected_load_file}}</span>
                        <span>Selected Solar File: {{input_data.selected_solar_file}}</span>
                    </div>
                    <div class="config-button" v-on:click="show()">Configure Data Sources </div>
                </div>
            </div>

            
            
            <div class="participants-table">
                <div class="participants-table-heading">Participants</div>
                <table >
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
                    <tr v-for="(row, index) in input_data.table_rows" :key="row.row_id">
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
                        
                        <td><div class="show-data-button" v-on:click="show_chart(row.row_id)">Show Data</div></td>
                        <td><div class="remove-row-button" v-on:click="remove_row(index);">Remove</div></td>
                    </tr>
                </table>


                <div class="add-participant-button" @click="add_row()">Add New Participant</div>

                <!-- <div class="file-buttons-container">
                    <button @click="load_participants_config(input_data.selected_config_file)">Load User Config</button>
                    <button @click="save_config()">Save User Config</button>
                    <button @click="load_participants_config('default_config.csv')">Load from default file</button>
                </div> -->
                
            </div>
            
        </div>

        <modal  width="80%" height="70%" name="data-files">
                <div class="modal-container">
                    <div class="modal-header">
                        Select Solar and Load Files
                    </div>
                    <div class="files-select-container">
                        <h4 class="load-title">Load File:</h4>
                        <SimpleDropdown
                                v-model="input_data.selected_load_file"
                                v-on:input="get_load_profiles(input_data.selected_load_file)"
                                :my_options="input_data.load_files_list"
                                :my_placeholder="'Select File'"/>

                        <h4 class="solar-title">Solar File:</h4>
                        <SimpleDropdown
                                v-model="input_data.selected_solar_file"
                                v-on:input="get_solar_profiles(input_data.selected_solar_file)"
                                :my_options="input_data.solar_files_list"
                                :my_placeholder="'Select File'" />
                        
                    </div>
                    <div class="dates"  >
                        <DateRange v-if="input_data.selected_solar_file && input_data.selected_load_file"
                            :load_start_date="input_data.load_dates[input_data.selected_load_file]['start_date']"
                            :load_end_date="input_data.load_dates[input_data.selected_load_file]['end_date']"
                            :solar_start_date="input_data.solar_dates[input_data.selected_solar_file]['start_date']"
                            :solar_end_date="input_data.solar_dates[input_data.selected_solar_file]['end_date']"
                            :solar_filename="input_data.selected_solar_file"
                            :load_filename="input_data.selected_load_file"
                            ></DateRange>
                        <!-- <span v-if="input_data.selected_solar_file">Solar Start Date:{{input_data.solar_dates[input_data.selected_solar_file]['start_date']}}</span>
                        <span v-if="input_data.selected_solar_file">Solar End Date:{{input_data.solar_dates[input_data.selected_solar_file]['end_date']}}</span>
                        <span v-if="input_data.selected_load_file">Load Start Date:{{input_data.load_dates[input_data.selected_load_file]['start_date']}}</span>
                        <span v-if="input_data.selected_load_file">Load End Date:{{input_data.load_dates[input_data.selected_load_file]['end_date']}}</span> -->
                    </div>
                    <div class="modal-close-buttons">
                        <div class="close-button" v-on:click="hide">Set</div>
                        <div class="close-autofill-button" v-on:click="hide(); auto_fill();">Set and Autofill</div>
                    </div>
                </div>
            </modal>
            
            <!-- MODAL - Participant Load & Solar Data -->
            <modal name="participant-chart" height="60%"  width="80%">
                <Chart class="mychart" :options="chartOptions"></Chart>
            </modal>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import DateRange from '@/components/DateRange.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';
    import {Chart} from 'highcharts-vue'
    export default {
        name: "Participants",

        components: {
            SimpleNumberInput,
            SimpleDropdown,
            DateRange,
            Chart,
        },

        mixins: [SaveLoad],

        data () {
            return {
                view_name: this.$options.name,
                model_page_name:"model_participants",
                chart:{
                    solar_participant_id: null,
                    load_participant_id: null,
                    solar_scaling_factor:1,
                    solar_timeseries:{},
                    load_timeseries:{},
                },

                input_data: {
                    
                    selected_solar_file: '',
                    selected_load_file: '',
                    selected_config_file: 'user_config.csv',

                    solar_files_list: [],
                    load_files_list: [],
                    
                    solar_dates:{},
                    load_dates:{},

                    table_rows: [],

                    my_options: {
                        participant_type_options: [
                            "Solar & Load",
                            "Load",
                            "solar",
                        ],

                        tariff_type_options: [
                            "TOU",
                            // "TOU + Block",
                        ],

                        battery_options: [
                            "No Battery",
                            "Tesla PowerWall",
                            "RedFlow",
                            "Central Battery"
                        ],

                        solar_profiles_options: [],
                        load_profiles_options: [],
                    },

                },

                table_headers: [
                    {id: 0, name: "Participant ID", additional_text:"ID"},
                    // {id: 1, name: "Participant Type", additional_text:"Type"},
                    {id: 2, name: "Tariff Type", additional_text:"Select One"},
                    {id: 3, name: "Load Data", additional_text:"Select One"},
                    {id: 4, name: "Solar Data", additional_text:"Select One"},
                    {id: 5, name: "Solar Scaling", additional_text:"Input Number"},
                    // {id: 6, name: "Battery", additional_text:"Select One"},
                ],
            }
        },

        computed:{
            chartOptions () {

                var solar_data = [];
                var load_data = [];
                // console.log('Chart load timeseries', this.chart.load_timeseries)
                console.log('Solar scaling Factor', this.chart.solar_scaling_factor)
                
                console.log('CHART',this.chart.solar_participant_id, this.chart.load_participant_id);
                if(this.chart.solar_participant_id != null){
                    // solar_data = this.chart.solar_timeseries[this.chart.solar_participant_id].slice()

                    for(var i = 0; i<this.chart.solar_timeseries[this.chart.solar_participant_id].length; i++){
                        solar_data.push(
                                [
                                    this.chart.solar_timeseries[this.chart.solar_participant_id][i][0],
                                    this.chart.solar_timeseries[this.chart.solar_participant_id][i][1] * this.chart.solar_scaling_factor,
                                ]
                            )
                        // solar_data[i][1] = solar_data[i][1] * this.chart.solar_scaling_factor;
                    }
                    // console.log('Chart solar data', solar_data)
                }

                if(this.chart.load_participant_id != null){
                    load_data = this.chart.load_timeseries[this.chart.load_participant_id]
                    // console.log('Chart load data', load_data);
                }

                

                
                

                return {
                    chart: {
                    zoomType: 'x'
                    },
                    title: {
                    text: 'Solar and Load'
                    },
                    width: null,

                    subtitle: {
                    text: document.ontouchstart === undefined
                        ? 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    yAxis: {
                    title: {
                        text: 'kWh'
                    }
                    },
                    legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                    },
                    xAxis: {
                    type: 'datetime'
                    },
                    series: [
                        {
                            name: 'PV',
                            data:solar_data,
                        },
                        {
                            name: 'Load',
                            data: load_data,
                        },

                    ]
                }
            },
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name];
            } else {
                this.add_row()
            }
            this.get_solar_files();
            this.get_load_files();
        },

        beforeDestroy() {
            this.save_page_simple();
        },

        mounted(){
            if(this.input_data.selected_load_file != ""){
                this.get_load_profiles(this.input_data.selected_load_file);
            }
            if(this.input_data.selected_solar_file != ""){
                this.get_solar_profiles(this.input_data.selected_solar_file);
            }
        },

        methods: {
            remove_row(index){
                this.input_data.table_rows.splice(index,1);
            },
            
            auto_fill(){
                if(this.input_data.selected_load_file != "" && this.input_data.selected_solar_file != ""){
                    var solar_profiles = this.input_data.my_options.solar_profiles_options;
                    var load_profiles = this.input_data.my_options.load_profiles_options;
                    this.input_data.table_rows = [];
                    for(var i = 0; i< Math.min(solar_profiles.length, load_profiles.length); i++){
                        this.add_row("Participant "+(i+1), "", "TOU", load_profiles[i], solar_profiles[i],1)
                    }
                }
            },
           
            add_row(participant_id=null, participant_type="", retail_tariff_type="", load_profile="", solar_profile="", solar_scaling=1, battery_type="No Battery") {
                let array_length = this.input_data.table_rows.length;
                if(participant_id == null){
                    var participant_num = array_length + 1
                    participant_id = "Participant "+ participant_num
                }
                // let participant_default = "participant_" + Number(array_length+1).toString();
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            id: 0,
                            name: "participant_id",
                            tag: "my_number",
                            value:participant_id,
                            placeholder:participant_id,
                        },
                        // {
                        //     id: 1,
                        //     name: "participant_type",
                        //     tag: "my_dropdown",
                        //     value:participant_type,
                        //     dropdown_key: "participant_type_options",
                        //     placeholder:"Type",
                        // },
                        {
                            id: 2,
                            name: "retail_tariff_type",
                            tag: "my_dropdown",
                            value:retail_tariff_type,
                            dropdown_key:"tariff_type_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 3,
                            name: "load_profile",
                            tag: "my_dropdown",
                            value:load_profile,
                            dropdown_key:"load_profiles_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 4,
                            name: "solar_profile",
                            tag: "my_dropdown",
                            value:solar_profile,
                            dropdown_key:"solar_profiles_options",
                            placeholder:"Select One",
                        },
                        {
                            id: 5,
                            name: "solar_scaling",
                            tag: "my_number",
                            value:solar_scaling,
                            placeholder:"Input Number",
                        },
                        // {
                        //     id: 6,
                        //     name: "battery_type",
                        //     tag: "my_dropdown",
                        //     value:battery_type,
                        //     dropdown_key:"battery_options",
                        //     placeholder:"Select Battery",
                        // },
                    ]
                };

                this.input_data.table_rows.push(new_row);
            },

            get_solar_files() {
                this.$socket.emit('get_solar_files')
                this.$socket.emit('get_solar_dates')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
                this.$socket.emit('get_load_dates')
            },

            get_solar_profiles (filename) {
                this.$socket.emit('get_solar_profiles', filename)
                this.$socket.emit('get_solar_timeseries', filename);
                console.log('Getting solar profiles')
            },

            get_load_profiles (filename) {
                this.$socket.emit('get_load_profiles', filename);
                this.$socket.emit('get_load_timeseries', filename);
                console.log('Getting load profiles')
            },

            save_config() {
                console.log("Re-implement Me");
            },

            load_participants_config(file) {
                this.$socket.emit('load_participants_config', this.model_page_name, file)
                this.input_data.table_rows = [];
            },
            show(){
                //modal is a plugin found here: https://www.npmjs.com/package/vue-js-modal
                this.$modal.show('data-files');
            },
            hide(){
                this.$modal.hide('data-files');
            },

            show_chart(id){
                
                console.log('Show Data:', id);
                var inputs = this.input_data.table_rows[id].row_inputs;
                var solar_participant_id = null;
                var load_participant_id = null;
                var solar_scaling_factor = 1;
                // Go through all table values, find the corresponding selected solar and load profile names.
                
                for(var i = 0; i< inputs.length; i++){
                    console.log(inputs[i].name)
                    if(inputs[i].name == "load_profile"){
                        
                        load_participant_id = inputs[i].value;
                    }
                    if(inputs[i].name == "solar_profile"){
                        
                        solar_participant_id = inputs[i].value;
                    }
                    if(inputs[i].name == "solar_scaling"){
                        
                        solar_scaling_factor = inputs[i].value;
                    }
                }
                console.log('Selected load and solar profiles:', solar_participant_id, load_participant_id)
                this.chart.solar_participant_id = solar_participant_id;
                this.chart.load_participant_id = load_participant_id;
                this.chart.solar_scaling_factor = solar_scaling_factor;
                this.$modal.show('participant-chart');
            },

            hide_chart(){
                this.$modal.hide('participant-chart');
            }

        },

        sockets: {
            filesChannel: function(response) {
                 if (response.key === 'solar_files_list') {
                    this.input_data.solar_files_list = response.data;
                } else if(response.key == 'load_files_list') {
                    this.input_data.load_files_list = response.data;
                }else if(response.key=='solar_dates'){
                    console.log('Solar Dates:', response.data);
                    this.input_data.solar_dates = response.data;
                }else if( response.key== 'load_dates'){
                    console.log('Load Dates:', response.data)
                    this.input_data.load_dates = response.data;
                }else if(response.key == 'solar_timeseries'){
                    this.chart.solar_timeseries = response.data;
                    console.log('solar timeseries', response.data)
                }else if(response.key == 'load_timeseries'){
                    console.log('load timeseries', response.data);
                    this.chart.load_timeseries = response.data;
                }else{
                    console.log('Unknown incoming key:', response.data);
                }
            },

            profilesChannel: function(response) {
                console.log('profiles',response)
                this.input_data.my_options[response.key] = response.data;
            },

            participants_file_channel: function(response) {
                this.input_data.table_rows = [];
                this.input_data.selected_solar_file = response["data"][0]["row_inputs"]["selected_solar_file"];
                this.input_data.selected_load_file = response["data"][0]["row_inputs"]["selected_load_file"];

                this.get_solar_profiles(this.input_data.selected_solar_file);
                this.get_load_profiles(this.import_data.selected_load_file);

                this.input_data.my_options["solar_profiles_options"] = response["solar_profiles_options"];
                this.input_data.my_options["load_profiles_options"] = response["load_profiles_options"];

                for (let i = 0; i < response["data"].length; i++) {
                    let data = response["data"][i]["row_inputs"];
                    this.add_row(
                        data["participant_id"],
                        data["participant_type"],
                        data["retail_tariff_type"],
                        data["load_profile"],
                        data["solar_profile"],
                        data["solar_scaling"],
                        data["battery_type"],
                    );
                }

            }
        }
    }

</script>

<style lang="scss" scoped>

    @import "./src/variables.scss";

    .background{
        position:relative;
        overflow:auto;
        height:95vh;
    }

    .main-container {
        // margin:15vh 0 1vh 0;
        animation-name: fade-in;
        animation-duration: 1s;

        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items: center;

        min-height:95vh;
        // max-height:95vh;
        
        // overflow:scroll;
        width:100%;
        // margin: 5vh 0 0 0;
        // background-color:green;
    }

    .participants-table {
        // border: 1px solid grey;
        // border-radius:4px;
        margin: 2vh 1vw 4vh 1vw;
        width:90%;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        color:$container-text;
        background-color: $container-bg;
        color:$container-text;
        min-width:75vw;
        // min-height:100vh;
        
        /* padding: 0vh 0 1.5vw 0; */
        
    }

    .participants-table-heading{
        background-color: $heading-bg;
        color: $heading-text;
        width:100%;
        font-size:1.2em;
    }

    .participants-table table{
        margin: 1vh 0 1vh 0;
    }

    td{
        /* background-color:green; */
        padding:0 1vw 0 1vw;
    }

    .add-participant-button{
        background-color:$button-primary;
        color:$button-text;
        padding: 1vh 1vw 1vh 1vw;
        border-radius:4px;
        width: 10vw;
        margin: 1vh 1vw 1vh 1vw;
        font-size: 0.8em;
        cursor:pointer;
    }
    
    .button {

    }

    .files-select-container {
        display: flex;
        flex-direction: row;
        width:50%;
        justify-content: space-evenly;
        align-items: center;

    }

    .file-buttons-container {

    }

    .config-button{
        background-color:$button-primary;
        color:$button-text;
        padding: 1vh 1vw 1vh 1vw;
        border-radius:4px;
        cursor:pointer;
        width: 10vw;
        margin: 1vh 0 1vh 0;
    }

    .modal-container{
        background-color:$container-bg;
        height:50vh;
        width:100%;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        color:$container-text;
    }

    .modal-header{
        background-color:$heading-bg;
        color:$heading-text;
        width:100%;
        padding: 1vh 0 1vh 0;
        text-align:center;
    }

    

    .close-button{
        background-color:$button-warning;
        color:$button-text;
        cursor:pointer;
        margin: 2vh 0 2vh 0;
        padding: 1vh 1vw 1vh 1vw;
        border-radius:4px;
        margin: 0 2vw 0 2vw;
        width:10vw;
        text-align:center;

    }

    .close-autofill-button{
        background-color:$button-primary;
        color:$button-text;
        cursor:pointer;
        margin: 2vh 0 2vh 0;
        padding: 1vh 1vw 1vh 1vw;
        border-radius:4px;
        margin: 0 2vw 0 2vw;
        width:10vw;
        text-align:center;
    }
    .config-heading{
        background-color:$heading-bg;
        color:$heading-text;
        font-size:1.2em;
    }

    .config-content{
        display:flex;
        flex-direction:row;
        padding: 1vh 1vw 1vh 1vw;
        justify-content: space-around
    }

    .config-info{
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        
        min-width:75vw;
        // height:30vh;

        background-color:$container-bg;
        color:$container-text;
        
    }

    .config-selected{
        display:flex;
        flex-direction:column;
        justify-content: space-around;

    }

    .show-data-button{
        font-size: 0.7em;
        background-color:$button-primary;
        color:$button-text;
        border-radius:4px;
        cursor: pointer;
        padding: 0 0.5vw 0 0.5vw;
    }

    .spacer{
        width:1px;
        height:1px;
        color:$bg;
    }

    .view-title{
        display:flex;
        flex-direction:row;
        justify-content:flex-start;
        width:100%;
        
        padding:0 0 0 5vw;
        font-weight:bold;
        margin: 1vh 0 5vh 0;
    }

    .modal-close-buttons{
        display:flex;
        flex-direction:row;
        margin: 4vh 0 0 0;
    }

    .remove-row-button{
        font-size: 0.7em;
        background-color:$button-warning;
        color:$button-text;
        border-radius:4px;
        cursor: pointer;
        padding: 0 0.5vw 0 0.5vw;
    }


</style>