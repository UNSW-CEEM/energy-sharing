<template>
    <div class="container">
        <h3> Dates </h3>
        <div class="range solar" :style="{width: solar_percent+'%'}">
            {{solar_filename}} {{load_start}}
        </div>

        <div class="range load" :style="{width: load_percent+'%'}">
            {{load_filename}}
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
            }

        

        },
        data () {
            return {

            }
        }
    }
</script>

<style scoped>

.container{
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
    align-items:center;
    width:100%;
    background-color:grey;
    border-radius:4px;
}

.solar{
    background-color:#a4a83c;
}

.load{
    background-color:#31a54c;
}

.range{
    border-radius:4px;
}

</style>