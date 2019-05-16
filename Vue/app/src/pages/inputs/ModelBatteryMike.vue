<template>
    <div class="background">
            <div class="container">
                <div class="container-header">Central Battery</div>
                <div class="central-battery-config">
                    <span class="input-line">
                    <span>Battery Type</span>
                        <SimpleDropdown 
                            v-model="input_data.central_battery_type"
                            :my_options="battery_types"
                            :my_placeholder="null"/>

                    </span>

                    <span class="input-line">
                    <span>Dispatch Strategy</span>
                        
                        <SimpleDropdown 
                            v-model="input_data.central_dispatch_strategy"
                            :my_options="dispatch_strategies"
                            :my_placeholder="null"/>
                    </span>

                    

                    
                </div>
            </div>

            <div class="container">
                <div class="container-header">Participant Batteries</div>
                <div class="participant-config" v-for="(value, name, index) in input_data.participant_batteries" v-bind:key="name">
                    <div class="participant-heading">{{name}}</div>
                    <!-- <div class="add-battery-button" v-on:click="add_battery(name)">Add Battery</div> -->
                    <div class="battery-config"  v-if="show_participant_battery[index]">
                        <span class="input-line" >
                        <span>Battery Type</span>
                            <SimpleDropdown 
                                v-model="input_data.participant_batteries[name].type"
                                :my_options="battery_types"
                                :my_placeholder="null"/>
                        </span>

                        <span class="input-line">
                        <span>Dispatch Strategy</span>
                            
                            <SimpleDropdown 
                                v-model="value.dispatch_strategy"
                                :my_options="dispatch_strategies"
                                :my_placeholder="null"/>
                        </span>

                        <span class="input-line">
                        <span>Capacity (kWh)</span>
                            
                            <SimpleNumberInput
                            v-model="value.capacity_kWh"
                            :my_placeholder="null"/>
                        </span>
                    </div>
                    <div v-else>
                        <div class="add-battery-button" v-on:click="add_battery(index)">Add Battery</div>
                    </div>
                </div>
            
            </div>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';
    import SaveLoad from '@/mixins/SaveLoad.vue';
    import Vue from 'vue'

    export default {
        name: "battery_mike",
        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        mixins: [SaveLoad],

        data () {
            
            return {
                view_name: this.$options.name,
                model_page_name: "battery_mike",
                // heading_text: "Central Services",
                battery_types:['pw_26','pw_52','pw_78','pw_104','pw_scale','powerwall2_1','powerwall2_2','powerwall2_3','powerwall2_4',],
                dispatch_strategies:['ed1700_cmax_dmax','ed1700_c20_d20','ed1730_cmax_dmax','ed1630_c20_d20','ch_ed1630_cmax_d20','ch_ed1700_cmax_dmax','sc1700_c20_dmax','sc1700_cmax_dmax','dc1700_c20_dmax','dc1700_cmax_dmax','pdt_pps_80','pdt_pps_85','pdt_pps_90','pdt_pps_95','pdt_ch_80','pdt_sc_80','pdt_sc_75','pdt_sc_70','pdt_sc_65','pdt_sc_60','pdt_sc_55','pdt_sc_50','pdt_sc_45','pdt_sc_40','pdt_sc_35','pdt_sc_30'],
                show_participant_battery:[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,],
                
                input_data: {
                    central_battery_type:null,
                    central_dispatch_strategy:null,
                    participant_batteries:{
                    },
                },

            }
        },

        

        computed:{
            // participant_batteries(){
            //     var array = [];
            //     for(var name in this.input_data.participant_batteries){
            //         array.push({
            //             name:name, 
            //             has_battery:this.input_data.participant_batteries[name].has_battery
            //             type:this.input_data.participant_batteries[name].type,
            //             dispatch_strategy:this.input_data.participant_batteries[name].has_battery
            //             })
            //     }
            //     return this.input_data.participant_batteries;
            // },
            participants(){
                let participant_names = [];
                let pm_data = this.$store.state.frontend_state["model_participants_mike"];
                console.log('Participants Data', pm_data['table_rows']);
                if(pm_data){
                    for(var i = 0; i< pm_data.table_rows.length; i++){ 
                        for(var j = 0; j< pm_data.table_rows[i].row_inputs.length; j++){
                            if(pm_data.table_rows[i].row_inputs[j]['name'] == 'participant_id'){
                                participant_names.push(pm_data.table_rows[i].row_inputs[j]['value']);
                            }
                        }
                    }
                }
                return participant_names
            }
        },

        methods: {
            add_battery(index){
                console.log('Adding Battery at index', index)
                this.show_participant_battery.splice(index, 1, true);
            },
            initialise_participant_batteries(){
                console.log('ModelBatteryMike.vue/initialise_participant_batteries() called')
                // If each participant not in participant batteries array, add. 
                var participants = this.participants;
                console.log('ModelBatteryMike.vue/initialise_participant_batteries() participants', participants)
                for(var i = 0; i< participants.length; i++){
                    if(!(participants[i] in this.input_data.participant_batteries) ){
                        this.input_data.participant_batteries[participants[i]] = {capacity_kWh:null,  type:null, dispatch_strategy:null}
                    }
                }

                //if a participant has been deleted, remove from participant batteries config. 
                // for(var participant in this.input_data.participant_batteries){
                //     if(!(participant in participants) ){
                //         console.log('Deleting', participant)
                //         delete this.input_data.participant_batteries[participant]
                //     }
                // }
                var i = 0;
                for(var p_id in this.input_data.participant_batteries){
                    var participant = this.input_data.participant_batteries[p_id];
                    if(participant.capacity_kWh && participant.type && participant.dispatch_strategy){
                        this.add_battery(i);
                    }
                    i++;
                }

                console.log('ModelBatteryMike.vue/initialise_participant_batteries() ', this.input_data.participant_batteries)

            }
        },
        created() {
            this.load_page_simple();
            this.initialise_participant_batteries()
        },
        mounted(){
            
            // this.initialise_participant_batteries()
        },

        beforeDestroy() {
            this.save_page_simple();
        },
    }
</script>

<style lang="scss" scoped>
    @import "./src/variables.scss";

    .container{
        background-color:$container-bg;
        color:$container-text;
        width:75vw;
        display:flex;
        flex-direction:column;
        // align-items:flex-start;

        animation-name: fade-in;
        animation-duration: 1s;
        margin: 2vh 0 2vh 0;
    }

    .container-header{
        background-color:$heading-bg;
        color:$heading-text;
        width:100%;
        font-size:1.2em;

    }


    .background{
        height:95vh;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        overflow:auto;
    }

    .input-line {
        width:30vw;
        display:flex;
        flex-direction:row;
        justify-content:space-between;
        align-items:center;
        margin: 1vh 1vw 1vh 1vw;
    }

    .view-title {

    }

    .participant-config{
        display:flex;
        flex-direction:row;
        justify-content:space-around;
        align-items:center;
        margin: 1vh 0 1vh 0;
        background-color:$nav-bg;
        margin: 1vh 2vw 1vh 2vw;
        border-radius:4px;
        padding:1vh 0 1vh 0;
    }


    .add-battery-button{
        background-color:$button-primary;
        color:$button-text;
        padding: 0.5vh 1vw 0.5vh 1vw;
        border-radius:4px;
        cursor:pointer;

    }

    .central-battery-config{
        display:flex;
        flex-direction:row;
        justify-content:center;
        align-items:center;
        width:100%;
    }

    .participant-heading{
        font-weight:bold;
    }
    
</style>