<script>
    import { Line } from 'vue-chartjs'

    export default {
        mixins: [ Line ],
        props: {
            chart_data: {
                type: Object,
                default: null
            },

            chart_options: {
                type: Object,
                default: null
            }
        },

        mounted () {
            this.renderChart(this.chart_data, this.chart_options)
        }
    }
</script>

<style scoped>

</style>