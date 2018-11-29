<script>
    import { Bar, mixins } from 'vue-chartjs';
    const { reactiveProp } = mixins;

    export default {
        extends: Bar,
        mixins: [ reactiveProp ],
        props: {
            options: {
                type: Object,
                default: null
            }
        },

        mounted () {
            this.renderChart(this.chartData, this.options)
        },
    }
</script>

<style scoped>

</style>