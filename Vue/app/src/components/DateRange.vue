<template>
    <div class="date-container">
        <div class="date-headings">
            <div class="date"> {{total_range_start.format('DD MMM YY')}} </div>
            <div v-if="!valid_range" class="heading"> No Date Crossover in Datasets</div>
            <div class="date"> {{total_range_end.format('DD MMM YY')}} </div>
        </div>

        <div class="range-holder">
            <div class="range solar" :style="{width: solar_percent+'%', 'margin-left':solar_offset_percent+'%'}">
                <span>Solar</span>
            </div>
        </div>

         <div class="range-holder">
            <div v-if="valid_range" class="range experiment" :style="{width: experiment_percent+'%', 'margin-left':experiment_offset_percent+'%'}">
                <div class="line"></div>
                <span class="heading">Simulation</span>
                <div class="line"></div>
            </div>
        </div>

        <div class="range-holder">
            <div class="range load" :style="{width: load_percent+'%', 'margin-left':load_offset_percent+'%'}">
                <span>Load</span>
            </div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment'

    export default {
        name: "DateRange",
        props: ["load_start_date", "load_end_date", "solar_start_date", "solar_end_date", "solar_filename", "load_filename"],
        computed:{
            load_start(){
                return moment(this.load_start_date);
            },
            load_end(){
                return moment(this.load_end_date);
            },
            solar_start(){
                return moment(this.solar_start_date);
            },
            solar_end(){
                return moment(this.solar_end_date);
            },
            total_range_start(){
                if (this.solar_start < this.load_start){
                    return this.solar_start
                }else{
                    return this.load_start
                }
            },
            total_range_end(){
                if(this.solar_end > this.load_end){
                    return this.solar_end;
                }else{
                    return this.load_end;
                }
            },
            solar_percent(){
                var solar_length = this.solar_end.diff(this.solar_start);
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 *solar_length / total_length;
            },
            load_percent(){
                var load_length = this.load_end.diff(this.load_start);
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 *load_length / total_length;
            },
            load_offset_percent(){
                var load_start_length = this.load_start.diff(this.total_range_start);
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 * load_start_length / total_length;
            },
            solar_offset_percent(){
                var solar_start_length = this.solar_start.diff(this.total_range_start);
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 * solar_start_length / total_length;
            },

            experiment_start(){
                //whichever one starts later
                if(this.solar_start > this.load_start){
                    return this.solar_start;
                }else{
                    return this.load_start;
                }
            },
            experiment_end(){
                if(this.solar_end < this.load_end){
                    return this.solar_end
                }else{
                    return this.load_end
                }
            },

            experiment_percent(){
                var experiment_length = this.experiment_end.diff(this.experiment_start)
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 * experiment_length / total_length;
            },
            experiment_offset_percent(){
                var experiment_start_length = this.experiment_start.diff(this.total_range_start);
                var total_length = this.total_range_end.diff(this.total_range_start);
                return 100.0 * experiment_start_length / total_length;
            },

            valid_range(){
                if(this.load_start > this.solar_end || this.solar_start > this.load_end){
                    return false;
                }
                return true;
            }
            


        },
        data () {
            return {

            }
        }
    }
</script>

<style lang="scss" scoped>

@import "./src/variables.scss";
.date-container{
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
    align-items:center;
    width:75vw;
    background-color:$heading-bg;
    border-radius:4px;
    padding-bottom:1vh;
    
}

.dates{
        width:90%;
        background-color:$heading-bg;
        padding: 2vh 1vw 2vh 1vw;
        border-radius:4px;
        // max-height:20vh;
    }

.solar{
    background-color:$secondary;
    
}

.load{
    background-color:$tertiary;
}

.range{
    border-radius:4px;
    display:flex;
    flex-direction:row;
    justify-content:center;
}

.range-holder{
    width:100%;
    display:flex;
    flex-direction:row;
    margin: 1vh 0 1vh 0;
}

.date-headings{
    display:flex;
    flex-direction:row;
    justify-content:space-between;
    align-items:center;
    width:100%;
    
}

.date-headings .date{
    margin: 0 0.2vw 0 0.2vw;
}

.experiment{
    border-left: 2px solid black;
    border-right: 2px solid black;
    border-radius:0px;
    display:flex;
    flex-direction:row;
    justify-content:space-between;
    align-items:center;
}

.line{
    width:100%;
    
    height:0px;
    border: 0.5px solid black;
    background-color:black;
}

.experiment .heading{
    margin: 0 1vw 0 1vw;
}



</style>