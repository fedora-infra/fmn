<script setup lang="ts">
import { useEditRuleMutation } from "@/api/rules";
import type { GenerationRule, PostError, Rule } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import { CAlert, CCol, CRow } from "@coreui/bootstrap-vue";
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

const { mutateAsync } = useEditRuleMutation(props.rule.id);

const handleSubmit = async (data: Rule, form: FormKitNode | undefined) => {
  console.log("Will edit the rule:", data);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    const response = await mutateAsync(data);
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
    <CRow class="mb-2">
      <CCol xs="auto" class="me-auto">
        <h4>
          <EditableName
            name="name"
            button-class="fs-3"
            input-class="form-control-lg"
            :value="props.rule.name"
          />
        </h4>
      </CCol>
      <CCol xs="auto">
        <FormKit
          type="submit"
          :class="['btn', 'btn-primary', 'form-control-lg']"
          :disabled="!formReady"
        >
          Save Rule
        </FormKit>
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
