<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { validationErrorToFormErrors } from "@/api";
import { useAddRuleMutation } from "@/api/rules";
import type { GenerationRule, HTTPValidationError, Rule } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import { CCol, CRow } from "@coreui/vue";
import type { FormKitGroupValue, FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import type { AxiosError } from "axios";
import { computed, ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter, onBeforeRouteLeave } from "vue-router";
import GenerationRuleList from "./rule-edit/generation-rule/GenerationRuleList.vue";
import TrackingRule from "./rule-edit/tracking-rule/TrackingRule.vue";

const toastStore = useToastStore();
const router = useRouter();

const { mutateAsync } = useAddRuleMutation();

const trackingRuleName = ref("");

const generationRulesCount = ref(0);

const newRuleForm = ref<{ node: FormKitNode } | null>(null);
const isDirty = computed(
  () => newRuleForm.value?.node.context?.state.dirty === true,
);

const formReady = computed(
  () => trackingRuleName.value !== "" && generationRulesCount.value > 0,
);

const handleSubmit = async (
  data: FormKitGroupValue,
  form: FormKitNode | undefined,
) => {
  console.log("Will submit the new rule:", data);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    await mutateAsync(data as Rule);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule created",
      content: `Rule has been successfully created.`,
    });
    router.push("/");
  } catch (err) {
    const error = err as AxiosError<HTTPValidationError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    form.setErrors(validationErrorToFormErrors(error.response.data));
  }
};

const handleTrackingRuleSelected = (name: string) => {
  trackingRuleName.value = name;
};
const handleGenerationRulesChanged = (rules: GenerationRule[]) => {
  generationRulesCount.value = rules.length;
};

const onCancel = () => {
  router.push("/");
};

// Warning on tab close or hard navigation away
const beforeUnloadHandler = (e: BeforeUnloadEvent) => {
  if (!isDirty.value) return;
  e.preventDefault();
  e.returnValue = "";
};
onMounted(() => {
  window.addEventListener("beforeunload", beforeUnloadHandler);
});
onBeforeUnmount(() => {
  window.removeEventListener("beforeunload", beforeUnloadHandler);
});

// Warn on in-app navigation away/route changes
onBeforeRouteLeave((_to, _from, next) => {
  if (!isDirty.value) {
    next();
    return;
  }
  if (window.confirm("You have not saved the new rule yet. Discard new rule?")) next();
  else next(false)
});

</script>

<template>
  <FormKit type="form" id="new-rule" @submit="handleSubmit" :actions="false" ref="newRuleForm">
    <!-- Track if the user has made changes in the form-->  

    <CRow class="mb-2 align-items-center">
      <CCol xs="auto" class="flex-fill">
        <h4>Create a new Rule</h4>
      </CCol>
    </CRow>

    <CRow>
      <CCol sm="12" md="4">
        <FormKit
          type="text"
          name="name"
          label="Rule Title:"
          label-class="fw-bold mb-0"
          placeholder="Optional Rule Title"
          input-class="form-control"
        />
        <TrackingRule @selected="handleTrackingRuleSelected" />
      </CCol>
      <CCol>
        <h5 class="d-md-none mt-3">Destinations:</h5>
        <GenerationRuleList
          v-if="!!trackingRuleName"
          @change="handleGenerationRulesChanged"
        />
      </CCol>
    </CRow>
    
    <!-- Moved the primary action button from the top-right to the bottom -->
    <CRow class="mt-3">
      <CCol class="d-flex justify-content-end gap-3">
        <button
          type="button"
          class="btn btn-secondary"
          @click="onCancel"
          aria-label="Cancel rule creation"
        >
          Cancel
        </button>
        <FormKit
          type="submit"
          :class="['btn', 'btn-primary', 'form-control-lg']"
          :disabled="!formReady"
          aria-label="Save rule"
        >
          Save Rule
        </FormKit>
      </CCol>
    </CRow>

  </FormKit>
</template>
