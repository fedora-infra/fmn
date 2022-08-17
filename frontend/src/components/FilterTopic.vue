<script setup lang="ts">
//const props = defineProps<{ value: string | null }>();
//const emit = defineEmits(["change"]);
</script>

<template>
  <p>Only notify if the message topic matches the following pattern:</p>
  <FormKit
    type="text"
    name="topic"
    placeholder="Topic pattern"
    help="Wildcards: * and ?"
  />
</template>
