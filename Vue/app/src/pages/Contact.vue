<template>
    <div>
        <h1>Contact Us</h1>
        <p>
            <ul>
                    <li>Email: {{email}}</li>
                    <li>Website: {{web}}</li>
            </ul>
        </p>
    </div>
</template>

<script>
    export default {
        name: "Contact",
        data () {
            return {
                email: "dave@example.com",
                web: "example@example.com"
            }
        }
    }
</script>

<style scoped>

</style>