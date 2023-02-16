<script setup lang="ts">
import { validationErrorToFormErrors } from "@/api";
import { usePatchRuleMutation } from "@/api/rules";
import type { PostError, RulePatch } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import { CInputGroup } from "@coreui/bootstrap-vue";
import type { FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import type { AxiosError } from "axios";

const toastStore = useToastStore();

const { mutateAsync: editMutation } = usePatchRuleMutation();

const handleSubmit = async (data: RulePatch, form: FormKitNode | undefined) => {
  console.log(`Will disable rule ${data.id}`);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    const response = await editMutation(data);
    form.reset();
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule disabled",
      content: `Rule "${response.name}" has been successfully disabled.`,
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
  <FormKit
    type="form"
    id="rule"
    @submit="handleSubmit"
    :actions="false"
    #default="{ state: { valid } }"
  >
    <FormKit type="hidden" name="disabled" :value="true" />
    <CInputGroup>
      <FormKit
        type="text"
        name="id"
        value=""
        placeholder="Rule ID"
        :classes="{ input: 'rounded-0 rounded-start' }"
        validation="required | number"
      />
      <FormKit
        type="submit"
        :disabled="!valid"
        :classes="{ input: 'rounded-0 rounded-end btn-danger' }"
      >
        Disable Rule
      </FormKit>
    </CInputGroup>
  </FormKit>
</template>
