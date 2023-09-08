<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { validationErrorToFormErrors } from "@/api";
import { useDeleteRuleMutation, useEditRuleMutation } from "@/api/rules";
import type { GenerationRule, HTTPValidationError, Rule } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import {
  CAlert,
  CButton,
  CButtonGroup,
  CCol,
  CRow,
} from "@coreui/bootstrap-vue";
import { cilTrash } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import type { FormKitGroupValue, FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import type { AxiosError } from "axios";
import { computed, ref, toRefs } from "vue";
import { useRouter } from "vue-router";
import GenerationRuleList from "./rule-edit/generation-rule/GenerationRuleList.vue";
import TrackingRule from "./rule-edit/tracking-rule/TrackingRule.vue";

const props = defineProps<{
  rule: Rule;
}>();

const { rule } = toRefs(props);
const toastStore = useToastStore();
const router = useRouter();

const { mutateAsync: editMutation } = useEditRuleMutation(rule.value.id);

const handleSubmit = async (
  data: FormKitGroupValue,
  form: FormKitNode | undefined,
) => {
  console.log("Will edit the rule:", data);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    await editMutation(data as Rule);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule edited",
      content: `Rule has been successfully edited.`,
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

const { mutateAsync: deleteMutate } = useDeleteRuleMutation();

const handleDelete = async (rule: Rule) => {
  console.log("Will delete the rule:", rule);
  try {
    await deleteMutate(props.rule.id);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule deleted",
      content: `Rule has been successfully deleted.`,
    });
    router.push("/");
  } catch (err) {
    const error = err as AxiosError<HTTPValidationError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    const errors = validationErrorToFormErrors(error.response.data);
    toastStore.addToast({
      color: "danger",
      title: "Deletion failed!",
      content: `Rule could not be deleted!\n${errors.join("\n")}`,
    });
  }
};

const generationRulesCount = ref(rule.value.generation_rules.length);
const handleGenerationRulesChanged = (rules: GenerationRule[]) => {
  generationRulesCount.value = rules.length;
};
const formReady = computed(() => generationRulesCount.value > 0);
</script>

<template>
  <FormKit
    type="form"
    id="rule"
    @submit="handleSubmit"
    :actions="false"
    :value="props.rule"
  >
    <CRow class="mb-4 align-items-center">
      <CCol xs="auto" class="flex-fill">
        <h3 class="m-0">Editing rule {{ props.rule.id }}</h3>
      </CCol>
      <CCol xs="auto">
        <CButtonGroup>
          <CButton
            @click.prevent="handleDelete"
            color="danger"
            variant="outline"
            class="ms-1"
            type="button"
          >
            <CIcon :icon="cilTrash" /> Delete Rule
          </CButton>
          <router-link to="/" class="btn btn-outline-secondary"
            >Cancel changes</router-link
          >
          <FormKit
            type="submit"
            :classes="{ input: 'rounded-0 rounded-end' }"
            :disabled="!formReady"
          >
            Save Rule
          </FormKit>
        </CButtonGroup>
      </CCol>
    </CRow>

    <CRow>
      <CCol sm="12" md="4">
        <FormKit
          type="checkbox"
          name="disabled"
          label="Rule Enabled?"
          label-class="fw-bold mt-5"
          :on-value="false"
          :off-value="true"
        />
        <FormKit
          type="text"
          name="name"
          label="Rule Title:"
          label-class="fw-bold mb-0"
          placeholder="Optional Rule Title"
          input-class="form-control"
        />
        <TrackingRule />
      </CCol>
      <CCol>
        <h5 class="d-md-none mt-3">Destinations:</h5>
        <GenerationRuleList
          @change="handleGenerationRulesChanged"
          :rules="props.rule.generation_rules"
        />
        <CAlert v-if="generationRulesCount === 0" color="warning" class="mt-2"
          >There must be at least one destination</CAlert
        >
      </CCol>
    </CRow>
  </FormKit>
</template>
