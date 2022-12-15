<script setup lang="ts">
import { useEditRuleMutation, useDeleteRuleMutation } from "@/api/rules";
import type { GenerationRule, PostError, Rule } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import {
  CAlert,
  CCol,
  CRow,
  CButton,
  CButtonGroup,
} from "@coreui/bootstrap-vue";
import { cilTrash } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import type { FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import type { AxiosError } from "axios";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import EditableName from "./EditableName.vue";
import GenerationRuleList from "./rule-edit/generation-rule/GenerationRuleList.vue";
import TrackingRule from "./rule-edit/tracking-rule/TrackingRule.vue";

const props = defineProps<{
  rule: Rule;
}>();

const toastStore = useToastStore();
const router = useRouter();

const { mutateAsync: editMutation } = useEditRuleMutation(props.rule.id);

const handleSubmit = async (data: Rule, form: FormKitNode | undefined) => {
  console.log("Will edit the rule:", data);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    const response = await editMutation(data);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule edited",
      content: `Rule "${response.name}" has been successfully edited.`,
    });
    router.push("/");
  } catch (err) {
    const error = err as AxiosError<PostError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    form.setErrors(
      error.response.data.detail.map(
        (e) => `Server error: ${e.loc[-1]}: ${e.msg}`
      )
    );
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
      content: `Rule "${props.rule.name}" has been successfully deleted.`,
    });
    router.push("/");
  } catch (err) {
    const error = err as AxiosError<PostError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    const errors = error.response.data.detail
      .map((e) => `${e.loc[-1]}: ${e.msg}`)
      .join("\n");
    toastStore.addToast({
      color: "danger",
      title: "Deletion failed!",
      content: `Rule "${props.rule.name}" could not be deleted!\n${errors}`,
    });
  }
};

const generationRulesCount = ref(props.rule.generation_rules.length);
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
    <CRow class="mb-2 d-flex">
      <CCol xs="auto" class="flex-grow-1 d-flex align-items-center h3">
        <FormKit
          type="checkbox"
          name="disabled"
          :on-value="false"
          :off-value="true"
        />
        <h4 class="mb-0 flex-grow-1">
          <EditableName
            name="name"
            button-class="fs-3"
            input-class="form-control-lg"
            :value="props.rule.name"
          />
        </h4>
      </CCol>
      <CCol xs="auto" class="d-flex align-items-center">
        <CButtonGroup>
          <CButton
            @click.prevent="handleDelete"
            color="danger"
            variant="outline"
            class="ms-1"
          >
            <CIcon :icon="cilTrash" /> Delete Rule
          </CButton>
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
      <CCol sm="4" class="border-end">
        <TrackingRule />
      </CCol>
      <CCol>
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
