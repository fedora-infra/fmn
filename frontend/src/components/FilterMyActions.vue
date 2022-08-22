<script setup lang="ts">
//const props = defineProps<{ value: boolean }>();
//const emit = defineEmits(["change"]);
</script>

<template>
  <p class="mb-0">Notify even if I'm the author of the action:</p>
  <FormKit type="checkbox" name="my_actions" label="Include my actions" />
</template>
