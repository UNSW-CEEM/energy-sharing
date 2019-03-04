<template>
    <div class="main-container">
        <LoadUpload/>
    </div>
</template>

<script>
    import LoadUpload from '@/components/LoadUpload.vue';

    export default {
        name: "Data",
        components: {
            LoadUpload
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_data",
                load_files: [],
            }
        },

        methods: {

        },
    }
</script>

<style scoped>
    .main-container {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: start;
    }

    span {
        animation-name: fade-in;
        animation-duration: 2s;
    }
</style>