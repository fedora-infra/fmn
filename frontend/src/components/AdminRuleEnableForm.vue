<script setup lang="ts">
import { validationErrorToFormErrors } from "@/api";
import { usePatchRuleMutation } from "@/api/rules";
import type { PostError, Rule, RulePatch } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import type { FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import type { AxiosError } from "axios";

const props = defineProps<{
  rule: Rule;
}>();

const toastStore = useToastStore();

const { mutateAsync: editMutation } = usePatchRuleMutation();

const handleSubmit = async (data: RulePatch, form: FormKitNode | undefined) => {
  console.log(`Will enable rule ${data.id}`);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    const response = await editMutation(data);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule enabled",
      content: `Rule "${response.name}" has been successfully enabled.`,
    });
  } catch (err) {
    const error = err as AxiosError<PostError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    form.setErrors(validationErrorToFormErrors(error.response.data));
  }
};
</script>

<template>
  <FormKit type="form" id="rule" @submit="handleSubmit" :actions="false">
    <FormKit type="hidden" name="id" :value="props.rule.id" />
    <FormKit type="hidden" name="disabled" :value="false" />
    <FormKit type="submit"> Enable Rule {{ props.rule.id }} </FormKit>
  </FormKit>
</template>
