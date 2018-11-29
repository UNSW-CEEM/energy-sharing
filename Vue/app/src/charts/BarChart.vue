<script>
    import { Bar } from 'vue-chartjs'

    export default {
        mixins: [ Bar ],
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