<script setup lang="ts">
const props = defineProps<{
  name: string;
  options: string[];
}>();
defineEmits<{ (e: "change", value: string | null): void }>();
</script>

<template>
  <FormKit type="select" :name="props.name">
    <option value="">(no filter)</option>
    <option v-for="option in props.options" :key="option" :value="option">
      {{ option }}
    </option>
  </FormKit>
</template>
