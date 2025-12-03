<!-- Vue v-html XSS -->
<template>
    <div v-html="userContent"></div>
</template>

<script>
export default {
    data() {
        return {
            userContent: this.$route.query.content // VULNERABLE
        }
    }
}
</script>